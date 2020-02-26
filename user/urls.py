from user.views import SignUpView, SignInView
from django.urls import path

urlpatterns = [
    path('/sign-up', SignUpView.as_view()),
    path('/sign-in', SignInView.as_view()),
]

