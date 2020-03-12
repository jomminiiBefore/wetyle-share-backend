from user.views import (
    SignInView,
    SignUpView,
    CheckSignInIdView,
    CheckSignUpIdView,
    UserFollowView,
    KakaoSignInView
)

from django.urls import path

urlpatterns = [
    path('', SignUpView.as_view()),
    path('/checkid', CheckSignUpIdView.as_view()),    
    path('/sign-in', SignInView.as_view()),
    path('/follow/<int:followee_id>', UserFollowView.as_view()), 
    path('/kakao/sign-in', KakaoSignInView.as_view()),
]
