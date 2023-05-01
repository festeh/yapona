from yapona.hook import Hook
from dbus_next.glib import MessageBus
from dbus_next.message import Message
from yapona.state import RunningState, IdleState


class DBus:

    def __init__(self):
        self.bus = MessageBus()
        self.bus.connect_sync()

    def call(self, text):
        message = Message("i3.status.rs",
                          "/Pomodoro",
                          "i3.status.rs",
                          "SetStatus",
                          signature="s",
                          body=[text])
        self.bus.call_sync(message)


class DBusHook(Hook):

    def __init__(self):
        self.dbus = DBus()

    def on_start(self, state: IdleState):
        self.dbus.call("Waiting")

    def on_update(self, state: RunningState):
        delta = int(state.delta)
        if delta < 60:
            msg = f"{delta}s"
        else:
            msg = f"{delta // 60}m:{delta % 60}s"
        self.dbus.call(msg)

    def on_interrupt(self, state: RunningState):
        self.dbus.call("Waiting")

    def on_done(self, state: IdleState):
        self.dbus.call("Waiting")
