from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
import ldap3

class Autenticacion(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None

        # 1. Definir los parámetros del servidor
        server_url = 'ldap://192.9.200.51:389'
        user_dn = f"comteco\\{username}"  # Formato Downlevel Logon Name para Active Directory

        try:
            # 2. Configurar el servidor y la conexión con ldap3
            server = ldap3.Server(server_url, get_info=ldap3.ALL)
            
            # Intentar el bind (autenticación)
            with ldap3.Connection(server, user=user_dn, password=password, authentication=ldap3.SIMPLE) as conn:
                if not conn.bind():
                    # Si las credenciales son incorrectas, ldap3 no levanta excepción, devuelve False
                    return None
                
                # Opcional: Si necesitas buscar datos del usuario en el árbol LDAP
                # base_dn = 'cn=users,dc=comteco,dc=net'
                # search_filter = f'(sAMAccountName={username})'
                # conn.search(base_dn, search_filter, attributes=['mail', 'givenName', 'sn'])
                
                # 3. Si el bind fue exitoso, proceder con el login/registro en Django
                return self.user_login(username)

        except ldap3.core.exceptions.LDAPException:
            # Captura fallos de conexión, timeout o servidor caído
            return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    
    def user_login(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # Crear el usuario local en Django la primera vez que se autentica en LDAP
            user = User(username=username)
            # ¡Importante! No guardes la contraseña de red en la BD local de Django
            user.set_unusable_password() 
            user.email = f"{username}@comteco.com.bo"
            
            # OJO: Tenías user.is_active = False. Si es False, Django bloqueará 
            # al usuario inmediatamente después de loguearse. Cambiado a True.
            user.is_active = False 
            user.save()
            print("usuario creado")
            
        # Si el usuario existe pero fue desactivado manualmente en Django
        if not user.is_active:
            return None
            
        return user