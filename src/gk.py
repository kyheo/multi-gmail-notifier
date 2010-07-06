import gnomekeyring as gk

class GK(object):
   
    def __unlock_app(fn):
        def deco(self, *args, **kwargs):
            self.unlock_app()
            res = fn(self, *args, **kwargs)
            return res
        return deco

    def __init__(self, app_name, app_pass):
        self._app_name = app_name.lower()
        self._app_pass = app_pass

    def create_app(self):
        if self._app_name not in gk.list_keyring_names_sync():
            gk.create_sync(self._app_name, self._app_pass)

    def lock_app(self):
        gk.lock_sync(self._app_name)

    def unlock_app(self):
        inf = gk.get_info_sync(self._app_name)
        if inf.get_is_locked():
            gk.unlock_sync(self._app_name, self._app_pass)

    def delete_app(self):
        gk.delete_sync(self._app_name)
    
    @__unlock_app
    def add_user(self, username, password, uri):
        atts = {'uri': uri}
        key,item = self.search_user(username)
        if item is not None:
            self.delete_user(key=key)
        gk.item_create_sync(self._app_name, gk.ITEM_GENERIC_SECRET, username, \
                            atts, password, True)

    @__unlock_app
    def search_user(self, username):
        item_keys = gk.list_item_ids_sync(self._app_name)
        if item_keys is not None:
            for key in item_keys:
                item_info = gk.item_get_info_sync(self._app_name, key)
                if (item_info.get_display_name() == username):
                    return key, item_info
        return None,None

    @__unlock_app
    def get_users(self):
        users = []
        item_keys = gk.list_item_ids_sync(self._app_name)
        for key in item_keys:
            item, attr = self.get_user(key)
            users.append({'item': item, 'attr': attr})
        return users

    @__unlock_app
    def get_user(self, key):
        item = gk.item_get_info_sync(self._app_name, key)
        attr = gk.item_get_attributes_sync(self._app_name, key)
        return item, attr

    @__unlock_app
    def delete_user(self, username=None, key=None):
        if key is None:
            key,item = self.search_user(username)
        gk.item_delete_sync(self._app_name, key)
        

if __name__ == '__main__':
    g = GK('testAPP', 'testPWD')
    g.create_app()
    g.add_user('martinUSER' , 'martinPASS' , 'http://www.gmaildasdasdas.com')
    g.add_user('martinUSER2', 'martinPASS2', 'http://www.gmaildasdasdas.com2')

    users = g.get_users()
    for u in users:
        user = u['item']
        attr = u['attr']
        print "Name    :", user.get_display_name()
        print "Uri     :", attr['uri'] 

    g.delete_app()
