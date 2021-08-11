from django.urls import path
from users import views

urlpatterns = [
    path('users/', views.UserList, name="users"), 
    path('posts/<int:pk>/', views.UserDetail, name="userDetailed")
]