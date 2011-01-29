#!/usr/bin/env python

from multigmailnotifier import gk

import pygtk
import gtk

class Settings(object):
    
    def __init__(self, app_name, app_pass):
        self.config = gk.GK(app_name, app_pass);
        self.config.create_app()
        self.config.unlock_app()

        self.builder = gtk.Builder()
        self.builder.add_from_file("multigmailnotifier-settings.glade")
        self.builder.connect_signals(self);
 
        self.set_initial_state()
        self.users_list_init()

    def show(self):
        self.builder.get_object("settings_window").show()
        gtk.main()

    def set_initial_state(self):
        self.set_entry_text('', '', '', '', '')
        self.set_entry_editable(False, False, False, False, False)
        self.set_buttons_visibility(True, False, False, True, False)

    def users_list_init(self):
        uts = gtk.TreeStore(str, str, str, str, str)
        for u in self.config.get_users():
            l = ''
            if 'labels' in u['attr']:
                l = u['attr']['labels']
            t = ''
            if 'timeout' in u['attr']:
                t = u['attr']['timeout']
            uts.append(None, [u['item'].get_display_name(), \
                              u['item'].get_secret(), \
                              u['attr']['uri'], l, t])

        col = gtk.TreeViewColumn('Users')
        cell = gtk.CellRendererText()
        col.pack_start(cell, True)
        col.add_attribute(cell, 'text', 0)
        
        self.builder.get_object('users_list').append_column(col)
        self.builder.get_object('users_list').set_model(uts)

    def exit(self):
        self.config.lock_app()
        gtk.main_quit()

    def set_entry_text(self, username, password, uri, labels, timeout):
        self.builder.get_object('username_entry').set_text(username)
        self.builder.get_object('password_entry').set_text(password)
        self.builder.get_object('uri_entry').set_text(uri)
        self.builder.get_object('labels_entry').set_text(labels)
        self.builder.get_object('timeout_entry').set_text(timeout)

    def set_entry_editable(self, username, password, uri, labels, timeout):
        self.builder.get_object('username_entry').set_editable(username)
        self.builder.get_object('password_entry').set_editable(password)
        self.builder.get_object('uri_entry').set_editable(uri)
        self.builder.get_object('labels_entry').set_editable(labels)
        self.builder.get_object('timeout_entry').set_editable(timeout)

    def set_buttons_visibility(self, new, save, remove, quit, cancel):
        self.builder.get_object('new').set_visible(new)
        self.builder.get_object('save').set_visible(save)
        self.builder.get_object('remove').set_visible(remove)
        self.builder.get_object('quit').set_visible(quit)
        self.builder.get_object('cancel').set_visible(cancel)

    def on_settings_window_destroy(self, widget, data=None):
        self.exit()

    def on_mf_ok_clicked(self, widget, data=None):
        self.builder.get_object('mf_window').hide()
     
    def on_users_list_cursor_changed(self, widget, data=None):
        model, row = widget.get_selection().get_selected()
        if row is not None:
            self.set_entry_text(model.get_value(row, 0), \
                                model.get_value(row, 1), \
                                model.get_value(row, 2), \
                                model.get_value(row, 3), \
                                model.get_value(row, 4) )
            self.set_entry_editable(True, True, True, True, True)
            self.set_buttons_visibility(False, True, True, False, True)

    def on_new_clicked(self, widget, data=None):
        self.set_entry_text('', '', '', '', '')
        self.set_entry_editable(True, True, True, True, True)
        self.set_buttons_visibility(False, True, False, False, True)

    def on_save_clicked(self, widget, data=None):
        ue = self.builder.get_object('username_entry')
        pe = self.builder.get_object('password_entry')
        ri = self.builder.get_object('uri_entry')   
        li = self.builder.get_object('labels_entry')
        ti = self.builder.get_object('timeout_entry')
        if not ue.get_text() or not pe.get_text() or not ri.get_text():
            self.builder.get_object('mf_window').show()
        else:
            model, row = self.builder.get_object('users_list').get_selection().get_selected()
            if row is not None:
                model.set_value(row, 0, ue.get_text())
                model.set_value(row, 1, pe.get_text())
                model.set_value(row, 2, ri.get_text())
                model.set_value(row, 3, li.get_text())
                model.set_value(row, 4, ti.get_text())
            else:
                model.append(None, [ue.get_text(), pe.get_text(),
                                    ri.get_text(), li.get_text(), 
                                    ti.get_text()])

            self.config.add_user(ue.get_text(), pe.get_text(), ri.get_text(),
                                 li.get_text(), ti.get_text())
            self.set_initial_state()

    def on_remove_clicked(self, widget, data=None):
        model, row = self.builder.get_object('users_list').get_selection().get_selected()
        if row is not None:
            self.config.delete_user(model.get_value(row, 0))
            model.remove(row)
        self.set_initial_state()
        
    def on_quit_clicked(self, widget, data=None):
        self.exit()

    def on_cancel_clicked(self, widget, data=None):
        self.set_initial_state()
