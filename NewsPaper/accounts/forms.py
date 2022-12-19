from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class BasicSignupForm(SignupForm):
    def save(self, request):
        new_user = super(BasicSignupForm, self).save(request)
        default_group = Group.objects.get(name='common')
        default_group.user_set.add(new_user)
        return new_user
