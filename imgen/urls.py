from django.urls import path
from . import views

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('init/', views.AIServerInitView.as_view(), name='init'),
    path('rmbg/', views.ImageRemoveBackgroundView.as_view(), name='remove_bg'),
    path('ladivton/', views.ImageLadiVtonView.as_view(), name='ladivton'),
]
