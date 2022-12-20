from datetime import datetime, timedelta

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.db.models import Prefetch
from django.template.loader import render_to_string
from django.urls import reverse

from news.models import User, Post, Category, CategorySubscriber


def send_digest():
    current_site = get_current_site(request=None)
    domain = current_site.domain
    protocol = "http"
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
                'posts_link': f'{protocol}://{domain}{reverse("post_list")}'
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
