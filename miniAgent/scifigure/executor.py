"""子进程绘图沙箱。

- LLM 生成的代码以子进程方式执行，主进程不受 import / 死循环 / 内存爆炸的影响。
- 数据通过临时 pickle 文件传入；图像通过临时 PNG 文件回传。
- 通过 timeout 限制执行时长。
"""
from __future__ import annotations

import os
import pickle
import subprocess
import sys
import tempfile
import textwrap
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class ExecutionResult:
    success: bool
    image_path: str | None  # 渲染成功的 PNG 路径
    stdout: str
    stderr: str
    error_summary: str = ""  # 简短错误描述，便于 LLM 自我修复

    @property
    def short_error(self) -> str:
        if self.error_summary:
            return self.error_summary
        if self.stderr:
            lines = [ln for ln in self.stderr.strip().splitlines() if ln.strip()]
            return lines[-1] if lines else ""
        return ""


# 子进程执行入口的 Python 代码
_RUNNER_TEMPLATE = r"""
import os, sys, io, traceback, pickle, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
try:
    import seaborn as sns
except Exception:
    sns = None

# 中文字体兜底（不影响科研英文）
try:
    from matplotlib import rcParams
    rcParams['axes.unicode_minus'] = False
    # 优先使用 Times New Roman；若数据含中文，sans-serif 加上 SimHei/Microsoft YaHei
    rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
    rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'DejaVu Sans']
except Exception:
    pass

DATA_PATH = {data_path!r}
OUT_PATH = {out_path!r}
CODE_PATH = {code_path!r}

# 加载用户数据为 df
df = None
if DATA_PATH and os.path.exists(DATA_PATH):
    with open(DATA_PATH, "rb") as f:
        df = pickle.load(f)

# 拦截 plt.show 防止阻塞
def _noop_show(*a, **kw):
    return None
plt.show = _noop_show

with open(CODE_PATH, "r", encoding="utf-8") as f:
    user_code = f.read()

_globals = {{
    "__name__": "__main__",
    "df": df,
    "plt": plt,
    "np": np,
    "pd": pd,
    "sns": sns,
}}

try:
    exec(compile(user_code, "<agent_code>", "exec"), _globals)
    fig = plt.gcf()
    if fig is None or not fig.axes:
        # 用户没画任何东西
        figs = [plt.figure(n) for n in plt.get_fignums()]
        fig = figs[-1] if figs else None
    if fig is None:
        print("__AGENT_ERROR__:NO_FIGURE", file=sys.stderr)
        sys.exit(2)
    fig.savefig(OUT_PATH, dpi=200, bbox_inches="tight")
    print("__AGENT_OK__")
except Exception:
    traceback.print_exc()
    sys.exit(1)
"""


class CodeExecutor:
    def __init__(self, timeout: float = 30.0) -> None:
        self.timeout = timeout

    def run(self, code: str, df: pd.DataFrame | None) -> ExecutionResult:
        tmpdir = Path(tempfile.mkdtemp(prefix="scifig_"))
        data_path = tmpdir / "data.pkl"
        out_path = tmpdir / "figure.png"
        code_path = tmpdir / "user_code.py"

        try:
            if df is not None:
                with open(data_path, "wb") as f:
                    pickle.dump(df, f)
            else:
                # 占位空文件
                data_path = Path("")

            code_path.write_text(code, encoding="utf-8")

            runner = _RUNNER_TEMPLATE.format(
                data_path=str(data_path),
                out_path=str(out_path),
                code_path=str(code_path),
            )

            # 用当前解释器跑子进程，确保 numpy/matplotlib 等环境一致
            proc = subprocess.run(
                [sys.executable, "-c", runner],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                encoding="utf-8",
                errors="replace",
            )

            success = proc.returncode == 0 and out_path.exists()
            err_summary = ""
            if not success:
                if proc.returncode == 2:
                    err_summary = "代码执行未产出任何图像（请确认调用了 matplotlib 绘图）。"
                elif "__AGENT_ERROR__:NO_FIGURE" in proc.stderr:
                    err_summary = "代码未生成 Figure。"
                else:
                    # 提取最后一行 traceback 作为简要错误
                    lines = [ln for ln in proc.stderr.strip().splitlines() if ln.strip()]
                    err_summary = lines[-1] if lines else "未知错误"

            return ExecutionResult(
                success=success and out_path.exists(),
                image_path=str(out_path) if (success and out_path.exists()) else None,
                stdout=proc.stdout,
                stderr=proc.stderr,
                error_summary=err_summary,
            )
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                success=False,
                image_path=None,
                stdout="",
                stderr=f"执行超时（>{self.timeout}s）",
                error_summary=f"执行超时（超过 {self.timeout} 秒）",
            )
        except Exception as exc:
            return ExecutionResult(
                success=False,
                image_path=None,
                stdout="",
                stderr=str(exc),
                error_summary=str(exc),
            )
