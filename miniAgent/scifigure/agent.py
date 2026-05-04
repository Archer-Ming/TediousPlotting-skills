"""绘图 Agent。

工作流：
1) 把启用的 Skill 内容注入 system prompt。
2) 用户消息 + 数据画像（列名 / dtype / 样例几行）一起给 LLM。
3) LLM 返回结构化 JSON：{kind: "code"|"answer", message, code?}。
4) 如果是 code：用沙箱执行，失败则把错误回喂给 LLM 让其修复（最多 N 次）。
5) 多轮：保留对话历史以支持继续追问、迭代美化。
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Callable, Optional

import pandas as pd
import requests

from .config import AppConfig
from .executor import CodeExecutor, ExecutionResult
from .skill_manager import SkillManager


@dataclass
class AgentStep:
    """Agent 的一步动作，用于在 UI 中流式显示思考过程。"""
    kind: str  # "thinking" | "code" | "exec_ok" | "exec_fail" | "answer" | "error"
    text: str = ""
    code: str = ""
    image_path: Optional[str] = None


@dataclass
class AgentTurn:
    """一次完整的对话回合最终结果。"""
    final_message: str = ""
    image_path: Optional[str] = None
    code: str = ""
    success: bool = True


@dataclass
class ChatMessage:
    role: str  # "user" / "assistant" / "system"
    content: str


class PlottingAgent:
    """对接 OpenAI 兼容协议的绘图 Agent。"""

    def __init__(
        self,
        config: AppConfig,
        skill_manager: SkillManager,
        executor: CodeExecutor,
        max_repair_rounds: int = 2,
    ) -> None:
        self.config = config
        self.skills = skill_manager
        self.executor = executor
        self.max_repair_rounds = max_repair_rounds
        self.history: list[ChatMessage] = []

    # --------------------- 配置 ---------------------
    def update_config(self, config: AppConfig) -> None:
        self.config = config

    def reset_history(self) -> None:
        self.history.clear()

    # --------------------- 主流程 ---------------------
    def chat(
        self,
        user_message: str,
        df: pd.DataFrame | None,
        on_step: Callable[[AgentStep], None] | None = None,
    ) -> AgentTurn:
        """执行一轮对话。on_step 在每个中间步骤被调用以便 UI 流式展示。"""
        def emit(step: AgentStep) -> None:
            if on_step is not None:
                try:
                    on_step(step)
                except Exception:
                    pass

        # 用户消息进历史
        self.history.append(ChatMessage("user", user_message))

        if not self.config.api_key:
            msg = "尚未配置大模型 API Key，请点击左下角“⚙️ 模型配置”填写后再试。"
            emit(AgentStep("error", text=msg))
            self.history.append(ChatMessage("assistant", msg))
            return AgentTurn(final_message=msg, success=False)

        system_prompt = self._build_system_prompt(df)
        messages = [{"role": "system", "content": system_prompt}]
        for m in self.history:
            messages.append({"role": m.role, "content": m.content})

        try:
            raw = self._call_llm(messages)
        except Exception as exc:
            msg = f"调用大模型失败：{exc}"
            emit(AgentStep("error", text=msg))
            self.history.append(ChatMessage("assistant", msg))
            return AgentTurn(final_message=msg, success=False)

        payload = self._parse_payload(raw)
        kind = payload.get("kind", "answer")
        message = str(payload.get("message", "")).strip()

        if kind == "answer" or "code" not in payload:
            final = message or "（无内容）"
            emit(AgentStep("answer", text=final))
            self.history.append(ChatMessage("assistant", final))
            return AgentTurn(final_message=final, success=True)

        # ---- 代码路径，进入执行+修复循环 ----
        code = str(payload.get("code", "")).strip()
        if message:
            emit(AgentStep("thinking", text=message))
        emit(AgentStep("code", code=code))

        last_result: ExecutionResult | None = None
        for attempt in range(self.max_repair_rounds + 1):
            result = self.executor.run(code, df)
            last_result = result
            if result.success:
                emit(AgentStep("exec_ok", text="渲染成功", image_path=result.image_path, code=code))
                # 把这次产出归档进历史，让模型在下一轮记得
                history_text = (
                    f"{message}\n\n[已执行的绘图代码]:\n```python\n{code}\n```\n（执行成功，已生成图像）"
                )
                self.history.append(ChatMessage("assistant", history_text))
                return AgentTurn(
                    final_message=message or "已为你生成图表。",
                    image_path=result.image_path,
                    code=code,
                    success=True,
                )

            err = result.short_error or "未知错误"
            emit(AgentStep("exec_fail", text=f"第 {attempt+1} 次尝试失败：{err}"))

            if attempt >= self.max_repair_rounds:
                break

            # 触发修复：把错误反馈给 LLM
            repair_messages = list(messages)
            repair_messages.append({"role": "assistant", "content": raw})
            repair_messages.append({
                "role": "user",
                "content": (
                    f"代码执行失败，错误信息：\n{err}\n\n"
                    f"完整 stderr（尾部）：\n{result.stderr[-1500:] if result.stderr else ''}\n\n"
                    f"请仅返回严格 JSON，修复 code 字段中的代码并重新发送（继续使用 df 变量）。"
                ),
            })
            try:
                raw = self._call_llm(repair_messages)
            except Exception as exc:
                emit(AgentStep("error", text=f"修复调用失败：{exc}"))
                break
            payload = self._parse_payload(raw)
            new_code = str(payload.get("code", "")).strip()
            new_msg = str(payload.get("message", "")).strip()
            if not new_code:
                # 模型放弃了
                if new_msg:
                    emit(AgentStep("answer", text=new_msg))
                self.history.append(ChatMessage("assistant", new_msg or "无法绘制。"))
                return AgentTurn(final_message=new_msg or "无法绘制。", success=False)
            code = new_code
            if new_msg:
                emit(AgentStep("thinking", text=new_msg))
            emit(AgentStep("code", code=code))

        # 走到这里说明所有尝试都失败
        final = (
            f"已尝试 {self.max_repair_rounds + 1} 次仍未渲染成功。最后错误：{last_result.short_error if last_result else ''}"
        )
        emit(AgentStep("error", text=final))
        self.history.append(ChatMessage("assistant", final))
        return AgentTurn(final_message=final, code=code, success=False)

    # --------------------- prompt 构造 ---------------------
    def _build_system_prompt(self, df: pd.DataFrame | None) -> str:
        skill_block = self.skills.build_prompt_section()
        data_block = self._dataframe_brief(df)

        return f"""你是 SciFigure AI Studio 的绘图 Agent，在用户的桌面应用中协助科研绘图。
你必须严格遵守激活的技能（skills）中给出的模板代码、配色、字体、图表风格。

【输出格式 - 重要】
你的每次回复**必须**是一个严格的 JSON 对象，不要使用 Markdown 代码块包裹整个 JSON，不要写任何解释性前缀或后缀。
JSON 字段：
- "kind": "code" 表示要绘图，"answer" 表示纯文字回答。
- "message": 给用户看的简短中文说明（例如：选择了什么图，为什么这样选）。
- "code": 当 kind=="code" 时必填。一段完整可独立运行的 Python 代码字符串。

【代码编写规则】
1. 用户的 DataFrame 已经预加载为变量 `df`，直接使用，不要 read_csv / read_excel。
2. 已可用的库：matplotlib.pyplot as plt、numpy as np、pandas as pd、seaborn as sns。**不要**额外 import 网络/系统/文件库（os/sys/subprocess/requests 等都禁用，会被沙箱拒绝）。
3. 代码末尾不要 plt.show()，沙箱会自动捕获当前 figure 保存为 PNG。也不要 plt.savefig()，沙箱负责保存。
4. 必须包含科研级 rcParams 设置（参见 skills 中的“前提”一节）。中文标题/标签时同时设置 SimHei，否则 Times New Roman。
5. 使用 skills 中给出的科研配色（colors 列表）；优先按用户指定的图表类型套用对应模板，不在模板中的可基于风格自创。
6. 对 df 列名做防御性检查：若用户提到的列不存在，从 df.columns 里挑最接近的；若数据不足，在 message 中说明并选择降级方案。
7. 一段代码只输出一张主图（可以包含 subplots），不要循环生成多张 figure。

【对话规则】
- 当用户询问数据情况、问"适合画什么"、问操作建议等没有明确画图诉求时，kind="answer"，用 message 给出简明回答。
- 当用户明确要求绘图、修改图、迭代美化、改颜色、加图例等，kind="code"。
- 用户后续要求"再修改 / 改成 X / 把标题换成 Y"时，记忆上一轮的代码，在其基础上修改而不是重新开始。

{skill_block if skill_block else "（当前未加载任何技能，按通用科研绘图规范处理。）"}

{data_block}
""".strip()

    @staticmethod
    def _dataframe_brief(df: pd.DataFrame | None) -> str:
        if df is None or df.empty:
            return "<dataset>当前未导入任何数据。如果用户要求绘图，请提示先导入数据。</dataset>"
        try:
            dtypes = {c: str(t) for c, t in df.dtypes.items()}
            head = df.head(6).to_dict(orient="records")
            numeric_cols = list(df.select_dtypes("number").columns)
            cat_cols = [c for c in df.columns if c not in numeric_cols]
            brief = {
                "rows": len(df),
                "columns": list(df.columns),
                "dtypes": dtypes,
                "numeric_columns": numeric_cols,
                "categorical_columns": cat_cols,
                "sample_first_rows": head,
            }
            return f"<dataset>\n{json.dumps(brief, ensure_ascii=False, default=str)}\n</dataset>"
        except Exception:
            return "<dataset>数据画像生成失败。</dataset>"

    # --------------------- LLM 调用 ---------------------
    def _call_llm(self, messages: list[dict]) -> str:
        url = f"{self.config.base_url.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }
        body = {
            "model": self.config.model,
            "messages": messages,
            "temperature": 0.2,
        }
        resp = requests.post(url, headers=headers, json=body, timeout=self.config.timeout)
        if not resp.ok:
            raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:800]}")
        data = resp.json()
        return data["choices"][0]["message"]["content"]

    @staticmethod
    def _parse_payload(raw: str) -> dict:
        if raw is None:
            return {"kind": "answer", "message": "（空响应）"}
        text = raw.strip()
        # 去 markdown fence
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```\s*$", "", text)
        # 直接 json
        try:
            return json.loads(text)
        except Exception:
            pass
        # 找最大花括号块
        match = re.search(r"\{.*\}", text, re.S)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                pass
        # 兜底：把整段当成纯文字回答
        return {"kind": "answer", "message": text}
