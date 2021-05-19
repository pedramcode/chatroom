from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from urllib.parse import parse_qs
from rest_framework.authtoken.models import Token


@database_sync_to_async
def get_user(scope):
    try:
        query_string = scope.get('query_string').decode()
        params = parse_qs(query_string)
        token_key = params.get('token')[0]
        token = Token.objects.get(key=token_key)
        user = token.user
        return user
    except Exception as e:
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        scope['user'] = await get_user(scope)
        return await super().__call__(scope, receive, send)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
