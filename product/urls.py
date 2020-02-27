from .views import BrandListView

from django.urls import path

urlpatterns =[
    path('brand-list/', BrandListView.as_view()),
]
