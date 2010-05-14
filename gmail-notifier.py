#!/usr/bin/env python

import os, sys
import ConfigParser, keyring
import gobject, gtk
import feedparser
import urllib2, base64
import indicate
import pynotify

from pprint import pprint

class GMail(indicate.Indicator):
    #@TODO aaaaa
    ATOM_URL = "https://mail.google.com/mail/feed/atom/"

    def __init__(self, username, password, uri):
        # Utils
        self.messages = set()
        self.unread   = 0
        self.new      = False
        # Login information
        self.username = username
        self.password = password
        self.uri      = uri
        # News requester
        self.req = urllib2.Request(self.ATOM_URL)
        self.req.add_header("Authorization", "Basic %s" % \
                        (base64.encodestring("%s:%s" % \
                            (self.username, self.password))[:-1]))
        # Indicator
        indicate.Indicator.__init__(self)
        self.connect("user-display", self.clicked)
        self.set_property("subtype", "mail")
        self.show()

    def show(self, *args, **kwargs):
        prefix = ''
        if self.new is True:
            prefix = '* '
        self.set_property("name", "%s%s - %d" % (prefix, self.username,self.unread))
        indicate.Indicator.show(self, *args, **kwargs)

    def clicked(self, *args):
        os.popen("gnome-open '%s' &" % (self.uri,))
        self.quiet()

    def quiet(self):
        self.set_property("draw-attention", "false")
        self.new = False
        self.show()

    def check_mail(self):
        atom = feedparser.parse(urllib2.urlopen(self.req).read())
        self.unread = len(atom['entries'])
        ids = set([entry['id'] for entry in atom['entries']])
        if len(ids) == 0:
            self.messages = set()
        elif ids != self.messages:
            self.messages = ids
            self.new = True
            self.set_property("draw-attention", "true")
        else:
            self.new = False
        self.show()
        return self.new



class Notifier:
    def __init__(self, path, check):
        self.accounts = []
        self.check = check
        # Indicator
        self.server = indicate.indicate_server_ref_default()
        self.server.set_type("message.mail")
        self.server.set_desktop_file(os.path.join(path, 'gmail-notifier.desktop'))
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



##### Fork Main process
def daemonize(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        sys.stderr.write("fork #1 failed: (%d) %sn" % (e.errno, e.strerror))
        sys.exit(1)

    os.chdir("/")
    os.setsid()
    os.umask(0)

    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        sys.stderr.write("fork #2 failed: (%d) %sn" % (e.errno, e.strerror))
        sys.exit(1)

    for f in sys.stdout, sys.stderr: f.flush()
    si = file(stdin, 'r')
    so = file(stdout, 'a+')
    se = file(stderr, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


if (__name__ == "__main__"):
    HOME_FOLDER         = "/home/%s" % (os.popen("whoami").read()[:-1])
    CONFIG_FOLDER       = "%s/.config" % (HOME_FOLDER)
    GMAIL_CONFIG_FOLDER = "%s/gmail-notifier" % (CONFIG_FOLDER)
    CONFIG_FILE         = "%s/settings.conf" % (GMAIL_CONFIG_FOLDER)

    CHECK = 60 * 5

    APP_PATH = sys.path[0]

    config = ConfigParser.RawConfigParser()
    config.read(CONFIG_FILE)

    daemonize()

    notifier = Notifier(APP_PATH, CHECK)
    for section in config.sections():
        username = config.get(section, 'username')
        realm    = "Gmail Notifier - Account: %s" % (username,)
        password = keyring.get_password(realm, username)
        uri      = config.get(section, 'homepage')
        
        m = GMail(username, password, uri)
        notifier.accounts.append(m)

    notifier.run()
    gtk.main()

