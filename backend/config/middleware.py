from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack
from urllib.parse import parse_qs


@database_sync_to_async
def get_user(token_key):
    try:
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        return None  # Return None instead of AnonymousUser


class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        print(query_string, "query string")
        query_params = parse_qs(query_string)
        print(query_params, "query params")
        token_key = query_params.get("token", [None])[0]

        user = None  # Default to None

        # Get user associated with the token, if token is found
        if token_key:
            user = await get_user(token_key)

        # Assign user if authenticated, otherwise continue with None
        scope["user"] = user if user else AnonymousUser()

        # Proceed with the rest of the middleware chain
        return await super().__call__(scope, receive, send)


# Middleware stack including the TokenAuthMiddleware
TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
