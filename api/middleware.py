# middleware.py

from django.utils.deprecation import MiddlewareMixin
from .models import BlacklistedToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

class TokenBlacklistMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(' ')[1]
                print(token)
                if BlacklistedToken.objects.filter(token=token).exists():
                    raise InvalidToken('Token has been blacklisted')
            except IndexError:
                pass
