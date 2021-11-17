from django.urls import path

from users import views

urlpatterns = [
    path('users/', views.UserList.as_view(), name="user lists"),
    path('user/avatar/', views.UpdateAvatar.as_view(), name='update avatar'),
    path('users/self/', views.UserSelfDetail.as_view(), name="user self"),
    path('users/<int:pk>/', views.UserDetail.as_view(), name="user details"),
    path('followers/', views.Followers.as_view(), name="followers"),
    path('following/', views.Following.as_view(), name='following'),
    path('not-following/', views.NotFollowingList.as_view(), name='following'),
    path('follow/<int:pk>/', views.Follow.as_view(), name='follow'),
    path('unfollow/<int:pk>/', views.Unfollow.as_view(), name='unfollow'),
]
