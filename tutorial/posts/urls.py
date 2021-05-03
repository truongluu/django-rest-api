from os import name
from django.urls import path
from .class_based_views import PostList, PostDetail

urlpatterns = [
    path('posts/', PostList.as_view()),
    path('posts/<int:pk>/', PostDetail.as_view()),
]
