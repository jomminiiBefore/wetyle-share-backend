from .views import BrandListView, ProductView, PopularProductView, ProductSizeView

from django.urls import path

urlpatterns =[
    path('/brand-list', BrandListView.as_view()),
    path('/<int:product_id>', ProductView.as_view()),
    path('/popular/<int:product_id>', PopularProductView.as_view()),  
    path('/size/<int:product_id>', ProductSizeView.as_view())    
]