from django.contrib import admin
from django.urls import include, path

from rest_framework_simplejwt.views import TokenRefreshView
from .views import TokenObtainPairView

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/", include("dj_rest_auth.registration.urls")),
    path("auth/", include("dj_rest_auth.urls")),
]