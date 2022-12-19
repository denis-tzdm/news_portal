from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from news.models import Category, PostCategory, CategorySubscriber


@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers_new_post(sender, instance, action, **kwargs):
    if action == 'post_add':
        current_site = get_current_site(request=None)
        domain = current_site.domain
        protocol = "http"
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
                        'post_link': f'{protocol}://{domain}{instance.get_absolute_url()}'
                    }
                )
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=subject,
                    to=[subscription.subscriber.email]
                )
                msg.attach_alternative(html, "text/html")
                msg.send()
