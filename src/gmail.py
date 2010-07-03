#!/usr/bin/env python

import os
import feedparser
import urllib2, base64
import indicate

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

