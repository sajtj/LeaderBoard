from django.urls import path
from .views import GamesLeaderBoardAPIView, GameDetailAPIView, UsersLeaderBoardAPIView

urlpatterns = [
    path('gamesleaderboard/<int:pk_l>/', GamesLeaderBoardAPIView.as_view(), name='Game-LeaderBoard'),
    path('gamesleaderboard/<int:pk_l>/<int:pk_g>/', GameDetailAPIView.as_view(), name='Game-Detail'),
    path('usersleaderboard/<int:pk_l>/', UsersLeaderBoardAPIView.as_view(), name='User-LeaderBoard'),
]
