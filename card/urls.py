from .views import StyleView, DailyLookCardView, StyleUploadView

from django.urls import path

urlpatterns = [
    path('style/<int:style_id>/', StyleView.as_view()),
    path('dailylook/', DailyLookCardView.as_view()),
    path('style/upload/', StyleUploadView.as_view()),
]
