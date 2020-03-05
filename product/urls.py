from .views import BrandListView, PopularBrandView

from django.urls import path

urlpatterns =[
    path('/brand-list', BrandListView.as_view()),
    path('/brand/popular', PopularBrandView.as_view()),
]
