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
    path('challenges/<int:pk>/leave/', views.ChallengeUserDelete.as_view()),
    path('challenges/team/join/',
         views.ChallengeTeamPost.as_view()),
    path('challenges/team/<int:pk>/joined/',
         views.TeamChallengeJoinedList.as_view()),
    path('challenges/<int:challenge_pk>/team/<int:team_pk>/',
         views.ChallengeTeamDelete.as_view()),
    path('challenges/<int:pk>/progress/', views.UserProgress.as_view()),
    path('challenges/<int:challenge_pk>/team/<int:team_pk>/progress/',
         views.TeamProgress.as_view()),
    path('challenge/user/<int:pk>/', views.ChallengeUserUpdateAndDelete.as_view()),
]
