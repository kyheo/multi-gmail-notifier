# -*- coding: utf-8 -*-

import os, sys
import ConfigParser
import keyring, getpass

class MGConfig(object):

    def __init__(self):
        self.home_folder         = "/home/%s" % (os.popen("whoami").read()[:-1])
        self.config_folder       = "%s/.config" % (self.home_folder)
        self.gmail_config_folder = "%s/multi-gmail-notifier" % (self.config_folder)
        self.config_file         = "%s/settings.conf" % (self.gmail_config_folder)
        self.app_path            = sys.path[0]

        self.check               = 60 * 5

        self._init_conf_dirs()

        self._c = ConfigParser.RawConfigParser()
        self._c.read(self.config_file)

    def grab_data(self):
        username = raw_input('Username: ')
        password = getpass.getpass()
        homepage = raw_input('Homepage (ex: http://www.gmail.com): ')
        
        realm  = self.get_realm(username)

        keyring.set_password(realm, username, password)
        section_name = "account_%s" % (username,)
        
        if not self._c.has_section(section_name):
            self._c.add_section(section_name)

        self._c.set(section_name, "username", username)
        self._c.set(section_name, "homepage", homepage)
        self._c.write(open(self.config_file, "wb"))

    def get_realm(self, username):
        return "Multi Gmail Notifier - Account: %s" % (username,)

    def _init_conf_dirs(self):
        if not os.path.exists(self.config_folder):
            os.mkdir(self.config_folder, 0700)

        if not os.path.exists(self.gmail_config_folder):
            os.mkdir(self.gmail_config_folder, 0700)
