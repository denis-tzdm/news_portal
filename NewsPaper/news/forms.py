from django import forms

from .models import Post


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('author', None)
        super(PostForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['author'].initial = self.user.id
        # todo: разрешать выбирать автора только администратору

    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'categories',
            'author',
        ]
