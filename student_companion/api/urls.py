from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token 
from api import views

urlpatterns = [
    path('/decks/',views.DeckModelList.as_view()),
    path('/decks/new/',views.DeckManager.as_view()),
    path('/get_logged_in_user/',views.LoggedinUserDetail.as_view()),
    path('/user/',views.UserDetail.as_view()),
    path('/friends/new/',views.FriendDetail.as_view()),
    path('/friends/list/',views.FriendList.as_view()),
    path('/leaderboard/',views.LeaderboardList.as_view()),
    path('/card/new/',views.NewFlashCardList.as_view()),
    path('/card/',views.ExistingFlashCardsList.as_view()),
    path('/card/revise/',views.GetTodaysRevisionFlashCardforDeck.as_view()),
    path('/login/', views.CustomAuthToken.as_view(), name='api_token_auth'),
    path('/register/', views.RegisterView.as_view(), name='auth_register'),
    path('/logout/', views.Logout.as_view()),
    path('/card/savestart/',views.SaveStart.as_view()),
    path('/card/savefinish/',views.SaveFinish.as_view()),
]