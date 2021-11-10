from django.urls import path

from teams import views

urlpatterns = [
    path('teams/', views.NotJoinedTeamList.as_view()),
    path('teams/new', views.TeamList.as_view()),
    path('teams/joined', views.JoinedTeamList.as_view()),
    path('teams/<int:pk>/', views.TeamDetail.as_view()),
    path('teams/users/<int:pk>/', views.UserTeamList.as_view()),
    path('teams/<int:pk>/emissions/', views.TeamEmissions.as_view()),
    path('teams/<int:pk>/emissions/week/',
         views.TeamEmissionsThisWeek.as_view()),
    path('teams/<int:pk>/members/', views.MembersOfTeam.as_view()),
    path('join_team/', views.Join.as_view()),
    path('teams/<int:pk>/leave/', views.Leave.as_view()),
    path('rivals/<int:pk>/', views.Rivals.as_view()),
    path('rivals/<int:pk>/other/', views.NotRivals.as_view()),
    path('rival_requests/new/', views.NewRivalRequests.as_view()),
    path('rival_requests/<int:pk>/', views.RivalRequests.as_view()),
    path('rival_requests/<int:pk>/update/',
         views.RivalUpdateAndDeleteRequests.as_view()),


]
