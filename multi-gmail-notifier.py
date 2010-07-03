#!/usr/bin/env python

from src.mgconfig  import MGConfig
from src.daemonize import daemonize
from src.notifier  import Notifier
from src.gmail     import GMail

import os, sys
import gobject, gtk

if (__name__ == "__main__"):
 
    if not(len(sys.argv) > 1 and sys.argv[1] == '--no-daemon'):
        daemonize()
    
    config   = MGConfig() 
    notifier = Notifier(sys.path[0], config.check)

    for section in config.get_sections():
        d = config.get_data(section)
        m = GMail(d['username'], d['password'], d['uri'])
        notifier.accounts.append(m)

    try:
        notifier.run()
        gtk.main()
    except KeyboardInterrupt:
        sys.exit()

