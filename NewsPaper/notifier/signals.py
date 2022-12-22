from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from news.models import PostCategory
from .tasks import send_new_post


@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers_new_post(sender, instance, action, **kwargs):
    if action == 'post_add':
        send_new_post.delay(instance.id, list(kwargs['pk_set']))
