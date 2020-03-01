from .views import (StyleView, DailyLookCardView, StyleUploadView,
                    StyleCommentUploadView, StyleCommentGetView)

from django.urls import path

urlpatterns = [
    path('style/<int:style_id>/', StyleView.as_view()),
    path('dailylook/', DailyLookCardView.as_view()),
    path('style/upload/', StyleUploadView.as_view()),
    path('style/comment-upload/<int:style_id>/', StyleCommentUploadView.as_view()),
    path('style/comment/<int:style_id>/', StyleCommentGetView.as_view()),
]
