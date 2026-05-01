from django.conf import settings
from isolate_proto import USER
from core.models import User
from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.plumbing import build_bearer_security_scheme_object
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
import jwt

JWT_SECRET_KEY = getattr(settings, 'JWT_SECRET_KEY', settings.SECRET_KEY)
JWT_ALGORITHM = 'HS256'


class TokenAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'core.authentication.TokenAuthentication'
    name = 'tokenAuth'
    match_subclasses = True
    priority = -1

    def get_security_definition(self, auto_schema):
        return build_bearer_security_scheme_object(
            header_name='Authorization',
            token_prefix='Bearer',
        )


class TokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            prefix, token = auth_header.split()
            if prefix.lower() != 'bearer':
                raise AuthenticationFailed('Formato inválido. Use Bearer <token>')
        except ValueError:
            raise AuthenticationFailed('Cabeçalho Authorization mal formatado')

        payload = self._decode_jwt(token)

        user = self._get_or_create_user(payload)

        return (user, None)

    def _decode_jwt(self, token):
        try:
            payload = jwt.decode(
                token,
                JWT_SECRET_KEY,
                algorithms=[JWT_ALGORITHM]
            )
            if 'user_id' not in payload:
                raise AuthenticationFailed('Token não contém user_id')
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expirado')
        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed(f'Token inválido: {str(e)}')

    def _get_or_create_user(self, payload):
        user_id = payload['user_id']
        try:
            user = User.objects.get(pk=user_id)
        except ObjectDoesNotExist:  
            raise AuthenticationFailed('Usuário não encontrado')

        return user