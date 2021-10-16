from django.urls import path
from api import views

urlpatterns = [
    path('/test/', views.TestModelList.as_view()),
    path('/test/<int:pk>/', views.TestModelDetail.as_view()),
    path('/decks/',views.DeckModelList.as_view())
]