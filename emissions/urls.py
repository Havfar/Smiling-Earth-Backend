from django.urls import path

from emissions import views

urlpatterns = [
    path('emissions/', views.UserEmission.as_view()),
    path('emissions/update/', views.UpdateOrCreateUserEmission.as_view()),
    path('emissions/team/<int:pk>/', views.TeamEmissions.as_view()),
]
