from django.urls import path

from posts import views

urlpatterns = [
    path('posts/', views.PostList.as_view()),
    path('posts/users/<int:pk>/', views.UserPostList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('posts/users/self/', views.MyPostList.as_view()),
    path('posts/team/<int:pk>/', views.TeamPostList.as_view()),
    path('likes/', views.Likes.as_view()),
    path('liked/<int:pk>/', views.Liked.as_view()),
    path('likes/post/<int:pk>/', views.LikeList.as_view()),
    path('likes/<int:pk>/', views.LikeDelete.as_view()),
    path('comment/', views.NewComment.as_view()),
    path('comments/<int:pk>/', views.CommentsDelete.as_view()),
    path('comments/<int:pk>/', views.CommentList.as_view())
]
