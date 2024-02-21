from django.contrib import admin
from django.urls import include, path
from .views import UserView, KakaoLoginView, UserMyView, DummyDataView, DeleteAllDataView, LevelView, ClosetView
from rest_framework_simplejwt.views import TokenVerifyView
from dj_rest_auth.jwt_auth import get_refresh_view  

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("", UserView.as_view()),
    path("<int:id>/", UserView.as_view()),
    path("my/", UserMyView.as_view()),
    path("kakao/login/", KakaoLoginView.as_view()),
    path("signup/", include("dj_rest_auth.registration.urls")),
    path("level/", LevelView.as_view()),
    path("closet/", ClosetView.as_view()),
    
    path("dummy/", DummyDataView.as_view()),
    path("delete/", DeleteAllDataView.as_view()),
]