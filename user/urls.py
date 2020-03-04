from user.views import SignInView, SignUpView, CheckSignUpIdView, CheckSignInIdView, UserFollowView
from django.urls import path

urlpatterns = [
    path('/sign-up', SignUpView.as_view()),
    path('/sign-up/checkid', CheckSignUpIdView.as_view()),
    path('/sign-in', SignInView.as_view()),
    path('/follow/<int:followee_id>', UserFollowView.as_view()), 
    path('/sign-in/checkid', CheckSignInIdView.as_view()),
]

