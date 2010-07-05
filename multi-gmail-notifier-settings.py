#!/usr/bin/env python

#CREQO QUE DEBERIA GUARDAR TODO EN MEMORIA Y RECIEN DESPUES, AL CERRAR, HABRIA
#QUE GUARDAR LOS DATOS EN EL ARCHIVO.



from src import mgconfig

import pygtk
import gtk
import pango

class Settings(object):
    def __init__(self):
        self.config = mgconfig.MGConfig();

        builder = gtk.Builder()
        builder.add_from_file("multi-gmail-notifier-settings.glade")
        builder.connect_signals({
            'on_settings_window_destroy' : self.exit,
            'on_quit_clicked': self.exit,
            'on_mf_ok_clicked': self.mf_exit,
            'on_users_list_cursor_changed': self.users_list_changed,

            'on_save_clicked': self.save_click,
            'on_new_clicked': self.new_click,
            'on_remove_clicked': self.remove_click
            })
        
        self.window = builder.get_object("settings_window")
        
        self.username_entry = builder.get_object('username_entry')
        self.password_entry = builder.get_object('password_entry')
        self.uri_entry      = builder.get_object('uri_entry')

        self.new_btn    = builder.get_object('new')
        self.save_btn   = builder.get_object('save')
        self.remove_btn = builder.get_object('remove')
        self.quit_btn   = builder.get_object('quit')

        self.mf_window = builder.get_object('mf_window')

        self.mf_label = builder.get_object('mf_label')
        self.mf_label.modify_font(pango.FontDescription("sans 26"))

        self.users_list = builder.get_object('users_list')

        self.users_list_init()

        self.window.show()

    def exit(self, widget):
        gtk.main_quit()

    def mf_exit(self, widget):
        self.mf_window.hide()

    def users_list_changed(self, widget):
        model, row = widget.get_selection().get_selected()
        if row is not None:
            self.username_entry.set_text(model.get_value(row, 0))
            self.password_entry.set_text(model.get_value(row, 1))
            self.uri_entry     .set_text(model.get_value(row, 2))

            self.username_entry.set_editable(True)
            self.password_entry.set_editable(True)
            self.uri_entry     .set_editable(True)

            self.new_btn   .set_visible(True)
            self.save_btn  .set_visible(True)
            self.remove_btn.set_visible(True)
            self.quit_btn  .set_visible(False)
        
    def new_click(self, widget):
        self.username_entry.set_text('')
        self.password_entry.set_text('')
        self.uri_entry     .set_text('')

        self.username_entry.set_editable(True)
        self.password_entry.set_editable(True)
        self.uri_entry     .set_editable(True)

        self.new_btn   .set_visible(False)
        self.save_btn  .set_visible(True)
        self.remove_btn.set_visible(False)
        self.quit_btn  .set_visible(False)

    def remove_click(self, widget):
        pass

##########################################


    def save_click(self, widget):
        if not self.username_entry.get_text() or \
           not self.password_entry.get_text() or \
           not self.uri_entry.get_text():
            self.mf_window.show()
        else:
            self.config.save_data(self.username_entry.get_text(), \
                                  self.password_entry.get_text(), \
                                  self.uri_entry.get_text())
            self.users_combo_init()

    def users_list_init(self):
        uts = gtk.TreeStore(str, str, str)
        for section in self.config.get_sections():
            d = self.config.get_data(section)
            uts.append(None, [d['username'], d['password'], d['uri']])

        col = gtk.TreeViewColumn('Users')
        cell = gtk.CellRendererText()
        col.pack_start(cell, True)
        col.add_attribute(cell, 'text', 0)
        
        self.users_list.append_column(col)
        self.users_list.set_model(uts)


if __name__ == "__main__":
    settings = Settings()
    gtk.main()
