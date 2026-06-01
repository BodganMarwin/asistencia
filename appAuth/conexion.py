from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
import ldap3

class Autenticacion(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):

        try:
            host = ldap3.initialize('ldap://192.9.200.51:389', bytes_mode=False)
            host.simple_bind_s('comteco\\' + username, password)
            resultado = host.search_s(u'cn=users,dc=comteco,dc=net', ldap3.SCOPE_SUBTREE, u'(cn=*)')
        except ldap3.LDAPError:
            return None
        return self.user_login(username, password)
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    
    def user_login(self,login, password):
        try:
            user = User.objects.get(username=login)
        except User.DoesNotExist:
            user = User(username=login)
            user.password = password
            user.email = login + '@comteco.com.bo'
            user.is_active = False
            user.save()
        return user