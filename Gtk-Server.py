# Copyright 2023 ShadowOfHassen
# A Gtk Server for Linux
# Licensed under the Lesser GPL License
# Imports / Setting Up Gtk
import gi

gi.require_version('Gtk','3.0')

from gi.repository import Gtk, Gdk, GdkPixbuf, GObject


import subprocess
import threading
import json
import socket

import savvy

UI_PATH = './gtk_ui.glade'
CONFIG_PATH = './config.json'

#


try:
    file = open(CONFIG_PATH, 'r')
    settings = json.load(file)
    port = settings['port']
    active = settings['active']
    
except FileNotFoundError:
    port = 8081
    active = False

class Window(Gtk.Window):
        def __init__(self, app, port, active):
            super().__init__(title='Savvy Gtk Server', application=app)
            self.server = savvy.Server(port)
            self.connect('destroy', self.on_quit)
            self.server_active = active
            self.load_ui()
            
        
        def load_ui(self):
            # Load UI
            builder = Gtk.Builder()
            builder.add_from_file(UI_PATH)
            # define UI parts and set them up
            header_bar = builder.get_object('app_bar')
            self.set_titlebar(header_bar)
            # Set up the rest
            self.main_box = builder.get_object('menu_box')
            self.add(self.main_box)
            self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
            self.server_togle_button = builder.get_object('server_togle_button')
            self.server_togle_button.set_active(self.server_active)
            about_button = builder.get_object('about_button')
            about_button.connect('clicked', self.on_about_button_pressed)
            self.status_label = builder.get_object('status_label')
            self.port_entry = builder.get_object('port_entry')
            self.copy_button = builder.get_object('clipboard_copy_button')
            self.port_entry.set_text(str(self.server.port))
            bindings = {'on_clipboard_copy_button_clicked':self.on_copy_url_clicked,'on_apply_button_clicked':self.on_apply_button_clicked,
                        'on_server_togle_button_toggled':self.on_server_togle_button_toggled
                        }
            builder.connect_signals(bindings)
            self.on_server_togle_button_toggled(self.server_togle_button)  # Useless number to get the thing to run
        def on_server_togle_button_toggled(self, button):
            if button.get_active ():
                self.server_togle_button.set_label('Server On!')
                self.server.start_server()

            else:
                self.server_togle_button.set_label('Activate Server')
                self.server.terminate_server()
        
        def on_about_button_pressed(self, button):
            about_dialog = About()
                        
        def on_copy_url_clicked(self, button):
            self.clipboard.set_text(self.server.url , -1)
            button.set_label('Copied!')
            
        def on_apply_button_clicked(self, button):
            self.server.terminate_server()
            try:
                self.server.port = int(self.port_entry.get_text())
            except ValueError:
                self.status_label.set_label('Please put in a real number!')
            self.server.start_server()
            self.copy_button.set_label('Copy Link To Clipboard')
            
        def on_quit(self, widget):
            file = open(CONFIG_PATH, 'w')
            json.dump({'port':self.server.port,'active':self.server.active}, file)
            file.close()
            self.server.terminate_server()
            Gtk.main_quit()


class About(GObject.Object):
    def __init__(self,):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(UI_PATH)
        d = self.builder.get_object('about-dialog')
        d.show_all()

# App

class SavvyApp(Gtk.Application):

    def __init__(self):
        super().__init__()

    def do_activate(self):
        self.win = Window(self, port, active)
       # self.win.set_icon(GdkPixbuf.Pixbuf.new_from_file(LOGO_FILE))
        self.win.show_all()
app = SavvyApp()

if __name__ == '__main__':
    app.run()          