"""
Pomodoro timer class
"""

from abc import ABC, abstractmethod
import time
from src.dbus import DBus


class State(ABC):

    @abstractmethod
    def step(self):
        pass

    @abstractmethod
    def done(self):
        pass


class IdleState(State):

    def __init__(self, dbus):
        self.dbus = dbus
        self.dbus.call("Waiting")

    def step(self):
        pass

    def done(self):
        return False


class RunningState(State):
    def __init__(self, dbus):
        self.dbus = dbus
        self.start_time = time.time()
        self.cur_time = self.start_time
        self.max_duration = 60 * 20

    def step(self):
        self.cur_time = time.time()
        delta = int(self.cur_time - self.start_time)
        if delta < 60:
            msg = f"{delta}s"
        else:
            msg = f"{delta // 60}m:{delta % 60}s"
        self.dbus.call(msg)

    def done(self):
        return self.cur_time - self.start_time >= self.max_duration


class Timer:

    def __init__(self):
        self.dbus = DBus()
        self.state = IdleState(self.dbus)
        self.msg = ""

    def start(self) -> bool:
        if self.state.__class__ != IdleState:
            return False
        self.state = RunningState(self.dbus)
        return True

    def interrupt(self) -> bool:
        if self.state.__class__ != RunningState:
            return False
        self.state = IdleState(self.dbus)
        return True

    def on_done(self):
        if self.state.__class__ == RunningState:
            self.msg = "Pomodoro done. Hooray!"
            self.state = IdleState(self.dbus)

    def update(self):
        self.state.step()
        if self.state.done():
            self.on_done()
