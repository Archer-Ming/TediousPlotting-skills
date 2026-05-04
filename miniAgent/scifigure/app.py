"""SciFigure Agent Studio - 主窗口。

布局：
- 顶栏：标题 / 模型徽标 / 数据导入 / 导出 / 模型配置
- 左栏：Skills 管理 + Tools + LLM 状态 + 数据状态
- 中栏：可视化反馈区（图像 / 数据预览 / 历史代码三个 Tab）
- 右栏：Agent 对话区（消息流 + 输入框）
"""
from __future__ import annotations

import shutil
from pathlib import Path

import pandas as pd
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QGuiApplication, QIcon, QPixmap
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSplitter,
    QTabWidget,
    QTableView,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from .agent import AgentStep, AgentTurn, PlottingAgent
from .config import load_config
from .data_model import DataProject, PandasTableModel
from .dialogs import LLMConfigDialog, ManualDataDialog, SkillContentDialog
from .executor import CodeExecutor
from .skill_manager import SkillManager
from .styles import APP_QSS
from .widgets import ChatBubble, ChatInput, CollapsibleThinking, SectionHeader, SkillCard, ToolCard
from .workers import AgentChatWorker


APP_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILLS_DIR = APP_ROOT / "skills"
SKILLS_INDEX_PATH = APP_ROOT / "skills_index.json"
ASSETS_DIR = APP_ROOT / "assets"


class SciFigureStudio(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.config = load_config()
        self.project = DataProject()
        self.table_model = PandasTableModel()

        # 初始化 Skill 管理器
        self.skills = SkillManager(default_dir=DEFAULT_SKILLS_DIR)
        self.skills.set_index_path(SKILLS_INDEX_PATH)
        # 第一次启动若没有持久化记录，扫描默认目录
        if not self.skills.all_skills():
            self.skills.load_default_dir()

        self.executor = CodeExecutor(timeout=45.0)
        self.agent = PlottingAgent(self.config, self.skills, self.executor)

        self.worker: AgentChatWorker | None = None
        self.current_thinking: CollapsibleThinking | None = None
        self.last_image_path: str | None = None
        self.last_code: str = ""
        self.history_images: list[str] = []  # 历次成功生成的图像，可在历史面板浏览
        self.history_codes: list[str] = []

        self._init_window()
        self._build_ui()
        self._build_menu()
        self._refresh_skills_panel()
        self._refresh_data_status()
        self._update_model_badge()
        self._post_system("欢迎使用 SciFigure Agent Studio。请先在左下角配置大模型，然后导入数据并在右侧对话框描述你的绘图需求。")

    # ====================================================================
    # 初始化
    # ====================================================================
    def _init_window(self) -> None:
        self.setWindowTitle("SciFigure Agent Studio · 智能科研绘图工作台")
        self.setObjectName("RootBg")
        icon_path = ASSETS_DIR / "pixel_style.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        self.resize(1620, 980)
        self.setStyleSheet(APP_QSS)

    def _build_menu(self) -> None:
        m_file = self.menuBar().addMenu("文件")
        for label, slot in (
            ("打开数据文件", self.on_open_data),
            ("从剪贴板读取", self.on_load_clipboard),
            ("手动输入数据", self.on_manual_data),
            ("导出当前图像", self.on_export_figure),
        ):
            act = QAction(label, self)
            act.triggered.connect(slot)
            m_file.addAction(act)

        m_skill = self.menuBar().addMenu("技能")
        add_skill_act = QAction("添加 Skill 文件…", self)
        add_skill_act.triggered.connect(self.on_add_skill)
        m_skill.addAction(add_skill_act)
        scan_act = QAction("重新扫描内置 skills/", self)
        scan_act.triggered.connect(self.on_rescan_skills)
        m_skill.addAction(scan_act)

        m_settings = self.menuBar().addMenu("设置")
        cfg_act = QAction("大模型配置", self)
        cfg_act.triggered.connect(self.on_open_model_config)
        m_settings.addAction(cfg_act)
        reset_chat_act = QAction("清空对话历史", self)
        reset_chat_act.triggered.connect(self.on_reset_chat)
        m_settings.addAction(reset_chat_act)

    def _build_ui(self) -> None:
        root = QWidget()
        root.setObjectName("RootBg")
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(14, 14, 14, 14)
        root_layout.setSpacing(12)
        self.setCentralWidget(root)

        root_layout.addWidget(self._build_top_bar())

        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(8)
        splitter.addWidget(self._build_left_panel())
        splitter.addWidget(self._build_center_panel())
        splitter.addWidget(self._build_right_panel())
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setStretchFactor(2, 0)
        splitter.setSizes([320, 760, 460])
        root_layout.addWidget(splitter, 1)

    # ====================================================================
    # 顶栏
    # ====================================================================
    def _build_top_bar(self) -> QWidget:
        bar = QFrame()
        bar.setObjectName("TopBar")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(20, 12, 20, 12)
        layout.setSpacing(14)

        # logo + 标题
        title_box = QVBoxLayout()
        title_box.setSpacing(0)
        title = QLabel("SciFigure Agent Studio")
        title.setObjectName("AppTitle")
        sub = QLabel("Skill 驱动 · 智能体绘图 · 自然语言迭代")
        sub.setObjectName("AppSubtitle")
        title_box.addWidget(title)
        title_box.addWidget(sub)
        layout.addLayout(title_box)
        layout.addStretch(1)

        # 模型徽标
        self.model_badge = QLabel("模型未配置")
        self.model_badge.setObjectName("ModelBadge")
        layout.addWidget(self.model_badge)

        # 操作按钮
        import_btn = QPushButton("📂 导入数据")
        import_btn.setObjectName("Secondary")
        import_btn.clicked.connect(self.on_open_data)
        layout.addWidget(import_btn)

        export_btn = QPushButton("📤 导出图像")
        export_btn.setObjectName("Secondary")
        export_btn.clicked.connect(self.on_export_figure)
        layout.addWidget(export_btn)

        cfg_btn = QPushButton("⚙️ 模型配置")
        cfg_btn.clicked.connect(self.on_open_model_config)
        layout.addWidget(cfg_btn)
        return bar

    # ====================================================================
    # 左栏：Agent 配置（Skills / Tools / LLM / Data）
    # ====================================================================
    def _build_left_panel(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("LeftPanel")
        outer = QVBoxLayout(panel)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # 顶部固定标题
        header = QLabel("Agent 配置")
        header.setStyleSheet("color:#1E1B4B; font-size:18px; font-weight:900; padding:14px 16px 4px 16px;")
        outer.addWidget(header)
        sub = QLabel("管理智能体使用的技能、工具、模型与数据")
        sub.setObjectName("Subtle")
        sub.setStyleSheet("padding:0 16px 8px 16px;")
        sub.setWordWrap(True)
        outer.addWidget(sub)

        # 滚动区域承载所有分区
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        outer.addWidget(scroll, 1)

        body = QWidget()
        scroll.setWidget(body)
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(14, 6, 14, 14)
        body_layout.setSpacing(14)

        # ---- Skills 分区 ----
        body_layout.addWidget(SectionHeader("📦 SKILLS · 专业技能"))
        self.skill_list_holder = QWidget()
        self.skill_list_layout = QVBoxLayout(self.skill_list_holder)
        self.skill_list_layout.setContentsMargins(0, 0, 0, 0)
        self.skill_list_layout.setSpacing(8)
        body_layout.addWidget(self.skill_list_holder)

        add_skill_btn = QPushButton("＋ 添加 Skill 文件…")
        add_skill_btn.setObjectName("Ghost")
        add_skill_btn.clicked.connect(self.on_add_skill)
        body_layout.addWidget(add_skill_btn)

        # ---- Tools 分区 ----
        body_layout.addWidget(SectionHeader("🛠️ TOOLS · 工具"))
        # 现版本只有一个内置工具：代码执行（沙箱）。其它是占位
        tool_box = QVBoxLayout()
        tool_box.setSpacing(8)
        tool_box.addWidget(ToolCard(
            "code_exec", "Matplotlib 沙箱执行器",
            "在隔离的子进程中安全执行 Agent 生成的绘图代码。", True, True))
        tool_box.addWidget(ToolCard(
            "data_query", "数据查询（即将推出）",
            "支持 Agent 反查 df 字段统计、分组聚合等。", False, False))
        tool_box.addWidget(ToolCard(
            "image_export", "图像导出（即将推出）",
            "Agent 自主导出 PNG/SVG/PDF 多格式。", False, False))
        body_layout.addLayout(tool_box)

        # ---- LLM 分区 ----
        body_layout.addWidget(SectionHeader("🧠 LLM · 大模型"))
        self.llm_status_label = QLabel("未配置")
        self.llm_status_label.setObjectName("Subtle")
        self.llm_status_label.setWordWrap(True)
        body_layout.addWidget(self.llm_status_label)
        llm_btn = QPushButton("⚙️ 修改模型配置")
        llm_btn.setObjectName("Secondary")
        llm_btn.clicked.connect(self.on_open_model_config)
        body_layout.addWidget(llm_btn)

        # ---- 数据分区 ----
        body_layout.addWidget(SectionHeader("📁 DATA · 数据"))
        self.data_status_label = QLabel("未加载数据")
        self.data_status_label.setObjectName("Subtle")
        self.data_status_label.setWordWrap(True)
        body_layout.addWidget(self.data_status_label)

        data_btns = QVBoxLayout()
        data_btns.setSpacing(6)
        b1 = QPushButton("📂 导入文件")
        b1.setObjectName("Secondary")
        b1.clicked.connect(self.on_open_data)
        data_btns.addWidget(b1)
        b2 = QPushButton("📋 从剪贴板")
        b2.setObjectName("Secondary")
        b2.clicked.connect(self.on_load_clipboard)
        data_btns.addWidget(b2)
        b3 = QPushButton("✍️ 手动录入")
        b3.setObjectName("Secondary")
        b3.clicked.connect(self.on_manual_data)
        data_btns.addWidget(b3)
        body_layout.addLayout(data_btns)

        body_layout.addStretch(1)
        return panel

    def _refresh_skills_panel(self) -> None:
        """重建左栏 Skills 列表。"""
        # 清空
        while self.skill_list_layout.count():
            item = self.skill_list_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        skills = self.skills.all_skills()
        if not skills:
            empty = QLabel("尚未加载任何 Skill。\n点击下方“添加 Skill 文件”来加载 .md 技能文件。")
            empty.setObjectName("Subtle")
            empty.setWordWrap(True)
            self.skill_list_layout.addWidget(empty)
            return

        for sk in skills:
            card = SkillCard(sk.skill_id, sk.name, sk.description, sk.enabled)
            card.toggled.connect(self._on_skill_toggled)
            card.view_clicked.connect(self._on_skill_view)
            card.remove_clicked.connect(self._on_skill_remove)
            self.skill_list_layout.addWidget(card)

    def _refresh_data_status(self) -> None:
        if not self.project.loaded:
            self.data_status_label.setText("未加载数据")
            return
        df = self.project.df
        self.data_status_label.setText(
            f"<b>{self.project.name}</b><br>"
            f"<span style='color:#64748B'>{len(df)} 行 × {len(df.columns)} 列</span>"
        )

    def _update_model_badge(self) -> None:
        if not self.config.api_key:
            self.model_badge.setText("⚠️ 未配置模型")
            self.model_badge.setStyleSheet(
                "color:#92400E; background:#FEF3C7; border:1px solid #FDE68A;"
                "border-radius:10px; padding:4px 10px; font-weight:700;"
            )
            self.llm_status_label.setText("尚未配置 API Key。请点击下方按钮设置。")
        else:
            self.model_badge.setText(f"🧠 {self.config.model}")
            self.model_badge.setStyleSheet("")  # 走默认 QSS
            self.llm_status_label.setText(
                f"<b>模型：</b>{self.config.model}<br>"
                f"<span style='color:#64748B'>Base：{self.config.base_url}</span>"
            )

    # ====================================================================
    # 中栏：可视化反馈
    # ====================================================================
    def _build_center_panel(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("CenterPanel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        head = QHBoxLayout()
        title = QLabel("可视化反馈")
        title.setStyleSheet("color:#1E1B4B; font-size:18px; font-weight:900;")
        head.addWidget(title)
        head.addStretch(1)
        self.image_meta_label = QLabel("等待 Agent 产出图像…")
        self.image_meta_label.setObjectName("Subtle")
        head.addWidget(self.image_meta_label)
        layout.addLayout(head)

        self.center_tabs = QTabWidget()
        layout.addWidget(self.center_tabs, 1)

        # ---- Tab 1: 当前图像 ----
        self.image_stage = QFrame()
        self.image_stage.setObjectName("ImageStage")
        stage_layout = QVBoxLayout(self.image_stage)
        stage_layout.setContentsMargins(12, 12, 12, 12)
        stage_layout.setSpacing(8)

        self.image_scroll = QScrollArea()
        self.image_scroll.setWidgetResizable(True)
        self.image_scroll.setAlignment(Qt.AlignCenter)
        self.image_scroll.setFrameShape(QScrollArea.NoFrame)
        self.image_label = QLabel()
        self.image_label.setObjectName("ImagePlaceholder")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setText(
            "🎨 还没有图像。\n\n请在右侧对话框告诉 Agent 你想画什么。\n"
            "例如：\n• 用 df 画各组的箱线图\n• 把上一张图改成 Nature 风格\n• 给柱状图加误差棒"
        )
        self.image_scroll.setWidget(self.image_label)
        stage_layout.addWidget(self.image_scroll, 1)

        # 底部操作栏
        ops = QHBoxLayout()
        self.prev_btn = QPushButton("◀ 上一张")
        self.prev_btn.setObjectName("Secondary")
        self.prev_btn.clicked.connect(self._on_prev_image)
        self.next_btn = QPushButton("下一张 ▶")
        self.next_btn.setObjectName("Secondary")
        self.next_btn.clicked.connect(self._on_next_image)
        self.image_index_label = QLabel("—")
        self.image_index_label.setObjectName("Subtle")
        export_btn = QPushButton("💾 导出当前")
        export_btn.setObjectName("Secondary")
        export_btn.clicked.connect(self.on_export_figure)
        ops.addWidget(self.prev_btn)
        ops.addWidget(self.image_index_label)
        ops.addWidget(self.next_btn)
        ops.addStretch(1)
        ops.addWidget(export_btn)
        stage_layout.addLayout(ops)

        self._current_image_idx: int = -1

        self.center_tabs.addTab(self.image_stage, "图像")

        # ---- Tab 2: 数据预览 ----
        data_page = QWidget()
        dl = QVBoxLayout(data_page)
        dl.setContentsMargins(8, 8, 8, 8)
        self.table_view = QTableView()
        self.table_view.setModel(self.table_model)
        self.table_view.setAlternatingRowColors(True)
        dl.addWidget(self.table_view)
        self.center_tabs.addTab(data_page, "数据预览")

        # ---- Tab 3: 复现代码 ----
        code_page = QWidget()
        cl = QVBoxLayout(code_page)
        cl.setContentsMargins(8, 8, 8, 8)
        self.code_view = QPlainTextEdit()
        self.code_view.setPlaceholderText("Agent 生成的最近一段绘图代码会显示在这里，可复制到本地复现。")
        self.code_view.setReadOnly(False)
        cl.addWidget(self.code_view, 1)
        copy = QPushButton("📋 复制代码")
        copy.setObjectName("Secondary")
        copy.clicked.connect(self._on_copy_code)
        cl.addWidget(copy)
        self.center_tabs.addTab(code_page, "代码")

        return panel

    def _show_image(self, path: str) -> None:
        if not path or not Path(path).exists():
            return
        pix = QPixmap(path)
        # 限制最大显示宽度，避免大图把布局撑爆
        max_w = max(self.image_scroll.viewport().width() - 24, 600)
        if pix.width() > max_w:
            pix = pix.scaledToWidth(max_w, Qt.SmoothTransformation)
        self.image_label.setPixmap(pix)
        self.image_label.setText("")
        self.image_label.setObjectName("ImageView")
        self.image_label.setStyleSheet("")  # 让 QSS 重新匹配
        self.center_tabs.setCurrentIndex(0)

    def _on_prev_image(self) -> None:
        if not self.history_images:
            return
        self._current_image_idx = max(0, self._current_image_idx - 1)
        self._show_image(self.history_images[self._current_image_idx])
        self._update_history_nav()

    def _on_next_image(self) -> None:
        if not self.history_images:
            return
        self._current_image_idx = min(len(self.history_images) - 1, self._current_image_idx + 1)
        self._show_image(self.history_images[self._current_image_idx])
        self._update_history_nav()

    def _update_history_nav(self) -> None:
        if not self.history_images:
            self.image_index_label.setText("—")
            self.prev_btn.setEnabled(False)
            self.next_btn.setEnabled(False)
            return
        self.image_index_label.setText(f"{self._current_image_idx + 1} / {len(self.history_images)}")
        self.prev_btn.setEnabled(self._current_image_idx > 0)
        self.next_btn.setEnabled(self._current_image_idx < len(self.history_images) - 1)

    def _on_copy_code(self) -> None:
        QGuiApplication.clipboard().setText(self.code_view.toPlainText())
        self.statusBar().showMessage("代码已复制", 2500)

    # ====================================================================
    # 右栏：对话区
    # ====================================================================
    def _build_right_panel(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("RightPanel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 12)
        layout.setSpacing(8)

        head = QHBoxLayout()
        title = QLabel("🤖 Agent 对话")
        title.setStyleSheet("color:#1E1B4B; font-size:18px; font-weight:900;")
        head.addWidget(title)
        head.addStretch(1)
        clear_btn = QToolButton()
        clear_btn.setText("清空")
        clear_btn.setObjectName("MiniLinkBtn")
        clear_btn.clicked.connect(self.on_reset_chat)
        head.addWidget(clear_btn)
        layout.addLayout(head)

        # 消息流（滚动）
        self.chat_scroll = QScrollArea()
        self.chat_scroll.setWidgetResizable(True)
        self.chat_scroll.setFrameShape(QScrollArea.NoFrame)
        self.chat_container = QWidget()
        self.chat_container.setStyleSheet("background: transparent;")
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setContentsMargins(2, 2, 2, 2)
        self.chat_layout.setSpacing(10)
        self.chat_layout.addStretch(1)  # 让消息从顶部往下排
        self.chat_scroll.setWidget(self.chat_container)
        layout.addWidget(self.chat_scroll, 1)

        # 输入区
        input_card = QFrame()
        input_card.setStyleSheet(
            "QFrame { background:#FFFFFF; border:1px solid #E0E7FF; border-radius:14px; }"
        )
        il = QVBoxLayout(input_card)
        il.setContentsMargins(8, 8, 8, 8)
        il.setSpacing(6)

        self.chat_input = ChatInput()
        self.chat_input.setPlaceholderText(
            "和 Agent 描述你的绘图需求，Enter 发送 / Shift+Enter 换行。\n"
            "例如：用 df 画各组冲击强度的小提琴+箱线图，标题用中文。"
        )
        self.chat_input.setMaximumHeight(110)
        self.chat_input.send_requested.connect(self.on_send_chat)
        il.addWidget(self.chat_input)

        send_row = QHBoxLayout()
        send_row.addStretch(1)
        self.send_btn = QPushButton("发送")
        self.send_btn.setObjectName("Send")
        self.send_btn.clicked.connect(self.on_send_chat)
        send_row.addWidget(self.send_btn)
        il.addLayout(send_row)

        layout.addWidget(input_card)
        return panel

    # ---------- 聊天插入辅助 ----------
    def _add_chat_widget(self, widget: QWidget, align_right: bool = False) -> None:
        # 在 stretch 之前插入
        idx = self.chat_layout.count() - 1
        if align_right:
            row = QHBoxLayout()
            row.addStretch(1)
            row.addWidget(widget)
            wrap = QWidget()
            wrap.setStyleSheet("background:transparent;")
            wrap.setLayout(row)
            self.chat_layout.insertWidget(idx, wrap)
        else:
            self.chat_layout.insertWidget(idx, widget)
        # 滚到底
        QApplication.processEvents()
        bar = self.chat_scroll.verticalScrollBar()
        bar.setValue(bar.maximum())

    def _add_user_message(self, text: str) -> None:
        bubble = ChatBubble("user", text)
        bubble.setMaximumWidth(380)
        self._add_chat_widget(bubble, align_right=True)

    def _add_agent_message(self, text: str) -> ChatBubble:
        bubble = ChatBubble("assistant", text)
        bubble.setMaximumWidth(420)
        self._add_chat_widget(bubble, align_right=False)
        return bubble

    def _add_system_message(self, text: str) -> None:
        label = QLabel(text)
        label.setObjectName("Subtle")
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color:#94A3B8; font-size:12px; padding:2px 16px;")
        self._add_chat_widget(label, align_right=False)

    def _post_system(self, text: str) -> None:
        self._add_system_message(text)

    def _start_thinking(self) -> CollapsibleThinking:
        block = CollapsibleThinking()
        self._add_chat_widget(block, align_right=False)
        return block

    # ====================================================================
    # 事件 - Skills
    # ====================================================================
    def _on_skill_toggled(self, skill_id: str, enabled: bool) -> None:
        self.skills.set_enabled(skill_id, enabled)
        self._post_system(f"技能已{'启用' if enabled else '禁用'}。")

    def _on_skill_view(self, skill_id: str) -> None:
        for sk in self.skills.all_skills():
            if sk.skill_id == skill_id:
                dlg = SkillContentDialog(sk.name, sk.body, self)
                dlg.exec_()
                break

    def _on_skill_remove(self, skill_id: str) -> None:
        ans = QMessageBox.question(self, "移除技能", "确定要从列表中移除该技能吗？\n（不会删除磁盘文件）")
        if ans != QMessageBox.Yes:
            return
        self.skills.remove(skill_id)
        self._refresh_skills_panel()

    def on_add_skill(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "选择 Skill 文件", "", "Markdown / 文本 (*.md *.markdown *.txt);;所有文件 (*.*)"
        )
        if not path:
            return
        try:
            sk = self.skills.load_from_file(Path(path))
            self._refresh_skills_panel()
            self._post_system(f"已加载技能：{sk.name}")
        except Exception as exc:
            QMessageBox.critical(self, "加载失败", str(exc))

    def on_rescan_skills(self) -> None:
        before = len(self.skills.all_skills())
        self.skills.load_default_dir()
        after = len(self.skills.all_skills())
        self._refresh_skills_panel()
        self._post_system(f"已扫描内置 skills/ 目录。新增 {max(0, after - before)} 个技能。")

    # ====================================================================
    # 事件 - 数据
    # ====================================================================
    def on_open_data(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "选择数据文件", "",
            "数据文件 (*.csv *.txt *.xlsx *.xls *.parquet *.json);;所有文件 (*.*)",
        )
        if not path:
            return
        try:
            df = self.project.load(path)
            self._after_data_loaded(df)
        except Exception as exc:
            QMessageBox.critical(self, "导入失败", str(exc))

    def on_load_clipboard(self) -> None:
        try:
            df = self.project.load_clipboard()
            self._after_data_loaded(df)
        except Exception as exc:
            QMessageBox.critical(self, "剪贴板读取失败", str(exc))

    def on_manual_data(self) -> None:
        dlg = ManualDataDialog(self)
        if dlg.exec_() == dlg.Accepted and dlg.df is not None:
            try:
                df = self.project.load_dataframe(dlg.df, name="手动输入数据")
                self._after_data_loaded(df)
            except Exception as exc:
                QMessageBox.critical(self, "数据导入失败", str(exc))

    def _after_data_loaded(self, df: pd.DataFrame) -> None:
        self.table_model.set_dataframe(df)
        self._refresh_data_status()
        self.center_tabs.setCurrentIndex(1)
        self._post_system(
            f"已加载 “{self.project.name}”，共 {len(df)} 行 × {len(df.columns)} 列。"
            f"现在可以在右侧让 Agent 帮你绘图。"
        )

    # ====================================================================
    # 事件 - 模型配置
    # ====================================================================
    def on_open_model_config(self) -> None:
        dlg = LLMConfigDialog(self.config, self)
        if dlg.exec_() == dlg.Accepted and dlg.saved_config is not None:
            self.config = load_config()
            self.agent.update_config(self.config)
            self._update_model_badge()
            self._post_system("大模型配置已保存。")

    def on_reset_chat(self) -> None:
        # 清空 UI 列表
        while self.chat_layout.count() > 1:  # 保留最后那个 stretch
            item = self.chat_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()
        self.agent.reset_history()
        self._post_system("对话历史已清空。")

    # ====================================================================
    # 事件 - 发送对话
    # ====================================================================
    def on_send_chat(self) -> None:
        text = self.chat_input.toPlainText().strip()
        if not text:
            return
        if not self.config.api_key:
            QMessageBox.warning(self, "未配置模型", "请先点击右上角“⚙️ 模型配置”填写 API Key。")
            return
        if self.worker is not None and self.worker.isRunning():
            QMessageBox.information(self, "正在处理", "请等待上一次对话完成。")
            return

        self.chat_input.clear()
        self._add_user_message(text)
        # 新建一个折叠思考块用来挂载本轮的 step
        self.current_thinking = self._start_thinking()

        df = self.project.df if self.project.loaded else None
        self.send_btn.setEnabled(False)
        self.send_btn.setText("生成中…")
        self.statusBar().showMessage("Agent 正在思考…")

        self.worker = AgentChatWorker(self.agent, text, df)
        self.worker.step.connect(self._on_agent_step)
        self.worker.finished_ok.connect(self._on_agent_done)
        self.worker.failed.connect(self._on_agent_failed)
        self.worker.start()

    def _on_agent_step(self, step: AgentStep) -> None:
        if self.current_thinking is None:
            self.current_thinking = self._start_thinking()
        if step.kind == "thinking":
            self.current_thinking.add_step("💭 思考：", step.text)
        elif step.kind == "code":
            self.current_thinking.add_step("⚙️ 生成代码：", "（点击展开查看）")
            self.current_thinking.add_code(step.code)
        elif step.kind == "exec_ok":
            self.current_thinking.add_step("✅ 渲染成功", step.text)
            if step.image_path:
                self.history_images.append(step.image_path)
                self.history_codes.append(step.code or "")
                self._current_image_idx = len(self.history_images) - 1
                self.last_image_path = step.image_path
                self.last_code = step.code or ""
                self._show_image(step.image_path)
                self.code_view.setPlainText(step.code or "")
                self.image_meta_label.setText(f"已生成 {len(self.history_images)} 张图")
                self._update_history_nav()
        elif step.kind == "exec_fail":
            self.current_thinking.add_step("❌ 失败：", step.text)
        elif step.kind == "answer":
            # 直接回答类的步骤暂不在这里展示，等 finished_ok 显示气泡
            pass
        elif step.kind == "error":
            self.current_thinking.add_step("⚠️ 错误：", step.text)
        # 滚到底
        bar = self.chat_scroll.verticalScrollBar()
        bar.setValue(bar.maximum())

    def _on_agent_done(self, turn: AgentTurn) -> None:
        if turn.final_message:
            self._add_agent_message(turn.final_message)
        self.send_btn.setEnabled(True)
        self.send_btn.setText("发送")
        self.statusBar().showMessage("就绪", 2000)
        self.worker = None
        self.current_thinking = None

    def _on_agent_failed(self, detail: str) -> None:
        last = (detail or "未知错误").strip().splitlines()
        msg = last[-1] if last else "Agent 出错"
        self._add_agent_message(f"出错：{msg}")
        self.send_btn.setEnabled(True)
        self.send_btn.setText("发送")
        self.statusBar().showMessage("出错", 3000)
        self.worker = None
        self.current_thinking = None

    # ====================================================================
    # 导出
    # ====================================================================
    def on_export_figure(self) -> None:
        if not self.last_image_path or not Path(self.last_image_path).exists():
            # 看一下是不是当前历史里有
            if 0 <= self._current_image_idx < len(self.history_images):
                src = self.history_images[self._current_image_idx]
            else:
                QMessageBox.information(self, "无可导出", "尚未生成任何图像。")
                return
        else:
            src = self.last_image_path
        path, _ = QFileDialog.getSaveFileName(
            self, "导出图像", "figure.png",
            "PNG (*.png);;SVG (*.svg);;PDF (*.pdf)"
        )
        if not path:
            return
        try:
            shutil.copyfile(src, path)
            self._post_system(f"已导出：{path}")
        except Exception as exc:
            QMessageBox.critical(self, "导出失败", str(exc))
