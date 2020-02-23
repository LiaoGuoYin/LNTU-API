from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from api import models


def md5(user):
    import hashlib
    import time
    # with server's current time to generate token
    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


class Authentication(BaseAuthentication):
    """Check HTTP header's Authorization: token"""

    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed("Authentication invalid!")
        elif not token_obj.expired:  # TODO
            pass
        else:
            return token_obj, token

    def authenticate_header(self, request):
        return "Token check failed"
