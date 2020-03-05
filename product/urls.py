from .views import BrandListView, ProductLikeView

from django.urls import path

urlpatterns = [
    path('/brand-list', BrandListView.as_view()),
    path('/like/<int:product_id>', ProductLikeView.as_view()),
]
