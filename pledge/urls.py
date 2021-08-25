from django.urls import path
from pledge import views

urlpatterns = [
    path('pledge/', views.PledgeList.as_view()),
    path('userpledge/user/', views.CreatePledgeUser.as_view()),
    path('userpledge/user/<int:pk>', views.PledgeUserList.as_view()),
    path('userpledge/<int:pk>', views.PledgeUserDelete.as_view()),
]