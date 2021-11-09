from django.urls import path

from challenges import views

urlpatterns = [
    path('challenges/', views.ChallengeList.as_view()),
    path('challenges/<int:pk>/', views.ChallengeDetail.as_view()),
    path('challenges/user/', views.ChallengeUserList.as_view()),
    path('challenges/team/<int:pk>/', views.TeamChallengeList.as_view()),
    path('challenges/user/<int:pk>/completed/',
         views.CompletedChallengeList.as_view()),
    path('challenges/team/<int:pk>/completed/',
         views.CompletedTeamChallengeList.as_view()),
    path('challenges/user/self/completed/',
         views.MyCompletedChallengeList.as_view()),
    path('challenges/join/', views.ChallengeUserPost.as_view()),
    path('challenges/team/join/',
         views.ChallengeTeamPost.as_view()),
    path('challenges/team/<int:pk>/joined/',
         views.TeamChallengeJoinedList.as_view()),
    path('challenge/user/<int:pk>/', views.ChallengeUserUpdateAndDelete.as_view()),
]
