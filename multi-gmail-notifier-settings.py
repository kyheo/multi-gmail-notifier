#!/usr/bin/env python

import os
import keyring
import getpass
import ConfigParser

HOME_FOLDER         = "/home/%s" % (os.popen("whoami").read()[:-1])
CONFIG_FOLDER       = "%s/.config" % (HOME_FOLDER)
GMAIL_CONFIG_FOLDER = "%s/multi-gmail-notifier" % (CONFIG_FOLDER)
CONFIG_FILE         = "%s/settings.conf" % (GMAIL_CONFIG_FOLDER)

if not os.path.exists(CONFIG_FOLDER):
    os.mkdir(CONFIG_FOLDER, 0700)

if not os.path.exists(GMAIL_CONFIG_FOLDER):
    os.mkdir(GMAIL_CONFIG_FOLDER, 0700)

username = raw_input('Username: ')
password = getpass.getpass()
homepage = raw_input('Homepage (ex: http://www.gmail.com): ')

realm  = "Multi Gmail Notifier - Account: %s" % (username,)

keyring.set_password(realm, username, password)

config = ConfigParser.RawConfigParser()
config.read(CONFIG_FILE)

section_name = "account_%s" % (username,)

if not config.has_section(section_name):
    config.add_section(section_name)

config.set(section_name, "username", username)
config.set(section_name, "homepage", homepage)
config.write(open(CONFIG_FILE, "wb"))
