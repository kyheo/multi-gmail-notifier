#!/usr/bin/env python

from src import gk

from src.daemonize import daemonize
from src.notifier  import Notifier
from src.gmail     import GMail

import os, sys
import gobject, gtk

if (__name__ == "__main__"):
    APP_NAME = 'multi-gmail-notifier'
    APP_PASS = 'multi-gmail-notifier-pass'
    CHECK    = 60 * 5
 
    if not(len(sys.argv) > 1 and sys.argv[1] == '--no-daemon'):
        daemonize()
    
    config = gk.GK(APP_NAME, APP_PASS);
    config.unlock_app()

    notifier = Notifier(sys.path[0], CHECK) 
    for u in config.get_users():
        m = GMail(u['item'].get_display_name(),
                  u['item'].get_secret(),
                  u['attr']['uri'])
        notifier.accounts.append(m)

    config.lock_app()

    try:
        notifier.run()
        gtk.main()
    except KeyboardInterrupt:
        sys.exit()

