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

        self.check               = 60 * 5

        self._init_conf_dirs()

        self.c = ConfigParser.RawConfigParser()
        self.c.read(self.config_file)


    def grab_data(self):
        username = raw_input('Username: ')
        password = getpass.getpass()
        homepage = raw_input('Homepage (ex: http://www.gmail.com): ')
        
        realm  = self.get_realm(username)

        keyring.set_password(realm, username, password)
        section_name = "account_%s" % (username,)
        
        if not self.c.has_section(section_name):
            self.c.add_section(section_name)

        self.c.set(section_name, "username", username)
        self.c.set(section_name, "homepage", homepage)
        self.c.write(open(self.config_file, "wb"))


    def get_realm(self, username):
        return "Multi Gmail Notifier - Account: %s" % (username,)


    def get_sections(self):
        return self.c.sections()


    def get_data(self, section):
        username = self.c.get(section, 'username')
        realm    = self.get_realm(username)
        password = keyring.get_password(realm, username)
        uri      = self.c.get(section, 'homepage')
        return {'username': username, 'password': password, 'uri': uri}


    def _init_conf_dirs(self):
        if not os.path.exists(self.config_folder):
            os.mkdir(self.config_folder, 0700)

        if not os.path.exists(self.gmail_config_folder):
            os.mkdir(self.gmail_config_folder, 0700)


