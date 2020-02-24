from user.views import *

from django.urls    import path

urlpatterns = [
    path('sign-up/', SignUpView.as_view()),
    path('sign-in/', SignInView.as_view()),
    path('sign-in/kakao/', KakaoSignInView.as_view()),
    path('sign-in/kakao/add/', KakaoSignInAddView.as_view()),
]


