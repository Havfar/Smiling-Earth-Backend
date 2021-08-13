from django.urls import path
from users import views

urlpatterns = [
    path('users/', views.UserList.as_view(), name="user lists"),
    path('users/<int:pk>/', views.UserDetail.as_view(), name="user details"),
    path('followers/<int:pk>/', views.Followers.as_view(), name="followers"),
    path('following/<int:pk>/', views.Following.as_view(), name='following'),
    path('follow/<int:pk>/', views.follow, name='follow'),

]