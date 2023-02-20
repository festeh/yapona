from dbus_next.glib import MessageBus
from dbus_next.message import Message


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
