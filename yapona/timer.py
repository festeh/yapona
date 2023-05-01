"""
Pomodoro timer class
"""
from yapona.state import IdleState, RunningState


class Timer:

    def __init__(self, duration=60 * 20):
        self.state = IdleState()
        self.description = ""
        self.tags = []
        self.duration = duration

    def get_state_class(self):
        return self.state.__class__

    def start(self) -> bool:
        self.state = RunningState(self.duration)
        return True

    def interrupt(self) -> bool:
        self.state = IdleState()
        return True

    def update(self) -> bool:
        self.state.update()
        return True

    def is_done(self) -> bool:
        return self.state.is_done()

