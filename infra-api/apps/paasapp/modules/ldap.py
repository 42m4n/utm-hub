import logging

from ldap3 import Server, Connection
from django.core.cache import cache
from common.logger import logger

from common.conf import LDAP



class LDAPHandler:
    def __init__(self):
        self.server = Server(LDAP.server_ip)
        self.conn = Connection(self.server, LDAP.bind_user, password=LDAP.password, auto_bind='NONE',
                               raise_exceptions=True)

    def connect(self):
        self.conn.bind()
        logger.info('Ldap connection bind ')

    def disconnect(self):
        self.conn.unbind()
        logger.info('Ldap connection unbind ')

    def get_groups(self, search_field):

        cache_key = f'ldap_groups_{search_field.lower()}' if search_field else 'ldap_groups'
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info('Get LDAP groups from cache')
            return cached_data
        else:
            logger.info('Get groups from LDAP')
            self.conn.search(LDAP.groups_dn, '(objectClass=top)', search_scope="LEVEL", attributes=['name'])
            groups = self.conn.entries

            group_names = [
                {
                    entry.split(":")[0].strip(): entry.split(":")[1].strip()
                    for entry in str(group).split("\n")
                    if ":" in entry
                }
                for group in groups
            ]

            for i, obj in enumerate(group_names, start=1):
                obj.update({'id': i})
                obj.pop('DN', None)

            if search_field:
                group_names = [i for i in group_names if
                               i['name'].lower().startswith(search_field.lower()) or (
                                       len(search_field) >= 3 and search_field.lower() in i['name'].lower())]
                cache.set(f'ldap_groups_{search_field}', group_names)
            else:
                cache.set('ldap_groups', group_names)
            return group_names

    def get_users(self):
        self.conn.search('OU=Users,OU=ASAX Objects,DC=asax,DC=local', '(objectClass=person)')
        users = self.conn.entries
        logger.info('Get Ldap users')
        return users
