from django.urls import include, path
from .views import BoardView, DummyBoardView, ToggleLikeView, MyLikeByIdView, MyLikeView

urlpatterns = [
    path("", BoardView.as_view()),
    path("<int:id>/", BoardView.as_view()),
    path("dummy/", DummyBoardView.as_view()),
    path("<int:id>/like/", ToggleLikeView.as_view()),
    path("mylike/", MyLikeView.as_view()),
    path("mylike/<int:id>/", MyLikeByIdView.as_view()),
]
