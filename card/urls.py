from .views import (StyleView, DailyLookCardView, StyleUploadView,
                    StyleCommentUploadView, StyleCommentGetView,
                    StyleLikeView, PopularCardView, CollectionView)

from django.urls import path

urlpatterns = [
    path('style/<int:style_id>/', StyleView.as_view()),
    path('dailylook/', DailyLookCardView.as_view()),
    path('style/upload/', StyleUploadView.as_view()),
    path('style/comment-upload/<int:style_id>/', StyleCommentUploadView.as_view()),
    path('style/comment/<int:style_id>/', StyleCommentGetView.as_view()),
    path('style/like/<int:style_id>/', StyleLikeView.as_view()),
    path('popular/', PopularCardView.as_view()),
    path('collection/<int:collection_id>/', CollectionView.as_view()),
]
