from django.urls import path
from activities import views

urlpatterns = [
    path('activities/', views.ActivityList.as_view()),
    path('activities/<int:pk>/', views.ActivityDetailed.as_view()),
]