"""Skill 管理器：加载、解析、启停 SKILL.md 风格的技能文件。

设计参考 Anthropic Skills 规范：
- 文件以 YAML frontmatter 开头（--- 包裹）
- frontmatter 至少包含 name 与 description
- 主体是技能内容（模板代码、规则、示例等），整体注入到 LLM system prompt 中
"""
from __future__ import annotations

import json
import re
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable


@dataclass
class Skill:
    skill_id: str
    name: str
    description: str
    body: str  # 不含 frontmatter 的主体文本
    source_path: str  # 原始文件路径，UI 显示用
    enabled: bool = True

    def to_prompt_block(self) -> str:
        """返回注入 system prompt 的格式化块。"""
        return (
            f"<skill name=\"{self.name}\">\n"
            f"<description>{self.description}</description>\n"
            f"<content>\n{self.body.strip()}\n</content>\n"
            f"</skill>"
        )


class SkillManager:
    """统一管理所有技能。支持目录扫描 + 用户指定路径添加。"""

    def __init__(self, default_dir: Path | None = None) -> None:
        self.default_dir = default_dir
        self._skills: dict[str, Skill] = {}
        self._index_path: Path | None = None  # 持久化已添加路径

    # --------------------- 持久化 ---------------------
    def set_index_path(self, path: Path) -> None:
        """启动时调用，指定持久化文件路径，并尝试恢复上次添加过的技能。"""
        self._index_path = path
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                for entry in data.get("skills", []):
                    src = entry.get("source_path")
                    if src and Path(src).exists():
                        try:
                            sk = self.load_from_file(Path(src), persist=False)
                            sk.enabled = bool(entry.get("enabled", True))
                        except Exception:
                            pass
            except Exception:
                pass

    def _persist(self) -> None:
        if self._index_path is None:
            return
        data = {
            "skills": [
                {"source_path": s.source_path, "enabled": s.enabled}
                for s in self._skills.values()
                if not s.source_path.startswith("<builtin>")
            ]
        }
        try:
            self._index_path.write_text(
                json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        except Exception:
            pass

    # --------------------- 加载 ---------------------
    def load_default_dir(self) -> None:
        """启动时扫描默认 skills/ 目录。"""
        if self.default_dir is None or not self.default_dir.exists():
            return
        for md in sorted(self.default_dir.glob("*.md")):
            try:
                self.load_from_file(md, persist=False)
            except Exception:
                continue

    def load_from_file(self, path: Path, persist: bool = True) -> Skill:
        text = path.read_text(encoding="utf-8")
        name, description, body = self._parse_frontmatter(text, fallback_name=path.stem)

        # 防重复：以 source_path 作为去重键
        for existing in list(self._skills.values()):
            if existing.source_path == str(path.resolve()):
                # 已存在则原地刷新内容
                existing.name = name
                existing.description = description
                existing.body = body
                if persist:
                    self._persist()
                return existing

        skill = Skill(
            skill_id=str(uuid.uuid4()),
            name=name,
            description=description,
            body=body,
            source_path=str(path.resolve()),
            enabled=True,
        )
        self._skills[skill.skill_id] = skill
        if persist:
            self._persist()
        return skill

    def remove(self, skill_id: str) -> None:
        if skill_id in self._skills:
            del self._skills[skill_id]
            self._persist()

    def set_enabled(self, skill_id: str, enabled: bool) -> None:
        if skill_id in self._skills:
            self._skills[skill_id].enabled = enabled
            self._persist()

    # --------------------- 查询 ---------------------
    def all_skills(self) -> list[Skill]:
        return list(self._skills.values())

    def enabled_skills(self) -> list[Skill]:
        return [s for s in self._skills.values() if s.enabled]

    def build_prompt_section(self) -> str:
        enabled = self.enabled_skills()
        if not enabled:
            return ""
        blocks = "\n\n".join(s.to_prompt_block() for s in enabled)
        return (
            "<skills>\n"
            "下面是当前激活的专业技能文档，请严格遵守其中规则与模板。\n"
            f"{blocks}\n"
            "</skills>"
        )

    # --------------------- 解析 ---------------------
    @staticmethod
    def _parse_frontmatter(text: str, fallback_name: str) -> tuple[str, str, str]:
        """解析 SKILL.md 的 frontmatter；容忍部分不严格的写法。"""
        name = fallback_name
        description = ""
        body = text

        # 标准 YAML frontmatter: --- ... --- (可能出现两次 --- 也尝试容错)
        match = re.match(r"^\s*---\s*\n(.*?)\n---\s*\n", text, re.S)
        if match:
            front = match.group(1)
            body = text[match.end():]
            # 简易 key: value 解析
            for line in front.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                # 兼容 "description:xxx" 与 "description: xxx"
                m = re.match(r"^([A-Za-z_][\w\-]*)\s*:\s*(.*)$", line)
                if not m:
                    continue
                key, val = m.group(1).lower(), m.group(2).strip().strip("\"'")
                if key == "name":
                    name = val or name
                elif key == "description":
                    description = val
            # 有时正文前还多一对 ---，去掉
            body = re.sub(r"^\s*---\s*\n", "", body)

        if not description:
            # 取正文第一段非空文字作为兜底描述
            for line in body.splitlines():
                stripped = line.strip()
                if stripped and not stripped.startswith("#"):
                    description = stripped[:120]
                    break

        return name or fallback_name, description, body
