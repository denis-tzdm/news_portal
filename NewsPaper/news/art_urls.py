from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostEdit, PostDelete


urlpatterns = [
   path('create/', PostCreate.as_view(), name='article_create'),
   path('<int:pk>/edit', PostEdit.as_view(), name='article_edit'),
   path('<int:pk>/delete', PostDelete.as_view(), name='article_delete'),
]