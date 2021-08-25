from django.urls import path
from challenges import views

urlpatterns = [
    path('challenges/', views.ChallengeList.as_view()),
    path('challenges/<int:pk>/', views.ChallengeDetail.as_view()),
    path('challenge/user/', views.ChallengeUserPost.as_view()),
    path('challenge/user/<int:pk>', views.ChallengeUserUpdateAndDelete.as_view()),
]
