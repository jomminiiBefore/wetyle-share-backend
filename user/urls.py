from user.views import SignInView, SignUpView, CheckSignupIdView, CheckSignInIdView
from django.urls import path

urlpatterns = [
    path('sign-up/', SignUpView.as_view()),
    path('sign-up/checkid', CheckSignupIdView.as_view()),    
    path('sign-in/', SignInView.as_view()),
    path('sign-in/checkid', CheckSignInIdView.as_view()),
]

