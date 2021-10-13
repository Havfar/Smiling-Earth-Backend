from django.urls import path

from pledge import views

urlpatterns = [
    path('pledge/', views.PledgeList.as_view()),
    path('pledge/user/', views.CreatePledgeUser.as_view()),
    path('pledge/user/<int:pk>/', views.PledgeUserList.as_view()),
    path('pledge/team/<int:pk>', views.PledgeTeamList.as_view()),
    path('pledge/user/delete/<int:pk>', views.PledgeUserDelete.as_view()),
]
