from typing_extensions import override
from yapona.hook import Hook
from yapona.state import IdleState, RunningState
from yapona import utils
from datetime import datetime
import json
import os


def form_event(event, state):
    data = {
        "event": event,
        "id": state.id,
        "time": datetime.now().strftime("%H:%M:%S %d-%m-%Y")
    }
    return json.dumps(data) + "\n"


class HistoryHook(Hook):

    def __init__(self) -> None:
        xdg_data_home = os.environ.get("XDG_DATA_HOME",
                                       os.path.expanduser("~/.local/share"))
        self.file_path = os.path.join(xdg_data_home, utils.kAppName, "history.jsonl")
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    @override
    def on_start(self, state: IdleState):
        with open(self.file_path, "a") as f:
            f.write(form_event("start", state))

    @override
    def on_interrupt(self, state: RunningState):
        with open(self.file_path, "a") as f:
            f.write(form_event("cancel", state))

    @override
    def on_done(self, state: RunningState):
        with open(self.file_path, "a") as f:
            f.write(form_event("complete", state))
