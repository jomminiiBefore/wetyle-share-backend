from django.urls import path
from .views import (
    StyleView,
    DailyLookCardView,
    DailyLookCollectionView,
    StyleUploadView,
    StyleCommentView,
    StyleLikeView,
    PopularCardView,
    CollectionView,
    CollectionFollowView,
    StyleImageUploadView,
    SearchCollectionView
)

urlpatterns = [
    path('/style/<int:style_id>', StyleView.as_view()),
    path('/dailylook', DailyLookCardView.as_view()),
    path('/style/upload', StyleUploadView.as_view()),
    path('style/upload/image', StyleImageUploadView.as_view()),
    path('/style/comment/<int:style_id>', StyleCommentView.as_view()),
    path('/style/like/<int:style_id>', StyleLikeView.as_view()),
    path('/popular', PopularCardView.as_view()),
    path('/collection/<int:collection_id>', CollectionView.as_view()),
    path('/collection/follow/<int:collection_id>', CollectionFollowView.as_view()),
    path('collection/search', SearchCollectionView.as_view()),
    path('dailylook/collection/', DailyLookCollectionView.as_view()),
]
