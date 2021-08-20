from django.urls import path
from posts import views

urlpatterns = [
    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('likes', views.Likes.as_view()),
    path('likes/post/<int:pk>', views.LikeList.as_view()),
    path('likes/<int:pk>', views.LikeDelete.as_view()),
    path('comment', views.Comment.as_view()),
    path('comments/<int:pk>', views.CommentsDelete.as_view()),
    path('comments/<int:pk>', views.CommentList.as_view())
]