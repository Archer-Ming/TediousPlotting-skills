"""自定义控件：聊天输入框、聊天气泡、可折叠思考块、Skill 卡片。"""
from __future__ import annotations

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeyEvent, QPixmap
from PyQt5.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QSizePolicy,
    QTextEdit,
    QToolButton,
    QVBoxLayout,
    QWidget,
)


class ChatInput(QPlainTextEdit):
    """支持 Enter 发送 / Shift+Enter 换行。"""

    send_requested = pyqtSignal()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() in (Qt.Key_Return, Qt.Key_Enter) and not (event.modifiers() & Qt.ShiftModifier):
            self.send_requested.emit()
            return
        super().keyPressEvent(event)


class ChatBubble(QFrame):
    """单条消息气泡。role 决定颜色和对齐。"""

    def __init__(self, role: str, text: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.role = role
        self.setObjectName("UserBubble" if role == "user" else "AgentBubble")
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 9, 12, 9)
        layout.setSpacing(4)

        role_label = QLabel("你" if role == "user" else ("助手" if role == "assistant" else "系统"))
        role_label.setObjectName("BubbleRole")
        layout.addWidget(role_label)

        self.body = QLabel(text)
        self.body.setWordWrap(True)
        self.body.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(self.body)

    def append_text(self, more: str) -> None:
        self.body.setText(self.body.text() + more)


class CollapsibleThinking(QFrame):
    """折叠/展开的"思考过程"块，里面是若干步骤。"""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("ThinkingBlock")

        outer = QVBoxLayout(self)
        outer.setContentsMargins(10, 8, 10, 8)
        outer.setSpacing(4)

        self.toggle = QToolButton()
        self.toggle.setObjectName("ThinkingToggle")
        self.toggle.setText("▸ 思考过程")
        self.toggle.setCheckable(True)
        self.toggle.setChecked(False)
        self.toggle.setToolButtonStyle(Qt.ToolButtonTextOnly)
        self.toggle.clicked.connect(self._on_toggle)
        outer.addWidget(self.toggle, 0, Qt.AlignLeft)

        self.body = QWidget()
        self.body_layout = QVBoxLayout(self.body)
        self.body_layout.setContentsMargins(4, 2, 4, 2)
        self.body_layout.setSpacing(3)
        self.body.setVisible(False)
        outer.addWidget(self.body)

    def _on_toggle(self) -> None:
        opened = self.toggle.isChecked()
        self.toggle.setText(("▾ 思考过程" if opened else "▸ 思考过程"))
        self.body.setVisible(opened)

    def add_step(self, prefix: str, text: str) -> None:
        label = QLabel(f"<b>{prefix}</b> {text}")
        label.setObjectName("ThinkingStep")
        label.setWordWrap(True)
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.body_layout.addWidget(label)

    def add_code(self, code: str) -> None:
        viewer = QPlainTextEdit()
        viewer.setReadOnly(True)
        viewer.setPlainText(code)
        viewer.setObjectName("ThinkingCode")
        viewer.setMaximumHeight(180)
        self.body_layout.addWidget(viewer)


class SkillCard(QFrame):
    """左栏中的一张 Skill 卡片。"""

    toggled = pyqtSignal(str, bool)  # skill_id, enabled
    view_clicked = pyqtSignal(str)
    remove_clicked = pyqtSignal(str)

    def __init__(self, skill_id: str, name: str, description: str, enabled: bool, parent=None) -> None:
        super().__init__(parent)
        self.skill_id = skill_id
        self.setObjectName("SkillCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(6)

        top = QHBoxLayout()
        self.check = QCheckBox(name)
        self.check.setObjectName("SkillName")
        self.check.setChecked(enabled)
        self.check.toggled.connect(lambda ok: self.toggled.emit(self.skill_id, ok))
        top.addWidget(self.check, 1)

        view_btn = QToolButton()
        view_btn.setText("查看")
        view_btn.setObjectName("MiniLinkBtn")
        view_btn.clicked.connect(lambda: self.view_clicked.emit(self.skill_id))
        top.addWidget(view_btn)

        rm_btn = QToolButton()
        rm_btn.setText("移除")
        rm_btn.setObjectName("MiniLinkBtn")
        rm_btn.clicked.connect(lambda: self.remove_clicked.emit(self.skill_id))
        top.addWidget(rm_btn)
        layout.addLayout(top)

        if description:
            desc = QLabel(description)
            desc.setObjectName("SkillDesc")
            desc.setWordWrap(True)
            layout.addWidget(desc)


class ToolCard(QFrame):
    """工具卡片（占位：未来扩展用）。"""

    toggled = pyqtSignal(str, bool)

    def __init__(self, key: str, name: str, description: str, enabled: bool, available: bool, parent=None) -> None:
        super().__init__(parent)
        self.key = key
        self.setObjectName("ToolCard")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4)

        top = QHBoxLayout()
        self.check = QCheckBox(name)
        self.check.setObjectName("SkillName")
        self.check.setChecked(enabled and available)
        self.check.setEnabled(available)
        self.check.toggled.connect(lambda ok: self.toggled.emit(self.key, ok))
        top.addWidget(self.check, 1)

        if not available:
            tag = QLabel("即将推出")
            tag.setObjectName("ComingSoonTag")
            top.addWidget(tag)
        layout.addLayout(top)

        desc = QLabel(description)
        desc.setObjectName("SkillDesc")
        desc.setWordWrap(True)
        layout.addWidget(desc)


class SectionHeader(QLabel):
    """侧栏分区小标题。"""

    def __init__(self, text: str, parent=None) -> None:
        super().__init__(text, parent)
        self.setObjectName("SectionHeader")
