from django.urls import path, include
from rest_framework_simplejwt.views import TokenBlacklistView
from .views import get_routes

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('auth/routes/', get_routes, name='routes'),
]