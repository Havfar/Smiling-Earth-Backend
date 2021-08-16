from django.urls import path
from teams import views

urlpatterns = [
    path('teams/', views.TeamList.as_view()),
    path('teams/<int:pk>/', views.TeamDetail.as_view()),
    path('members/<int:pk>/', views.MembersOfTeam.as_view()),
]