from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from news.models import Post, Category, PostCategory, CategorySubscriber


@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers_new_post(sender, instance, action, **kwargs):
    if action == 'post_add':
        new_cats = Category.objects.filter(id__in=kwargs['pk_set'])
        for cat in new_cats:
            subject = f'Новая статья в категории {cat.title}'
            for subscription in CategorySubscriber.objects.filter(category=cat):
                html = render_to_string(
                    'notifier/subscription.html',
                    {
                        'subscriber': subscription.subscriber,
                        'category': cat,
                        'post': instance,
                    }
                )
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=subject,
                    to=[subscription.subscriber.email]
                )
                msg.attach_alternative(html, "text/html")
                msg.send()
