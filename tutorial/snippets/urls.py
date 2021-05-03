from os import name
from django.urls import path
from .views import UserList, UserDetail, UserCreate
from .class_based_views import SnippetList, SnippetDetail
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('snippets/', SnippetList.as_view()),
    path('snippets/<int:pk>/', SnippetDetail.as_view()),
    path('users/', UserList.as_view(), name='list'),
    path('users/create/', UserCreate.as_view(), name='create'),
    path('users/<int:pk>/', UserDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
