from .views import BrandListView

from django.urls import path

urlpatterns =[
    path('brandList/', BrandListView.as_view()),
]
