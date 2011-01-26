#!/usr/bin/env python

# pynotify sends pops a notification bubble of
# sudo apt-get install python-notify


import sys
try:
    import pynotify
except ImportError, e:
    print "Error: %s" % (e,)
    sys.exit(1)

if not pynotify.init('Testing'):
    print 'Error'
    sys.exit(1)

n = pynotify.Notification('Test Title', 'TEst content, this is longer. This message will live for 5 seconds')
n.set_timeout(5000)
if not n.show():
    print 'Error notifiying'
    sys.exit(1)
