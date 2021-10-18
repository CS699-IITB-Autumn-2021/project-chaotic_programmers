from django.urls import path
from api import views

urlpatterns = [
    path('/test/', views.TestModelList.as_view()),
    path('/test/<int:pk>/', views.TestModelDetail.as_view()),
    path('/decks/',views.DeckModelList.as_view()),
    path('/decks/new/',views.DeckManager.as_view()),
    path('/get_logged_in_user/',views.LoggedinUserDetail.as_view()),
    path('/user/',views.UserDetail.as_view()),
    path('/friends/new/',views.FriendDetail.as_view()),
    path('/friends/list/',views.FriendList.as_view()),
    path('/leaderboard/',views.LeaderboardList.as_view()),
]