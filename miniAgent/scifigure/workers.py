from __future__ import annotations

import traceback

import pandas as pd
from PyQt5.QtCore import QThread, pyqtSignal

from .agent import AgentStep, AgentTurn, PlottingAgent


class AgentChatWorker(QThread):
    """后台执行一次 Agent 对话，主线程只处理 UI 更新。"""

    step = pyqtSignal(object)        # AgentStep
    finished_ok = pyqtSignal(object)  # AgentTurn
    failed = pyqtSignal(str)

    def __init__(self, agent: PlottingAgent, user_message: str, df: pd.DataFrame | None) -> None:
        super().__init__()
        self.agent = agent
        self.user_message = user_message
        self.df = df.copy() if df is not None else None

    def run(self) -> None:
        try:
            def emit_step(s: AgentStep) -> None:
                self.step.emit(s)

            turn: AgentTurn = self.agent.chat(self.user_message, self.df, on_step=emit_step)
            self.finished_ok.emit(turn)
        except Exception:
            self.failed.emit(traceback.format_exc())
