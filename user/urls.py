from django.contrib import admin
from django.urls import include, path
from .views import UserView, KakaoLoginView

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("", UserView.as_view()),
    path("<int:id>/", UserView.as_view()),
    path("kakao/login/", KakaoLoginView.as_view()),
    path("signup/", include("dj_rest_auth.registration.urls")),
]