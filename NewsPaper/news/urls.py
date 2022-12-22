from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (
    PostList,
    PostDetail,
    PostCreate,
    PostEdit,
    PostDelete,
    CategoryPostList
)

urlpatterns = [
    path('', cache_page(60)(PostList.as_view()), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_details'),
    path('create/', PostCreate.as_view(), name='news_create'),
    path('<int:pk>/edit', PostEdit.as_view(), name='news_edit'),
    path('<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
    path('categories/', cache_page(60)(PostList.as_view()), name='cats_list'),
    path('categories/<int:pk>', cache_page(60)(CategoryPostList.as_view()), name='cat_post_list'),
    path('categories/<int:pk>/subscribe',
         login_required(CategoryPostList.as_view(subscribe_mode='subscribe')),
         name='cat_subscribe'),
    path('categories/<int:pk>/unsubscribe',
         login_required(CategoryPostList.as_view(subscribe_mode='unsubscribe')),
         name='cat_unsubscribe'),
]
