from django.forms import widgets
from django_filters import FilterSet, ModelMultipleChoiceFilter, CharFilter, DateFilter

from .models import Post, Category


class PostFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок содержит'
    )
    create_ts = DateFilter(
        field_name='create_ts',
        lookup_expr='date__gt',
        label='Опубликован после',
        widget=widgets.DateInput(attrs={
                                     'class': 'datepicker',
                                     'type': 'date'
                                 })
    )
    categories = ModelMultipleChoiceFilter(
        field_name='postcategory__category',
        queryset=Category.objects.all(),
        label='Теги',
    )

    class Meta:
        model = Post
        fields = ['title', 'create_ts', 'categories']
