# apps/users/views.py
from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer


class SignupView(generics.CreateAPIView):
    """
    POST /api/signup/
    Create a new user.
    Validates age >= 15, hashes password automatically.
    Optionally returns JWT.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Optional: return JWT immediately after signup
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": serializer.data,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })


class LoginView(TokenObtainPairView):
    """
    POST /api/login/
    Standard JWT login using SimpleJWT.
    Returns access + refresh token.
    """
    permission_classes = [permissions.AllowAny]


class MeView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET / PUT / PATCH / DELETE /api/me/
    Operations on the currently authenticated user.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        # Always return the currently authenticated user
        return self.request.user

    def delete(self, request, *args, **kwargs):
        """
        DELETE /api/me/
        Right to be forgotten: delete the user completely.
        """
        user = self.get_object()
        user.delete()
        return Response({"detail": "User deleted successfully."})
