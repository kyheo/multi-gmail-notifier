from multigmailnotifier import gk

class Account(object):
    
    def __init__(self, name, passwd, uri):
        self.name = name
        self.passwd = passwd
        self.uri = uri

def main():
    APP_NAME = 'multi-gmail-notifier'
    APP_PASS = 'multi-gmail-notifier-pass'

    config = gk.GK(APP_NAME, APP_PASS)
    config.unlock_app()

    accounts = []
    for u in config.get_users():
        accounts.append(Account(u['item'].get_display_name(), u['item'].get_secret(),
                                u['attr']['uri']))
    config.lock_app()

    print accounts


if __name__ == '__main__':
    main()
