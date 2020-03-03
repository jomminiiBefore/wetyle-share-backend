from .views import BrandListView, ProductView, PopularProductView, SearchProductView

from django.urls import path

urlpatterns =[
    path('brand-list', BrandListView.as_view()),
    path('<int:product_id>', ProductView.as_view()),
    path('popular/<int:product_id>', PopularProductView.as_view()),
    path('search', SearchProductView.as_view()),
]
