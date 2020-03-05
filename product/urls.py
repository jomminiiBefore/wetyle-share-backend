from .views import BrandListView, ProductColorView

from django.urls import path

urlpatterns = [
    path('/brand-list', BrandListView.as_view()),
    path('/color/<int:product_id>', ProductColorView.as_view()),
]
