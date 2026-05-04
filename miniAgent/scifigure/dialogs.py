"""精简版对话框：只保留大模型配置和手动数据录入。

旧版的 ChartTypeDialog / StyleEditorDialog / FeatureSelectionDialog 已经移除，
因为 Agent 模式下这些功能改由对话方式完成。
"""
from __future__ import annotations

import io
import re
from dataclasses import replace

import pandas as pd
from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from .config import AppConfig, save_config


class LLMConfigDialog(QDialog):
    PRESETS = {
        "OpenAI": ("https://api.openai.com/v1", "gpt-4.1-mini"),
        "DeepSeek": ("https://api.deepseek.com", "deepseek-chat"),
        "DeepSeek Reasoner": ("https://api.deepseek.com", "deepseek-reasoner"),
        "Anthropic（OpenAI 兼容代理）": ("", "claude-sonnet-4-5"),
        "自定义 OpenAI-compatible": ("", ""),
    }

    def __init__(self, config: AppConfig, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("大模型配置")
        self.setMinimumWidth(560)
        self.config = config
        self.saved_config: AppConfig | None = None
        self._build_ui()
        self._load_config(config)

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        hint = QLabel("Agent 需要可调用的 OpenAI 兼容 ChatCompletion API。保存后会写入项目根目录的 .env。")
        hint.setWordWrap(True)
        hint.setObjectName("Subtle")
        layout.addWidget(hint)

        form = QFormLayout()
        self.provider_box = QComboBox()
        self.provider_box.addItems(list(self.PRESETS.keys()))
        self.provider_box.currentTextChanged.connect(self._apply_preset)
        self.base_url_edit = QLineEdit()
        self.model_edit = QLineEdit()
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.Password)
        self.show_key_check = QCheckBox("显示 API Key")
        self.show_key_check.stateChanged.connect(self._toggle_key_visible)
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(5, 600)
        self.timeout_spin.setValue(60)
        form.addRow("服务商预设", self.provider_box)
        form.addRow("Base URL", self.base_url_edit)
        form.addRow("模型名称", self.model_edit)
        form.addRow("API Key", self.api_key_edit)
        form.addRow("", self.show_key_check)
        form.addRow("超时秒数", self.timeout_spin)
        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._save)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _load_config(self, config: AppConfig) -> None:
        self.base_url_edit.setText(config.base_url)
        self.model_edit.setText(config.model)
        self.api_key_edit.setText(config.api_key)
        self.timeout_spin.setValue(config.timeout)
        if "deepseek" in config.base_url.lower():
            self.provider_box.setCurrentText("DeepSeek")
        else:
            self.provider_box.setCurrentText("OpenAI")

    def _apply_preset(self, name: str) -> None:
        base_url, model = self.PRESETS.get(name, ("", ""))
        if name == "自定义 OpenAI-compatible":
            return
        self.base_url_edit.setText(base_url)
        self.model_edit.setText(model)

    def _toggle_key_visible(self) -> None:
        self.api_key_edit.setEchoMode(
            QLineEdit.Normal if self.show_key_check.isChecked() else QLineEdit.Password
        )

    def _save(self) -> None:
        cfg = replace(
            self.config,
            api_key=self.api_key_edit.text().strip(),
            base_url=(self.base_url_edit.text().strip() or "https://api.openai.com/v1").rstrip("/"),
            model=(self.model_edit.text().strip() or "gpt-4.1-mini"),
            timeout=int(self.timeout_spin.value()),
        )
        try:
            save_config(cfg)
        except Exception as exc:
            QMessageBox.critical(self, "保存失败", str(exc))
            return
        self.saved_config = cfg
        self.accept()


class ManualDataDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("手动输入 / 粘贴数据")
        self.setMinimumSize(720, 540)
        self.df: pd.DataFrame | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        hint = QLabel("可以直接输入 X/Y 两列，也可以从 Excel 复制整块表格后粘贴到“表格文本”里。")
        hint.setObjectName("Subtle")
        hint.setWordWrap(True)
        layout.addWidget(hint)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs, 1)

        # X/Y 简易输入
        xy_page = QWidget()
        xy_layout = QFormLayout(xy_page)
        self.x_name_edit = QLineEdit("x")
        self.y_name_edit = QLineEdit("y")
        self.x_values_edit = QPlainTextEdit()
        self.y_values_edit = QPlainTextEdit()
        self.x_values_edit.setPlaceholderText("例如：1, 2, 3, 4\n或每行一个值")
        self.y_values_edit.setPlaceholderText("例如：2.1, 2.9, 4.2, 5.0\n或每行一个值")
        xy_layout.addRow("X 列名", self.x_name_edit)
        xy_layout.addRow("Y 列名", self.y_name_edit)
        xy_layout.addRow("X 数据", self.x_values_edit)
        xy_layout.addRow("Y 数据", self.y_values_edit)
        self.tabs.addTab(xy_page, "X/Y 快速输入")

        # 整块表格粘贴
        table_page = QWidget()
        table_layout = QVBoxLayout(table_page)
        self.header_check = QCheckBox("第一行是列名")
        self.header_check.setChecked(True)
        self.table_text = QPlainTextEdit()
        self.table_text.setPlaceholderText(
            "从 Excel 复制后直接粘贴，例如：\n"
            "Sample\tGroup\tValue\nA\tControl\t1.2\nB\tTreatment\t2.4\n\n"
            "也支持 CSV：\nSample,Group,Value\nA,Control,1.2"
        )
        table_layout.addWidget(self.header_check)
        table_layout.addWidget(self.table_text, 1)
        self.tabs.addTab(table_page, "表格文本 / Excel 粘贴")

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._parse)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    @staticmethod
    def _parse_values(text: str) -> list[str]:
        return [p for p in re.split(r"[\n,;，；\s]+", text.strip()) if p != ""]

    @staticmethod
    def _convert_columns(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="ignore")
        return df

    def _parse_xy(self) -> pd.DataFrame:
        x = self._parse_values(self.x_values_edit.toPlainText())
        y = self._parse_values(self.y_values_edit.toPlainText())
        if not x or not y:
            raise ValueError("X 和 Y 数据不能为空。")
        if len(x) != len(y):
            raise ValueError(f"X/Y 数量不一致：X={len(x)}，Y={len(y)}。")
        x_name = self.x_name_edit.text().strip() or "x"
        y_name = self.y_name_edit.text().strip() or "y"
        return self._convert_columns(pd.DataFrame({x_name: x, y_name: y}))

    def _parse_table(self) -> pd.DataFrame:
        text = self.table_text.toPlainText().strip()
        if not text:
            raise ValueError("表格文本不能为空。")
        header = 0 if self.header_check.isChecked() else None
        try:
            df = pd.read_csv(io.StringIO(text), sep=None, engine="python", header=header)
        except Exception:
            df = pd.read_csv(io.StringIO(text), sep="\t", header=header)
        if header is None:
            df.columns = [f"col_{i + 1}" for i in range(len(df.columns))]
        if df.empty:
            raise ValueError("没有解析出有效数据。")
        return self._convert_columns(df)

    def _parse(self) -> None:
        try:
            self.df = self._parse_xy() if self.tabs.currentIndex() == 0 else self._parse_table()
        except Exception as exc:
            QMessageBox.critical(self, "数据解析失败", str(exc))
            return
        self.accept()


class SkillContentDialog(QDialog):
    """只读查看 Skill 完整内容的弹窗。"""

    def __init__(self, name: str, body: str, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(f"技能详情：{name}")
        self.resize(720, 600)
        layout = QVBoxLayout(self)
        viewer = QPlainTextEdit()
        viewer.setReadOnly(True)
        viewer.setPlainText(body)
        viewer.setStyleSheet("font-family: 'JetBrains Mono','Consolas','Courier New',monospace; font-size: 13px;")
        layout.addWidget(viewer, 1)
        btn = QPushButton("关闭")
        btn.clicked.connect(self.accept)
        h = QHBoxLayout()
        h.addStretch(1)
        h.addWidget(btn)
        layout.addLayout(h)
