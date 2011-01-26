import feedparser
import urllib2
import base64

from multigmailnotifier import gk
 
class Account(object):

    GMAIL_ATOM_URL = 'https://mail.google.com/mail/feed/atom/%s'
    
    def __init__(self, name, passwd, uri, labels=['inbox']):
        self.name = name
        self.passwd = passwd
        self.uri = uri
        self.labels = labels

    def check(self):
        res = {}
        for label in self.labels:
            label = label.lower()
            if label == 'inbox':
                url = self.GMAIL_ATOM_URL % ('',)
            else:
                url = self.GMAIL_ATOM_URL % (label,)
            req = urllib2.Request(url)
            req.add_header("Authorization", \
                           "Basic %s" % (base64.encodestring("%s:%s" % \
                                (self.name, self.passwd))[:-1]))
            atom = feedparser.parse(urllib2.urlopen(req).read())
            res[label] = int(atom['feed']['fullcount'])
        return res



def main():
    APP_NAME = 'multi-gmail-notifier'
    APP_PASS = 'multi-gmail-notifier-pass'

    config = gk.GK(APP_NAME, APP_PASS)
    config.unlock_app()

    accounts = []
    for u in config.get_users():
        accounts.append(Account(u['item'].get_display_name(), u['item'].get_secret(),
                                u['attr']['uri']
                                #,labels=[list of lables]
                                #, labels=['inbox', '__jobs__']
                                ))
    config.lock_app()
    

if __name__ == '__main__':
    main()
