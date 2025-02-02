from rest_framework.authtoken.views import ObtainAuthToken , APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import *
from rest_framework import generics
from .serializers import CustomRegistrationSerializer , ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = CustomRegistrationSerializer

    def post(self,request , *args, **kwargs):
        serializer = CustomRegistrationSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token , created = Token.objects.get_or_create(user = user)
        data = {
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'message': 'User registered successfully, and token created.',
        }
        return Response(data, status=status.HTTP_201_CREATED)

class CustomAuthToken(ObtainAuthToken):


    def post(self,request,*args, **kwargs):
        serializer = self.serializer_class(data=request.data , context={'request' : request} )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token , created = Token.objects.get_or_create(user=user)
        data = {
            'token' : token.key,
            'user_id' : user.pk,
            'user' : user.username,
            'detail' : 'token is created successfully'

        }
        return Response(data , status=status.HTTP_200_OK)

class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self , request):
        try:
            request.user.auth_token.delete()
            return Response({'detail' : 'Logged out successfully'} , status=status.HTTP_200_OK)
        except (AttributeError, Token.DoesNotExist):
            return Response({"error": "Token does not exist or user is not authenticated."}, status=status.HTTP_400_BAD_REQUEST)
            
class ChangePasswordApiView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    model = User

    def get_object(self):
        obj = self.request.user
        return obj
    
    def put(self,request ,*args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data = request.data) 
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status' : 'success',
                'message' : 'Password updated successfully',
                'code' : status.HTTP_200_OK,
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)