from django.urls import path
from teams import views

urlpatterns = [
    path('teams/', views.TeamList.as_view()),
    path('teams/<int:pk>/', views.TeamDetail.as_view()),
    path('members/<int:pk>/', views.MembersOfTeam.as_view()),
    path('join_team/', views.Join.as_view()),
    path('leave_team/<int:pk>', views.Leave.as_view()),
]