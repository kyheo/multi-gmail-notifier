#!/usr/bin/env python

import os
import gobject, gtk
import indicate
import pynotify

class Notifier(object):
    def __init__(self, path, check):
        self.accounts = []
        self.check = check
        # Indicator
        self.server = indicate.indicate_server_ref_default()
        self.server.set_type("message.mail")
        self.server.set_desktop_file(os.path.join(path, 'multi-gmail-notifier.desktop'))
        self.server.connect("server-display", self.clicked)
        self.server.show()

    def run(self):
        pynotify.init("icon-summary-body")
        n = pynotify.Notification('GMail', "You have mail.", "notification-message-email")
        for account in self.accounts:
            try:
                new = account.check_mail()
                if new is True:
                    n.show()
            except Exception, e:
                n = pynotify.Notification('GMail', e, "gtk-error")
                n.show()
        gobject.timeout_add_seconds(self.check, self.run)

    def clicked(self, *args, **kwargs):
        for account in self.accounts:
            account.quiet()

