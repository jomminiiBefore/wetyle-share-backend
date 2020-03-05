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
    ImageUploadView,
    SearchCollectionView,
    CollectionUploadView,
    FollowingCardView,
    NewCardView
)

urlpatterns = [
    path('/style/<int:style_id>', StyleView.as_view()),
    path('/dailylook', DailyLookCardView.as_view()),
    path('/style/upload', StyleUploadView.as_view()),
    path('/upload/image', ImageUploadView.as_view()),
    path('/style/comment/<int:style_id>', StyleCommentView.as_view()),
    path('/style/like/<int:style_id>', StyleLikeView.as_view()),
    path('/popular', PopularCardView.as_view()),
    path('/collection/<int:collection_id>', CollectionView.as_view()),
    path('/collection/follow/<int:collection_id>', CollectionFollowView.as_view()),
    path('/collection/search', SearchCollectionView.as_view()),
    path('/dailylook/collection', DailyLookCollectionView.as_view()),
    path('/collection/upload', CollectionUploadView.as_view()),
    path('/following', FollowingCardView.as_view()),
    path('/new-card', NewCardView.as_view()),
]
