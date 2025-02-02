from rest_framework.authtoken.views import ObtainAuthToken , APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import *
from rest_framework import generics
from .serializers import CustomRegistrationSerializer
from rest_framework.response import Response


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
        user = serializer.save()
        user_obj = serializer.validated_data['user']
        # user_obj = serializer.validated_data['user']
        token , created = Token.objects.get_or_create(user=user_obj)
        data = {
            'token' : token.key,
            'user_id' : user.pk,
            'user' : user.username,
            'detail' : 'token is created successfully'

        }
        return Response(data , status=status.HTTP_201_CREATED)

class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self , request):
        try:
            request.user.auth_token.delete()
            return Response({'detail' : 'Logged out successfully'} , status=status.HTTP_200_OK)
        except (AttributeError, Token.DoesNotExist):
            return Response({"error": "Token does not exist or user is not authenticated."}, status=status.HTTP_400_BAD_REQUEST)
            
