from django.urls import path
from wordle.views import (
    WordleHistoryList,
    GameBoard,
    WordleCreateView
)

urlpatterns = [
    path("", WordleHistoryList.as_view(), name="wordle_history"),
    path("<int:pk>/game/", GameBoard.as_view(), name="game_board"),
    path("new/", WordleCreateView.as_view(), name="new_game")
]
