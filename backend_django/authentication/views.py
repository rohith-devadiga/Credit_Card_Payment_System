from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import LoginSerializer, RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    """POST /api/auth/register/ -- create a new user account."""

    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class LoginView(APIView):
    """POST /api/auth/login/ -- returns JWT access + refresh tokens."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSerializer(user).data,
            }
        )


class LogoutView(APIView):
    """POST /api/auth/logout/ -- blacklists the refresh token."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            token = RefreshToken(request.data["refresh"])
            token.blacklist()
        except (KeyError, TokenError):
            return Response({"detail": "Invalid or missing refresh token."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Logged out successfully."}, status=status.HTTP_205_RESET_CONTENT)


class MeView(APIView):
    """GET /api/auth/me/ -- protected route example, returns current user."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
