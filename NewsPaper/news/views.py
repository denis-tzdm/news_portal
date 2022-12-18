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
from .models import Post, Author, Category


class PostList(ListView):
    model = Post
    ordering = '-create_ts'
    template_name = 'news/postlist.html'
    context_object_name = 'postlist'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['category'] = ''
        context['categories'] = Category.objects.all()
        add_author_fields(self, context)
        return context


class CategoryPostList(PostList):
    def get_queryset(self):
        cat = Category.objects.filter(id=self.kwargs['pk']).first()
        queryset = Post.objects.filter(postcategory__category=cat)
        self.filterset = PostFilter(self.request.GET, queryset)
        self.filterset.form.fields.pop('categories')
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.filter(id=self.kwargs['pk']).first()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = get_post_type(context['post'])
        add_author_fields(self, context)
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'

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
    template_name = 'news/post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Изменение'
        context['type'] = get_post_type(context['post'])
        return context


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news/post_delete.html'
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


def add_author_fields(view, context):
    context['is_author'] = view.request.user.groups.filter(name='authors').exists()
    context['show_became_author'] = (
            view.request.user.is_authenticated
            and not context['is_author']
    )
