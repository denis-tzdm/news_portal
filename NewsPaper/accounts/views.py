from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect

from news.models import Author


@login_required
def became_author(request):
    current_user = request.user
    authors = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors.user_set.add(current_user)
    Author.objects.create(user=current_user)

    return redirect('/news')
