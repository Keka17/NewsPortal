from django_filters import FilterSet, DateFilter
from .models import Post
from django import forms
from django.utils.translation import gettext as _


class PostFilter(FilterSet):
    publication_date = DateFilter(
        field_name='publication_date',
        lookup_expr='gte',
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'type': 'date'}),
        label=_('Публикация от')  # Локализация
    )

    class Meta:
        model = Post
        fields = {
            'title': ['contains'],
            'author': ['exact'],  # foreign key
        }
        labels = {
            'title': _('Заголовок'),
            'author': _('Автор'),  # Локализация для автора
        }
