from .views import BrandListView, SearchProductView

from django.urls import path

urlpatterns =[
    path('/brand-list', BrandListView.as_view()),
    path('/search', SearchProductView.as_view()),
]
