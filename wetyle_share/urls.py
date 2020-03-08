from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path('user',    include('user.urls')),
    path('product', include('product.urls')),
    path('card',    include('card.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
