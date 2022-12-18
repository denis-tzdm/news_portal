from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .filters import PostFilter
from .forms import PostForm
from .models import Post, Author


class PostList(ListView):
    model = Post
    ordering = '-create_ts'
    template_name = 'postlist.html'
    context_object_name = 'postlist'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        context['show_became_author'] = (
                self.request.user.is_authenticated
                and not context['is_author']
        )
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = get_post_type(context['post'])
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        context['show_became_author'] = (
                self.request.user.is_authenticated
                and not context['is_author']
        )
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Создание'
        path = self.request.get_full_path()
        context['type'] = get_post_type(None, path)
        return context

    def form_valid(self, form):
        new_post = form.save(commit=False)
        # new_post.author = Author.objects.get(user=self.request.user)
        path = self.request.get_full_path()
        if path == reverse('news_create'):
            new_post.type = Post.news
        else:
            new_post.type = Post.article
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(PostCreate, self).get_form_kwargs()
        kwargs['author'] = Author.objects.get(user=self.request.user)
        return kwargs


class PostEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Изменение'
        context['type'] = get_post_type(context['post'])
        return context


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Удаление'
        context['type'] = get_post_type(context['post'])
        return context


def get_post_type(post: Post | None, path: str = '') -> str:
    value = 'Запись'
    if post:
        if post.type == Post.news:
            value = 'Новость'
        elif post.type == Post.article:
            value = 'Статья'
    else:
        if path == reverse('news_create'):
            value = 'Новость'
        elif path == reverse('article_create'):
            value = 'Статья'

    return value
