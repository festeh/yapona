import atexit
from yapona.engine import Engine
from yapona.version import get_version
from yapona.task_window import TaskWindow
import os
from threading import Thread, Lock
import time
from functools import partial
import signal
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
gi.require_version("XApp", "1.0")
from gi.repository import Notify, XApp, Gtk as gtk

IS_DEBUG = os.environ.get("YAPONA_DEBUG", True)

def get_icon(name):
    icons_dir = os.path.dirname(os.path.realpath(__file__))
    if icons_dir is None:
        return None
    path = os.path.realpath(os.path.join(icons_dir, name))
    return path


def send_notification(message):
    Notify.init("pomodoro-indicator")
    Notify.Notification.new(message).show()
    Notify.uninit()


class App:

    def __init__(self):
        self.name = "Yapona"
        self.indicator = XApp.StatusIcon()
        self.indicator.set_primary_menu(self.create_menu())
        self.indicator.set_tooltip_text(get_version())
        self.indicator.set_icon_name(get_icon("focus.svg"))
        self.is_running = False
        self.mutex = Lock()
        self.start_time = time.time()
        self.pomo_engine = Engine()
        self.update = Thread(target=self.show_seconds)
        self.update.daemon = True
        self.update.start()
        if IS_DEBUG:
            self.task_window(None)

    def create_menu(self):
        menu = gtk.Menu()
        item_start_10_min = gtk.MenuItem(label="Start (10 min)")
        item_start_10_min.connect("activate",
                                  partial(self.start, duration=10 * 60))
        item_start_20_min = gtk.MenuItem(label="Start (20 min)")
        item_start_20_min.connect("activate",
                                  partial(self.start, duration=20 * 60))
        item_start_30_min = gtk.MenuItem(label="Start (30 min)")
        item_start_30_min.connect("activate",
                                  partial(self.start, duration=30 * 60))

        item_reset = gtk.MenuItem(label="Reset")
        item_reset.connect("activate", self.reset)

        item_quit = gtk.MenuItem(label="Quit")
        item_quit.connect("activate", self.quit)

        item_task = gtk.MenuItem(label="Task")
        item_task.connect("activate", self.task_window)

        menu.append(item_start_10_min)
        menu.append(item_start_20_min)
        menu.append(item_start_30_min)
        menu.append(item_task)
        menu.append(item_reset)
        menu.append(item_quit)

        if IS_DEBUG:
            item_start_10_sec = gtk.MenuItem(label="Start (10 sec)")
            item_start_10_sec.connect("activate",
                                      partial(self.start, duration=10))
            menu.append(item_start_10_sec)
        menu.show_all()
        return menu

    def show_seconds(self):
        while True:
            with self.mutex:
                self.pomo_engine.update()
                if self.pomo_engine.msg:
                    self.is_running = False
                    send_notification(self.pomo_engine.msg)
                    self.pomo_engine.msg = ""
            time.sleep(1)

    def start(self, widget, duration=60 * 20):
        with self.mutex:
            self.is_running = True
            self.pomo_engine = Engine(duration=duration)
            send_notification("Pomodoro started")
            self.pomo_engine.start()

    def reset(self, widget):
        with self.mutex:
            self.is_running = False
            send_notification("Pomodoro reset")
            self.pomo_engine.interrupt()

    def quit(self, widget):
        gtk.main_quit()

    def task_window(self, widget):
        window = TaskWindow(self)
        window.show_all()


def handle_exit(*args):
    from yapona.dbus import DBus
    bus = DBus()
    bus.call("Waiting")


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    atexit.register(handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    app = App()
    gtk.main()


if __name__ == '__main__':
    main()
