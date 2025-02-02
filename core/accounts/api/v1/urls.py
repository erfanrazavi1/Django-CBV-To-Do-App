from django.urls import path , include
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView , TokenVerifyView

urlpatterns = [
    #registration
    path('registration/' ,RegistrationApiView.as_view() , name = 'registration' ),


    #token login
    path('token/login/' , CustomAuthToken.as_view() , name = 'token-login'),
    path('token/logout/' , CustomDiscardAuthToken.as_view() , name = 'token-logout'),

    #jwt login
    # path('jwt/create/' , CustomTokenObtainPairView.as_view() , name="jwt-create"),
    # path('jwt/refresh/' , TokenRefreshView.as_view() , name="jwt-refresh"),
    # path('jwt/verify/' , TokenVerifyView.as_view() , name="jwt-verify"),
]
