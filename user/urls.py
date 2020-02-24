from user.views import *

from django.urls import path

urlpatterns = [
    path('sign-up/', SignUpView.as_view()),
]

