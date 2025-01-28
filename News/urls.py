from django.urls import path
from .views import (PostsList, PostDetail, PostSearch,
                    NewsCreate, NewsEdit, NewsDelete,
                    ArticlesCreate, ArticlesEdit, ArticlesDelete,
                    NewsListAPIView, ArticlesListAPIView, PostDetailAPIView)

# app_name = 'news'

urlpatterns = [

   path('', PostsList.as_view(), name='posts_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search/', PostSearch.as_view(), name='post_search'),
   path('news/', NewsListAPIView.as_view(), name='news_list_api'),
   path('articles/', ArticlesListAPIView.as_view(), name='articles_list_api'),
   path('posts/<int:pk>/', PostDetailAPIView.as_view(), name='post_detail_api'),  # API для одного поста
   path('create/', NewsCreate.as_view(), name='news_create'),
   path('<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('articles/create', ArticlesCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/edit/', ArticlesEdit.as_view(), name='articles_edit'),
   path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),
]
