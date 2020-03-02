from .views import StyleView, DailyLookCardView

from django.urls import path

urlpatterns = [
    path('style/<int:style_id>/', StyleView.as_view()),
    path('dailylook/', DailyLookCardView.as_view()),
]
