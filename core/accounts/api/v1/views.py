from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import generics
from .serializers import (
    CustomRegistrationSerializer,
    ChangePasswordSerializer,
    ResetPasswordSerializer,
    ResetPasswordConfirmSerializer,
)
from django.contrib.auth.models import User
from mail_templated import EmailMessage
from ..utils import EmailThread
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from jwt.exceptions import (
    ExpiredSignatureError,
    DecodeError,
    InvalidTokenError,
)

from django.conf import settings


# Registration API View for user registration and token generation
class RegistrationApiView(generics.GenericAPIView):
    """
    This API view handles the user registration process.
    It validates the input data using a serializer,
    saves the user, generates authentication tokens
    (refresh and access), and sends an email with the token.
    """

    serializer_class = CustomRegistrationSerializer

    def post(self, request, *args, **kwargs):
        # Validates and registers a new user
        serializer = CustomRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Creates a new user object and generates a token for the user
        user = serializer.save()

        # Creates tokens for the user
        token = self.get_tokens_for_user(user)

        # Sends an email with the generated token to the user
        email_obj = EmailMessage(
            "email/hello.tpl",
            {"token": token, "user": user.username},
            "erfan6235@gmail.com",
            to=["erfanr926@gmail.com"],
        )
        EmailThread(email_obj).start()  # Sends the email in a separate thread

        # Returns the response with user details and success message
        data = {
            "username": user.username,
            "message": "User registered successfully, and token created.",
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def get_tokens_for_user(self, user):
        """
        Generates refresh and access tokens for the given user.
        """
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


# Custom Auth Token API for user authentication and token generation
class CustomAuthToken(ObtainAuthToken):
    """
    This API view handles user authentication.
    It generates an authentication token for the user
    and returns the token along with the user's information.
    """

    def post(self, request, *args, **kwargs):
        # Validates input data for authentication
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        # Retrieves the authenticated user and generates the token
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        # Returns the token and user details in the response
        data = {
            "token": token.key,
            "user_id": user.pk,
            "user": user.username,
            "detail": "Token is created successfully",
        }
        return Response(data, status=status.HTTP_200_OK)


# API for discarding the user's authentication token (logging out)
class CustomDiscardAuthToken(APIView):
    """
    This API view allows the user to
    log out by deleting their authentication token.
    The user must be authenticated to perform this action.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Deletes the authentication token of the currently logged-in user
            request.user.auth_token.delete()
            return Response(
                {"detail": "Logged out successfully"},
                status=status.HTTP_200_OK,
            )
        except (AttributeError, Token.DoesNotExist):
            # Handles case when the token does not exist
            return Response(
                {"error": "Token does not exist or user is not authenticated."},
                status=status.HTTP_400_BAD_REQUEST,
            )


# API for changing the user's password
class ChangePasswordApiView(generics.GenericAPIView):
    """
    This API view allows an authenticated user
    to change their password. It validates the old password
    and updates it with the new one if valid.
    """

    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    model = User

    def get_object(self):
        """
        Retrieves the current user object for password change.
        """
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        # Validates input data for password change
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            # Checks if the old password is correct
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Changes the user's password and saves the updated user
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            # Returns success response after password change
            response = {
                "status": "success",
                "message": "Password updated successfully",
                "code": status.HTTP_200_OK,
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API for sending a password reset link to the user's email
class ResetPasswordApiView(generics.GenericAPIView):
    """
    This API view allows an authenticated user
    to initiate the password reset process by sending
    a reset password link to their provided email address.
    """

    serializer_class = ResetPasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Validates and retrieves email for password reset
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        # Sends a reset password link to the specified email
        data = {
            "email": email,
            "detail": "We have sent a reset password link to your email!",
        }

        # Generates authentication tokens for the user and sends them via email
        token = self.get_tokens_for_user(request.user)
        email_obj = EmailMessage(
            "email/reset-pass.tpl",
            {"token": token},
            "erfan6235@gmail.com",
            to=[email],
        )
        EmailThread(email_obj).start()

        # Returns the response with success details
        return Response(data, status=status.HTTP_201_CREATED)

    def get_tokens_for_user(self, user):
        """
        Generates refresh and access tokens for the given user.
        """
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


# API for confirming the passwordreset and applying the new password
class ResetPasswordConfirmApiView(generics.GenericAPIView):
    """
    This API view handles the password
    reset confirmation by validating the provided token,
    decoding it to retrieve the user's ID,
    and then allowing the user to set a new password.
    """

    serializer_class = ResetPasswordConfirmSerializer

    def post(self, request, token, *args, **kwargs):
        try:
            # Decodes the provided token to extract user information
            decoder = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoder["user_id"]
        except ExpiredSignatureError:
            return Response(
                {"error": "Token is expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except DecodeError:
            return Response(
                {"error": "Token is invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidTokenError:
            return Response(
                {"error": "Token is invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Retrieves the user based on the decoded user_id
        user_obj = get_object_or_404(User, id=user_id)

        # Validates the new password and updates the user's password
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj.set_password(serializer.validated_data["new_password"])
        user_obj.save()

        # Returns a success response after password reset
        return Response(
            {"message": "Your password has been reset successfully"},
            status=status.HTTP_200_OK,
        )
