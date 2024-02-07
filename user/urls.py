from django.contrib import admin
from django.urls import include, path
from .views import UserView, KakaoLoginView, UserMyView
from rest_framework_simplejwt.views import TokenVerifyView
from dj_rest_auth.jwt_auth import get_refresh_view  

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("", UserView.as_view()),
    path("<int:id>/", UserView.as_view()),
    path("my/", UserMyView.as_view()),
    path("kakao/login/", KakaoLoginView.as_view()),
    path("signup/", include("dj_rest_auth.registration.urls")),
]