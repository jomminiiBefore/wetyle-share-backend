from django.urls import path
from .views import (
    StyleView,
    DailyLookCardView,
    StyleUploadView,
    StyleCommentView,
    StyleLikeView
)

urlpatterns = [
    path('style/<int:style_id>/', StyleView.as_view()),
    path('dailylook/', DailyLookCardView.as_view()),
    path('style/upload/', StyleUploadView.as_view()),
    path('style/comment/<int:style_id>/', StyleCommentView.as_view()),
    path('style/like/<int:style_id>/', StyleLikeView.as_view())
]
