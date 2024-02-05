from django.urls import include, path
from .views import BoardView

urlpatterns = [
    path("", BoardView.as_view()),
    path("<int:id>/", BoardView.as_view()),
]
