from .views import BrandListView, SearchProductViewi, PopularBrandView

from django.urls import path

urlpatterns =[
    path('/brand-list', BrandListView.as_view()),
    path('/search', SearchProductView.as_view()),
    path('/brand/popular', PopularBrandView.as_view()),
]
