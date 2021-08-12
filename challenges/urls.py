from django.urls import path
from challenges import views

urlpatterns = [
    path('challenges/', views.ChallengeList.as_view()),
    path('challenges/<int:pk>/', views.ChallengeList.as_view()),
]