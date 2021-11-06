from django.urls import path

from notifications import views

urlpatterns = [
    path('notifications/', views.NotificationsList.as_view()),
    path('notifications/<int:pk>/', views.NotificationsUpdate.as_view()),
    path('notifications/count/', views.CountUnReadNotifications.as_view()),
]
