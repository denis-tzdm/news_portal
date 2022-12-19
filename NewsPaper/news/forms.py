from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import Group

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


class BasicSignupForm(SignupForm):
    def save(self, request):
        new_user = super(BasicSignupForm, self).save(request)
        default_group = Group.objects.get(name='common')
        default_group.user_set.add(new_user)
        return new_user
