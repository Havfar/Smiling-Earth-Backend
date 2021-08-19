
from django.urls import path
from pledge import views

urlpatterns = [
    path('pledge', views.PledgeList.as_view()),
    path('ok', views.PledgeUserList.as_view()),
    path('userpledge/<int:pk>', views.PledgeUserDelete.as_view()),
]