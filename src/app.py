import time
from threading import Thread, Lock
import os
from src.timer import Timer
import atexit
import gi
import signal
from functools import partial
gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
gi.require_version("AppIndicator3", "0.1")
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify

mutex = Lock()


def get_icon(name):
    icons_dir = os.path.dirname(os.path.realpath(__file__))
    path = os.path.realpath(os.path.join(icons_dir, name))
    assert os.path.exists(path)
    return path


def send_notification(message):
    Notify.init("pomodoro-indicator")
    Notify.Notification.new(message).show()
    Notify.uninit()


class App:

    def __init__(self):
        self.name = "Yapona"
        self.indicator = appindicator.Indicator.new(
            "appindicator", get_icon("focus.svg"),
            appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu())
        self.indicator.set_label(self.name, self.name)
        self.start_time = time.time()
        self.timer = Timer()
        self.update = Thread(target=self.show_seconds)
        self.update.daemon = True
        self.update.start()

    def create_menu(self):
        menu = gtk.Menu()
        item_start_10_min = gtk.MenuItem(label="Start (10 min)")
        item_start_10_min.connect("activate", partial(self.start, duration=10 * 60))
        item_start_20_min = gtk.MenuItem(label="Start (20 min)")
        item_start_20_min.connect("activate", partial(self.start, duration=20 * 60))
        item_start_30_min = gtk.MenuItem(label="Start (30 min)")
        item_start_30_min.connect("activate", partial(self.start, duration=30 * 60))
        item_reset = gtk.MenuItem(label="Reset")
        item_reset.connect("activate", self.reset)
        item_quit = gtk.MenuItem(label="Quit")
        item_quit.connect("activate", self.quit)
        menu.append(item_start_10_min)
        menu.append(item_start_20_min)
        menu.append(item_start_30_min)
        menu.append(item_reset)
        menu.append(item_quit)
        menu.show_all()
        return menu

    def show_seconds(self):
        while True:
            with mutex:
                self.timer.update()
                if self.timer.msg:
                    send_notification(self.timer.msg)
                    self.timer.msg = ""
            time.sleep(1)

    def start(self, widget, duration = 60 * 20):
        with mutex:
            self.timer = Timer(duration=duration)
            send_notification("Pomodoro started")
            self.timer.start()

    def reset(self, widget):
        with mutex:
            send_notification("Pomodoro reset")
            self.timer.interrupt()

    def quit(self, widget):
        gtk.main_quit()


def handle_exit(*args):
    from src.dbus import DBus
    bus = DBus()
    bus.call("Waiting")


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    atexit.register(handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    app = App()
    gtk.main()
