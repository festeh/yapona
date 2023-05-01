from typing import cast
from yapona.state import RunningState, IdleState
from yapona.timer import Timer
from yapona.hook import HookCollection
from yapona.dbus import DBusHook
from yapona.history import HistoryHook


class Engine:

    def __init__(self, duration=60 * 20) -> None:
        self.duration = duration
        self.timer = Timer()
        self.hooks = HookCollection([DBusHook(), HistoryHook()])
        self.msg = ""

    def _get_state_as(self, cls):
        if self.timer.state.__class__ != cls:
            return None
        return cast(cls, self.timer.state)

    def start(self):
        state = self._get_state_as(IdleState)
        if state is None:
            return False
        self.hooks.on_start(state)
        self.timer.state = RunningState(self.timer.state.id, self.duration)
        return self.timer.start()

    def interrupt(self):
        state = self._get_state_as(RunningState)
        if state is None:
            return False
        self.hooks.on_interrupt(state)
        return self.timer.interrupt()

    def update(self):
        state = self._get_state_as(RunningState)
        if state is None:
            return False
        self.hooks.on_update(state)
        ok = self.timer.update()
        if ok and self.timer.is_done():
            return self.set_done()
        return ok

    def set_done(self):
        state = self._get_state_as(RunningState)
        if state is None:
            return False
        self.hooks.on_done(state)
        self.msg = "Pomodoro done. Hooray!"
        self.timer.state = IdleState()
