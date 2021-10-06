from django.urls import path

from teams import views

urlpatterns = [
    path('teams/', views.NotJoinedTeamList.as_view()),
    path('teams/new', views.TeamList.as_view()),
    path('teams/joined', views.JoinedTeamList.as_view()),
    path('teams/<int:pk>/', views.TeamDetail.as_view()),
    path('teams/<int:pk>/emissions/', views.TeamEmissions.as_view()),

    path('teams/<int:pk>/members/', views.MembersOfTeam.as_view()),
    path('join_team/', views.Join.as_view()),
    path('leave_team/<int:pk>', views.Leave.as_view()),
    path('rivals/<int:pk>/', views.Rivals.as_view()),
    path('rival_requests/<int:pk>', views.RivalRequests.as_view())
]
