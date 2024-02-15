from django.urls import include, path
from .views import BoardView, DummyBoardView, ToggleLikeView

urlpatterns = [
    path("", BoardView.as_view()),
    path("<int:id>/", BoardView.as_view()),
    path("dummy/", DummyBoardView.as_view()),
    path("<int:id>/like/", ToggleLikeView.as_view()),
]
