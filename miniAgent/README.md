# SciFigure Agent Studio 3.0

> Skill 驱动的智能体科研绘图工作台 —— 加载 SKILL.md → 自然语言对话 → Agent 安全沙箱出图。

## 与旧版 (2.x) 的区别

| | 2.x（ChartSpec 模式） | 3.0（Agent 模式） |
|---|---|---|
| 工作流 | LLM → 结构化 ChartSpec → 本地引擎渲染 | Skill 注入 + LLM 直出 matplotlib 代码 → 沙箱执行 |
| 图表类型 | 固定 9 种 | 任意（由 Skill 模板和 LLM 决定） |
| 风格定制 | 参数面板 + 样式设计器 | 通过对话迭代："改成 Nature 风格"、"加误差棒" |
| 扩展能力 | 改 charting.py 源码 | 加一份 .md 技能文件 |

## 三栏布局

```
┌────────────────┬─────────────────────────┬─────────────────┐
│ 左：Agent 配置  │   中：可视化反馈          │ 右：Agent 对话   │
│                │                          │                 │
│ 📦 Skills      │  当前图像 / 数据 / 代码    │ 💬 用户气泡     │
│ 🛠️ Tools       │  ◀ 1/N ▶ 💾 导出         │ 🤖 Agent 气泡    │
│ 🧠 LLM 状态    │                          │ ▸ 思考过程       │
│ 📁 数据状态     │                          │ [输入] [发送]   │
└────────────────┴─────────────────────────┴─────────────────┘
```

## 快速开始

### 1. 启动

Windows：双击 `启动软件.bat`

或者手动：

```bash
python -m venv .venv
.venv\Scripts\activate     # Windows
source .venv/bin/activate  # macOS / Linux
pip install -r requirements.txt
python main.py
```

### 2. 配置大模型

打开右上角 **⚙️ 模型配置**，填入：

- OpenAI: `https://api.openai.com/v1` + `gpt-4.1-mini` + your key
- DeepSeek: `https://api.deepseek.com` + `deepseek-chat` + your key
- 任意 OpenAI 兼容代理

### 3. 加载 Skill

`skills/` 目录已经预置了 `professional_plotting.md`（你提供的科研绘图技能）。

启动后会自动扫描该目录。要追加更多技能：

- 点击左栏 **＋ 添加 Skill 文件…** 选择本机任意路径的 .md
- 或者把 .md 直接丢进 `skills/`，菜单选 **技能 → 重新扫描**

每个 Skill 卡片可以**勾选启停**，仅启用的 Skill 会被注入 LLM 上下文。

### 4. 导入数据

左栏底部 **导入文件 / 剪贴板 / 手动录入** 三选一。Agent 启动时会自动看到当前 `df`。

### 5. 对话绘图

在右栏输入框（Enter 发送，Shift+Enter 换行）：

```
帮我画一张柱状图，比较 Method 列的不同方法在三个 Direction 下的 R²，加图例。
```

```
把上面那张图改成箱线图叠加小提琴图。
```

```
给柱子加上数值标签，标题改成中文：模型对比。
```

Agent 会：

1. 读取你启用的 Skill（模板代码、配色、字体规则）
2. 生成完整 matplotlib 代码
3. 在子进程沙箱里执行
4. 失败会自动重试修复（最多 2 次）
5. 成功的图渲染到中栏，代码同步到「代码」Tab

## 安全模型

所有 LLM 生成的代码在**独立子进程**里运行：

- 主程序进程不受其 import / 死循环影响
- 可设置超时（默认 45 秒）
- 数据通过临时 pickle 传入，图通过临时 PNG 传出
- 子进程结束后临时目录可被清理

> 注意：子进程隔离能防止程序崩溃和死锁，但**不能阻止恶意代码读写文件系统或调用网络**。如果你担心这一点，可以在 OS 层加一层 sandbox（Linux 上用 firejail / Windows 上用 AppContainer）。

## 目录结构

```
scifigure_agent/
  main.py
  requirements.txt
  启动软件.bat
  .env.example
  skills/
    professional_plotting.md      # 你提供的科研绘图技能
  scifigure/
    app.py                # 主 UI（三栏布局）
    agent.py              # Agent 大脑（多轮对话、Skill 注入、自我修复）
    skill_manager.py      # Skill 加载/启停/持久化
    executor.py           # 子进程沙箱
    workers.py            # QThread 后台 worker
    widgets.py            # 聊天气泡、思考块、Skill 卡片等
    dialogs.py            # 模型配置 / 手动数据录入 / 技能查看
    data_model.py         # 数据导入与字段画像
    config.py             # .env 读写
    styles.py             # 全局 QSS
```

## 写一个新的 Skill

任何符合下面格式的 .md 都能被加载（YAML frontmatter 可省略 description）：

```markdown
---
name: 我的箱线图技能
description: 专门处理冲击实验三方向数据的箱线图绘制规范
---

### 配色规范
颜色固定使用：
\`\`\`python
palette = {"Upright": "#2E86AB", "Side": "#A23B72", "Flat": "#F18F01"}
\`\`\`

### 模板代码
（粘贴你的模板）
\`\`\`python
fig, ax = plt.subplots(figsize=(10, 5))
sns.violinplot(data=plot_df, x='Direction', y='Value', palette=palette)
...
\`\`\`

### 注意事项
- 三方向必须按 Upright/Side/Flat 顺序
- ...
```

整份 .md 会作为 system prompt 的一部分被注入，Agent 会"读懂"模板并据此绘图。

## 已知限制

- 当前内置工具仅有「沙箱执行器」一个；后续可在左栏 Tools 区扩展数据查询、自动导出等。
- Agent 一次对话只画一张图；想要"批量画 N 张"目前需要分多轮对话。
- 子进程冷启动约 0.5–1 秒，复杂图整体响应在 5–15 秒之间，取决于模型延迟。
