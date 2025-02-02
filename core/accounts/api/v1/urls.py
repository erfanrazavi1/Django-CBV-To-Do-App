from django.urls import path 
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


'''
                **************************************************************

                                 Dear professor, 
                since you only mentioned adding these two topics,
                I'm not sure if you meant to complete them fully or not. Because in that case,
                I would need to use the email instead of the username.
                If this is the structure you're aiming for,
                please let me know in your feedback and I'll fix the assignment and resend it  
                                          
                ***************************************************************                                                    
     
 
'''

urlpatterns = [
    #registration
    path('registration/' ,RegistrationApiView.as_view() , name = 'registration' ),


    #token login
    path('token/login/' , CustomAuthToken.as_view() , name = 'token-login'),
    path('token/logout/' , CustomDiscardAuthToken.as_view() , name = 'token-logout'),

    #change pass
    path('change-password/' , ChangePasswordApiView.as_view() , name = 'change-password'),
   

    #jwt login
    path('jwt/create/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
]



