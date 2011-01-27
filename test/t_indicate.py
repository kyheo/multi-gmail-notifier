#!/usr/bin/env python

# sets a indication in the indicator applect
# sudo apt-get install python-indicate

import sys, os
try:
    import indicate
    import gobject 
    import gtk 
except ImportError, e:
    print "Error: %s" % (e,)
    sys.exit(1)

curdir = os.getcwd() 
desktop_file = os.path.join(curdir, "t_indicate.desktop")

def server_display(server, *args, **kwargs):
    for indicator in server.indicators:
        indicator.set_property("draw-attention", "false")

def display(indicator, *args, **kwargs):
    indicator.set_property("draw-attention", "false")

def timeout_cb(indicator):
    old = indicator.get_property('count')
    new = int(old) + 1
    indicator.set_property("count", str(new))

    if new % 2 == 0:
        indicator.set_property("draw-attention", "true")
        old_title = indicator.get_property('sender')
        indicator.set_property('sender', "%s *" % (old_title,))

    return True


if __name__ == "__main__":

    for i in range(2):
        pid = os.fork()
        if pid == 0:
            # Setup the server
            server = indicate.indicate_server_ref_default()
            server.set_type("message.mail")
            server.set_desktop_file(desktop_file)
            server.connect("server-display", server_display)
            server.show()
            
            # Setup the message
            indicator = indicate.Indicator()
            indicator.set_property("sender", "Test message %d" % (i,))
            indicator.set_property("count", "1")
            indicator.show()
            indicator.connect("user-display", display)

            server.indicators = [indicator]

            # Loop
            gobject.timeout_add_seconds(3, timeout_cb, indicator)
            gtk.main()


