import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk, GLib as glib


class TaskWindow(gtk.Window):

    def __init__(self, app):
        gtk.Window.__init__(self, title="Daily Tasks")
        self.set_border_width(10)

        self.app = app
        status_vbox = self.draw_status()
        duration_vbox = self.draw_duration_radio_button()

        vbox = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)
        vbox.pack_start(status_vbox, False, False, 0)
        vbox.pack_start(duration_vbox, False, False, 0)


    def draw_status(self):
        vbox = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=10)
        self.state_label = gtk.Label()
        vbox.pack_start(self.state_label, False, False, 0)

        glib.timeout_add(100, self.update_state_label)
        return vbox

    def draw_duration_radio_button(self):
        vbox = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=10)

        duration_label = gtk.Label("Duration:")
        vbox.pack_start(duration_label, False, False, 0)

        self.minute10 = gtk.RadioButton.new_with_label_from_widget(
            None, "10 min")
        vbox.pack_start(self.minute10, False, False, 0)

        self.minute20 = gtk.RadioButton.new_with_label_from_widget(
            self.minute10, "20 min")
        vbox.pack_start(self.minute20, False, False, 0)

        self.minute30 = gtk.RadioButton.new_with_label_from_widget(
            self.minute10, "30 min")
        vbox.pack_start(self.minute30, False, False, 0)

        self.minute10.connect("toggled", self.on_duration_button_toggled, 10)
        self.minute20.connect("toggled", self.on_duration_button_toggled, 20)
        self.minute30.connect("toggled", self.on_duration_button_toggled, 30)

        return vbox

    def update_state_label(self):
        self.state_label.set_text(str(self.app.is_running))
        return True

    def on_duration_button_toggled(self, button, duration):
        if button.get_active():
            print(f"Selected color: {duration}")
