from .views import BrandListView, SearchProductView, PopularBrandView, ProductLikeView

from django.urls import path

urlpatterns = [
    path('/brand-list', BrandListView.as_view()),
    path('/like/<int:product_id>', ProductLikeView.as_view()),
    path('/search', SearchProductView.as_view()),
    path('/brand/popular', PopularBrandView.as_view()),
]
