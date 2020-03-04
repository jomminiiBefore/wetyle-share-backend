from .views import BrandListView, ProductView, PopularProductView, SearchProductView

from django.urls import path

urlpatterns =[
    path('/brand-list', BrandListView.as_view()),
]
