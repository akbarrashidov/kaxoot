from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import AnonymousUser

User = get_user_model()

class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"].decode()
        token = None
        if "token=" in query_string:
            token = query_string.split("token=")[-1]

        if token:
            try:
                access_token = AccessToken(token)
                user_id = access_token["user_id"]
                user = await self.get_user(user_id)
                scope["user"] = user
                print("✅ User authenticated:", user)
            except Exception as e:
                print("❌ JWT error:", str(e))
                scope["user"] = AnonymousUser()
        else:
            print("⚠️ Token not found in query string")
            scope["user"] = AnonymousUser()

        return await self.inner(scope, receive, send)

    @staticmethod
    async def get_user(user_id):
        try:
            return await User.objects.aget(id=user_id)
        except User.DoesNotExist:
            print(f"❌ User {user_id} not found in DB")
            return AnonymousUser()
