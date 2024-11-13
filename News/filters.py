from django_filters import FilterSet, DateFilter
from .models import Post
from django import forms

class PostFilter(FilterSet):

    class Meta:
        model = Post
        fields = {
            'title': ['contains'],
            'author': ['exact'],  # foreign key
        }

    publication_date = DateFilter(
        field_name='publication_date',
        lookup_expr='gte',
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'type': 'date'})
    )

