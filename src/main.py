from dbus_next.glib import MessageBus
from dbus_next.message import Message

bus = MessageBus()
bus.connect_sync()
print("Connected")

message = Message("i3.status.rs",
                  "/Pomodoro",
                  "i3.status.rs",
                  "SetStatus",
                  signature="s", body=["sosi"])
bus.call_sync(message)
