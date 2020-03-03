from .views import BrandListView, ProductListView

from django.urls import path

urlpatterns =[
    path('brand-list/', BrandListView.as_view()),
    path('product-list/<int:product_id>/', ProductListView.as_view()),
]
