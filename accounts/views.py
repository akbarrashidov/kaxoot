from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer, AdminGoogleSerializer
from django.contrib.auth import get_user_model

# Create your views here.

User = get_user_model()

# Mobile users
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Admin Google
class AdminGoogleView(generics.CreateAPIView):
    serializer_class = AdminGoogleSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        data["role"] = "admin"
        data["is_staff"] = True
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "username": user.username,
                "access": user.access,
                "refresh": user.refresh
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)