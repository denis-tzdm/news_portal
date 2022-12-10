from django.db import models
from django.contrib.auth.models import User


class NewsUser(User):
    @staticmethod
    def get_deleted():
        """Получить пользователя для подстановки при удалении"""
        return NewsUser.objects.get_or_create(username='Пользователь удален')[0]


class Author(models.Model):
    user = models.ForeignKey(NewsUser, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    @staticmethod
    def get_deleted():
        """Получить автора для подстановки при удалении"""
        return Author.objects.get_or_create(user=NewsUser.get_deleted())[0]

    def update_rating(self) -> None:
        """Обновить рейтинг автора, сумма:

            - рейтинг каждой статьи автора ×3;
            - рейтинг всех комментариев автора;
            - рейтинг всех комментариев к статьям автора"""
        if self.user.username == 'Пользователь удален':
            return
        self.rating = 0
        posts = Post.objects.filter(author=self).values('rating')
        for post in posts:
            self.rating += post['rating'] * 3
        author_comments = Comment.objects.filter(user=self.user).values('rating')
        for comment in author_comments:
            self.rating += comment['rating']
        post_comments = Comment.objects.filter(post__author=self).values('rating')
        for comment in post_comments:
            self.rating += comment['rating']
        self.save()


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    article = 'art'
    news = 'nws'

    TYPES = [
        (article, 'статья'),
        (news, 'новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.SET(Author.get_deleted))
    type = models.CharField(max_length=3,
                            choices=TYPES,
                            default=article)
    create_ts = models.DateTimeField(auto_now_add=True)
    title = models.TextField()
    content = models.TextField()
    rating = models.IntegerField(default=0)
    categories = models.ManyToManyField(Category, through='PostCategory')

    def like(self) -> None:
        """Повысить рейтинг поста на 1"""
        self.rating += 1
        self.save()

    def dislike(self) -> None:
        """Понизить рейтинг поста на 1"""
        self.rating -= 1
        self.save()

    def preview(self) -> str:
        """Получить превью поста (первые 124 знака и символ многоточия)"""
        return self.content[:125] + "…"


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(NewsUser, on_delete=models.SET(NewsUser.get_deleted))
    content = models.TextField()
    create_ts = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self) -> None:
        """Повысить рейтинг комментария на 1"""
        self.rating += 1
        self.save()

    def dislike(self) -> None:
        """Понизить рейтинг комментария на 1"""
        self.rating -= 1
        self.save()
