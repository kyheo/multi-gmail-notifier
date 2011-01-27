import sys
import os
import re
import urllib2
import base64
import feedparser

import indicate
import gobject
import gtk
import pynotify

from multigmailnotifier import gk

#FIXME Source DESKTOP_FILE is hardcoded
DESKTOP_FILE = '/home/martin/dev/multi-gmail-notifier/multigmailnotifier.desktop'

class Label(object):
    
    URL = 'https://mail.google.com/mail/feed/atom/%s'

    def __init__(self, user, passwd, name='inbox'):
        self.user = user
        self.passwd = passwd
        self.name = name
        self.total = 0
        self.ids = []
        self.unread = False

        if self.name.lower() == 'inbox':
            self.url = self.URL % ('',)
        else:
            self.url = self.URL % (name.replace('/', '-'),)

        self.indicator = indicate.Indicator()
        self.indicator.set_property("sender", self.name)
        self.indicator.set_property("count", str(self.total))
        self.indicator.show()
        self.indicator.connect("user-display", self.click)

        self.check()

    def click(self, *args, **kwargs):
        self.silence()
        #TODO Open label on browser
        #https://mail.google.com/mail/u/0/?shva=1#inbox
        #https://mail.google.com/mail/u/0/?shva=1#label/Listas%2FListas 

    def attention(self):
        self.indicator.set_property("sender", "* %s" % (self.name,))
        self.indicator.set_property("draw-attention", "true")
        self.notify()

    def notify(self):
        title = "%s  ::  %s" % (self.user, self.name)
        desc = '%d new emails.' % (self.total,)
        n = pynotify.Notification(title, desc, "notification-message-email")
        n.set_timeout(2000)
        n.show()

    def silence(self):
        self.indicator.set_property("sender", self.name)
        self.indicator.set_property("draw-attention", "false")

    def check(self):
        req = urllib2.Request(self.url)
        req.add_header("Authorization", \
                       "Basic %s" % (base64.encodestring("%s:%s" % \
                            (self.user, self.passwd))[:-1]))
        result = feedparser.parse(urllib2.urlopen(req).read())
        self._parse_result(result)
        self.indicator.set_property("count", str(self.total))
        if self.unread:
            self.attention()

    def _parse_result(self, data):
        self.total = int(data['feed']['fullcount'])
        if self.total == 0:
            self.unread = False
            self.ids = []
        else:
            nids = set([entry['id'] for entry in data['entries']])
            if nids == self.ids:
                self.unread = False
            else:
                for nid in nids:
                    if nid not in self.ids:
                        self.unread = True
                self.ids = nids
    


class Account(object):

    def __init__(self, user, passwd, uri, labels=['inbox'], timeout=60*5):
        self.user = user
        self.passwd = passwd
        self.uri = uri
        self.labels = [Label(self.user, self.passwd, l) for l in labels]
        self.timeout = timeout
        self.desktop_file = '/tmp/gmc_%s' % (self.user,) 

        self._create_desktop_file()

        self.server = indicate.indicate_server_ref_default()
        self.server.set_type("message.mail")
        self.server.set_desktop_file(self.desktop_file)
        self.server.connect("server-display", self.click)
        self.server.show()

    def check(self):
        for label in self.labels:
            label.check()
        gobject.timeout_add_seconds(self.timeout, self.check)

    def click(self, server, *args, **kwargs):
        for label in self.labels:
            label.silence()

    def _create_desktop_file(self):
        data = open(DESKTOP_FILE).read()
        o = open(self.desktop_file,"w")
        o.write(re.sub("##NAME##", self.user, data))
        o.close()



def main():
    APP_NAME = 'multi-gmail-notifier'
    APP_PASS = 'multi-gmail-notifier-pass'

    config = gk.GK(APP_NAME, APP_PASS)
    config.unlock_app()

    for u in config.get_users():
        a = Account(u['item'].get_display_name(), u['item'].get_secret(),
                    u['attr']['uri']
                    #, labels=['Inbox', '__JOBS__', 'Listas/PyAr']
                    #, timeout=timeout
                    )
        a.check()
    config.lock_app()

    try:
        gtk.main()
    except KeyboardInterrupt:
        print ''
        sys.exit()

if __name__ == '__main__':
    main()
