from .views import StyleView

from django.urls import path

urlpatterns = [
    path('style/<int:style_id>/', StyleView.as_view()),
]
