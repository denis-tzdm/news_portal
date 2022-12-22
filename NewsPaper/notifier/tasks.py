from datetime import datetime, timedelta

from celery import shared_task
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.db.models import Prefetch
from django.template.loader import render_to_string
from django.urls import reverse

from news.models import User, Post, Category, CategorySubscriber


@shared_task
def send_new_post(post_id, pk_set):
    base_link = get_base_link()
    new_cats = Category.objects.filter(id__in=pk_set)
    post = Post.objects.get(id=post_id)
    for cat in new_cats:
        subject = f'Новая статья в категории {cat.title}'
        for subscription in CategorySubscriber.objects.filter(category=cat):
            html = render_to_string(
                'notifier/subscription.html',
                {
                    'user': subscription.subscriber,
                    'category': cat,
                    'post': post,
                    'post_link': f'{base_link}{post.get_absolute_url()}'
                }
            )
            msg = EmailMultiAlternatives(
                subject=subject,
                body=subject,
                to=[subscription.subscriber.email]
            )
            msg.attach_alternative(html, "text/html")
            msg.send()


@shared_task
def send_digest():
    base_link = get_base_link()
    last_week = last_week_range()
    frmt = '%d.%m.%y'
    subject = f'Дайджест за неделю с {last_week[0].strftime(frmt)} по {last_week[1].strftime(frmt)}'
    subs = CategorySubscriber.objects.values('subscriber').distinct()
    for sub in subs:
        cats = Category.objects.filter(
            categorysubscriber__subscriber=sub['subscriber']
        ).prefetch_related(
            Prefetch(
                'post_set',
                queryset=Post.objects.filter(create_ts__range=last_week),
                to_attr='all_posts')
        )
        # skip subscriber if no posts in any subscribed categories
        if not any(cat.all_posts for cat in cats):
            continue

        subscriber = User.objects.get(id=sub['subscriber'])

        html = render_to_string(
            'notifier/digest.html',
            {
                'user': subscriber,
                'categories': cats,
                'posts_link': f'{base_link}{reverse("post_list")}'
            }
        )
        msg = EmailMultiAlternatives(
            subject=subject,
            body=subject,
            to=[subscriber.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()


def last_week_range():
    today = datetime.today()
    last_week_end = (today - timedelta(days=(today.weekday() + 1))).replace(
        hour=23,
        minute=59,
        second=59,
        microsecond=0
    )
    last_week_start = (last_week_end - timedelta(days=6)).replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0)
    return last_week_start, last_week_end


def get_base_link() -> str:
    current_site = get_current_site(request=None)
    domain = current_site.domain
    protocol = "http"
    return f'{protocol}://{domain}'
