from django.contrib import admin
from django.urls import include, path
import user.views as user_views

urlpatterns = [
    path("", user_views.UserView.as_view()),
    path("signup/", user_views.UserCreate.as_view()),
    path("login/", user_views.UserLogin.as_view()),
]