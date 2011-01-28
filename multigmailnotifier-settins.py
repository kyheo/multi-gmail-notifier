#!/usr/bin/env python

from multigmailnotifier import settings

if __name__ == "__main__":
    APP_NAME = 'multi-gmail-notifier'
    APP_PASS = 'multi-gmail-notifier-pass'
 
    s = settings.Settings(APP_NAME, APP_PASS)
    s.show()
