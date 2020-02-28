from user.views import SignInView, SignUpView, CheckIdView, CheckEmailView
from django.urls import path

urlpatterns = [
    path('sign-up/', SignUpView.as_view()),
    path('sign-up/checkid', CheckIdView.as_view()),
    path('sign-up/checkemail', CheckEmailView.as_view()),
    path('sign-in/', SignInView.as_view()),
]

