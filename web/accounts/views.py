from rest_framework import status, permissions, views, response
from rest_framework.authtoken.views import obtain_auth_token
from .serializers import UserSerializer

login = obtain_auth_token

class UserRegistrationView(views.APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        request.user.auth_token.delete()
        return response.Response(data={'msg': f"{request.user.username} logged out."}, status=status.HTTP_200_OK)
