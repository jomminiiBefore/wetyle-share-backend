from .views import BrandListView, SearchProductView, PopularBrandView, ProductLikeView, ProductColorView, ProductView, PopularProductView, ProductSizeView

from django.urls import path

urlpatterns = [
    path('/brand-list', BrandListView.as_view()),
    path('/color/<int:product_id>', ProductColorView.as_view()),
    path('/like/<int:product_id>', ProductLikeView.as_view()),
    path('/search', SearchProductView.as_view()),
    path('/brand/popular', PopularBrandView.as_view()),
    path('/<int:product_id>', ProductView.as_view()),
    path('/popular', PopularProductView.as_view()),  
    path('/size/<int:product_id>', ProductSizeView.as_view())
]
