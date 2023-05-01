from typing import Optional, cast
from yapona.state import RunningState, IdleState
from yapona.timer import Timer
from yapona.hook import HookCollection
from yapona.dbus import DBusHook


class Engine:

    def __init__(self, duration=60 * 20) -> None:
        self.timer = Timer(duration)
        self.hooks = HookCollection([DBusHook()])
        self.msg = ""

    def _get_state_as(self, cls):
        if self.timer.__class__ != cls:
            return None
        return cast(cls, self.timer.state)

    def start(self):
        state = self._get_state_as(IdleState)
        if state is None:
            return False
        self.hooks.on_start(state)
        return self.timer.start()

    def interrupt(self):
        state = self._get_state_as(RunningState)
        if state is None:
            return False
        self.hooks.on_interrupt(state)
        return self.timer.interrupt()

    def update(self):
        print("tik")
        state = self._get_state_as(RunningState)
        if state is None:
            return False
        print("tik2")
        self.hooks.on_update(state)
        ok = self.timer.update()
        if ok and self.timer.is_done():
            return self.set_done()
        return ok

    def set_done(self):
        state = self._get_state_as(RunningState)
        if state is None:
            return False
        self.msg = "Pomodoro done. Hooray!"
        state = IdleState()
        self.timer.state = state
        self.hooks.on_done(state)
