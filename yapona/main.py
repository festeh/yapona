from dbus_next.glib import MessageBus
from dbus_next.message import Message


def main():
    bus = MessageBus()
    bus.connect_sync()
    message = Message("i3.status.rs",
                      "/Pomodoro",
                      "i3.status.rs",
                      "SetStatus",
                      signature="s", body=["hello"])
    bus.call_sync(message)


if __name__ == "__main__":
    main()
