"""SciFigure Agent Studio 全局样式。

设计基调：浅色玻璃感 / 圆角卡片 / 蓝紫渐变强调。聊天气泡区分 user/assistant。
2025-05 调整：整体字号上调一档以提升可读性。
"""

APP_QSS = """
QMainWindow, QWidget#RootBg {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
        stop:0 #EEF2FF, stop:0.45 #F5F7FF, stop:1 #ECF1FF);
}
QWidget {
    color: #1B2138;
    font-size: 14px;
}

/* ---- 顶栏 ---- */
QFrame#TopBar {
    background: rgba(255,255,255,0.86);
    border: 1px solid #E2E8F4;
    border-radius: 18px;
}
QLabel#AppTitle {
    color: #0F172A;
    font-size: 24px;
    font-weight: 900;
    letter-spacing: 0.3px;
}
QLabel#AppSubtitle {
    color: #64748B;
    font-size: 13px;
}
QLabel#ModelBadge {
    color: #4338CA;
    background: #EEF2FF;
    border: 1px solid #C7D2FE;
    border-radius: 10px;
    padding: 5px 12px;
    font-size: 13px;
    font-weight: 700;
}

/* ---- 三栏面板 ---- */
QFrame#LeftPanel, QFrame#CenterPanel, QFrame#RightPanel {
    background: rgba(255,255,255,0.96);
    border: 1px solid #E2E8F4;
    border-radius: 22px;
}

QLabel#SectionHeader {
    color: #312E81;
    font-size: 14px;
    font-weight: 800;
    letter-spacing: 0.4px;
    padding-top: 4px;
    padding-bottom: 2px;
}
QLabel#Subtle {
    color: #64748B;
    font-size: 13px;
}

/* ---- 通用按钮 ---- */
QPushButton {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #4F46E5, stop:1 #6366F1);
    border: none;
    border-radius: 12px;
    color: white;
    padding: 10px 16px;
    font-size: 14px;
    font-weight: 800;
}
QPushButton:hover { background: #4338CA; }
QPushButton:pressed { background: #3730A3; }
QPushButton:disabled { background: #CBD5E1; color: #F8FAFC; }
QPushButton#Secondary {
    background: #EEF2FF;
    color: #3730A3;
    border: 1px solid #C7D2FE;
}
QPushButton#Secondary:hover { background: #E0E7FF; }
QPushButton#Ghost {
    background: transparent;
    color: #4338CA;
    border: 1px dashed #C7D2FE;
}
QPushButton#Ghost:hover {
    background: #F5F3FF;
    border: 1px solid #C7D2FE;
}
QPushButton#Danger {
    background: #FEE2E2;
    color: #B91C1C;
    border: 1px solid #FECACA;
}
QPushButton#Danger:hover { background: #FECACA; }
QPushButton#Send {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #6366F1, stop:1 #8B5CF6);
    font-size: 15px;
    padding: 11px 22px;
}
QPushButton#Send:hover { background: #6D28D9; }

QToolButton#MiniLinkBtn {
    background: transparent;
    color: #4F46E5;
    border: none;
    padding: 3px 7px;
    font-size: 12px;
    font-weight: 700;
}
QToolButton#MiniLinkBtn:hover {
    color: #3730A3;
    text-decoration: underline;
}

/* ---- 表单控件 ---- */
QComboBox, QLineEdit, QSpinBox, QDoubleSpinBox {
    background: #FFFFFF;
    border: 1px solid #D8DEEC;
    border-radius: 10px;
    padding: 7px 12px;
    font-size: 14px;
    min-height: 24px;
}
QComboBox:focus, QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus,
QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #6366F1;
}
QTextEdit, QPlainTextEdit {
    background: #FFFFFF;
    border: 1px solid #E2E8F4;
    border-radius: 12px;
    padding: 11px;
    font-size: 14px;
    selection-background-color: #C7D2FE;
}
QCheckBox {
    spacing: 7px;
    font-size: 14px;
}
QCheckBox::indicator {
    width: 17px;
    height: 17px;
    border-radius: 4px;
    border: 1px solid #C7D2FE;
    background: #F8FAFC;
}
QCheckBox::indicator:checked {
    background: #6366F1;
    border: 1px solid #6366F1;
    image: none;
}

/* ---- Skill / Tool 卡片 ---- */
QFrame#SkillCard, QFrame#ToolCard {
    background: #FAFBFF;
    border: 1px solid #E0E7FF;
    border-radius: 14px;
}
QFrame#SkillCard:hover {
    border: 1px solid #A5B4FC;
    background: #F5F7FF;
}
QLabel#SkillName, QCheckBox#SkillName {
    font-size: 14px;
    font-weight: 800;
    color: #1E1B4B;
}
QLabel#SkillDesc {
    color: #64748B;
    font-size: 12px;
}
QLabel#ComingSoonTag {
    color: #92400E;
    background: #FEF3C7;
    border: 1px solid #FDE68A;
    border-radius: 8px;
    padding: 3px 9px;
    font-size: 11px;
    font-weight: 800;
}

/* ---- 聊天气泡 ---- */
QFrame#UserBubble {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #6366F1, stop:1 #8B5CF6);
    border: none;
    border-radius: 14px;
    color: white;
}
QFrame#UserBubble QLabel {
    color: white;
    font-size: 14px;
}
QFrame#UserBubble QLabel#BubbleRole {
    color: rgba(255,255,255,0.85);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.5px;
}
QFrame#AgentBubble {
    background: #FFFFFF;
    border: 1px solid #E0E7FF;
    border-radius: 14px;
}
QFrame#AgentBubble QLabel {
    font-size: 14px;
}
QFrame#AgentBubble QLabel#BubbleRole {
    color: #6366F1;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.5px;
}

/* ---- 思考过程 ---- */
QFrame#ThinkingBlock {
    background: #F8FAFF;
    border: 1px dashed #C7D2FE;
    border-radius: 12px;
}
QToolButton#ThinkingToggle {
    background: transparent;
    border: none;
    color: #4338CA;
    font-weight: 800;
    font-size: 12px;
    padding: 3px 5px;
}
QToolButton#ThinkingToggle:hover {
    color: #312E81;
}
QLabel#ThinkingStep {
    color: #475569;
    font-size: 13px;
}
QPlainTextEdit#ThinkingCode {
    background: #1E1B4B;
    color: #E0E7FF;
    border: none;
    border-radius: 10px;
    font-family: 'JetBrains Mono','Consolas','Courier New',monospace;
    font-size: 12px;
    padding: 9px;
}

/* ---- 中栏图像区 ---- */
QFrame#ImageStage {
    background: #FFFFFF;
    border: 1px solid #E2E8F4;
    border-radius: 18px;
}
QLabel#ImagePlaceholder {
    color: #94A3B8;
    font-size: 14px;
}
QLabel#ImageView {
    background: #FFFFFF;
    border-radius: 12px;
}

/* ---- TabWidget ---- */
QTabWidget::pane {
    border: 1px solid #E2E8F4;
    border-radius: 14px;
    background: #FFFFFF;
    top: -1px;
}
QTabBar::tab {
    background: #EEF2FF;
    color: #4338CA;
    padding: 8px 18px;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
    margin-right: 4px;
    font-size: 14px;
    font-weight: 700;
}
QTabBar::tab:selected {
    background: #FFFFFF;
    color: #1E1B4B;
}
QTabBar::tab:hover {
    background: #E0E7FF;
}

/* ---- 表格 ---- */
QTableView {
    gridline-color: #E2E8F0;
    alternate-background-color: #F8FAFF;
    selection-background-color: #C7D2FE;
    selection-color: #1E1B4B;
    border: none;
    font-size: 13px;
}
QHeaderView::section {
    background: #EEF2FF;
    color: #312E81;
    border: none;
    border-right: 1px solid #DDE3F5;
    border-bottom: 1px solid #DDE3F5;
    padding: 9px;
    font-size: 13px;
    font-weight: 800;
}

/* ---- 滚动条 ---- */
QScrollBar:vertical {
    background: transparent;
    width: 10px;
    margin: 4px 2px;
}
QScrollBar::handle:vertical {
    background: #C7D2FE;
    border-radius: 5px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: #A5B4FC;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
QScrollBar:horizontal {
    background: transparent;
    height: 10px;
    margin: 2px 4px;
}
QScrollBar::handle:horizontal {
    background: #C7D2FE;
    border-radius: 5px;
    min-width: 30px;
}

/* ---- 菜单 ---- */
QMenuBar {
    background: transparent;
    padding: 4px;
    font-size: 14px;
}
QMenuBar::item {
    padding: 7px 12px;
    border-radius: 8px;
}
QMenuBar::item:selected {
    background: #EEF2FF;
    color: #3730A3;
}
QMenu {
    background: #FFFFFF;
    border: 1px solid #E2E8F4;
    border-radius: 12px;
    padding: 6px;
    font-size: 14px;
}
QMenu::item {
    padding: 8px 24px 8px 14px;
    border-radius: 8px;
}
QMenu::item:selected {
    background: #EEF2FF;
    color: #3730A3;
}

QStatusBar {
    background: transparent;
    color: #64748B;
    font-size: 13px;
}
"""
