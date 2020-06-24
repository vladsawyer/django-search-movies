import django_filters as filters
from movies.models import Movies


class MovieFilter(filters.FilterSet):
    year = filters.NumberFilter(
        field_name="world_premiere",
        lookup_expr='year'
    )
    categories = filters.CharFilter(
        field_name='categories__slug',
        lookup_expr='icontains'
    )
    genres = filters.CharFilter(
        field_name='categories__slug',
        lookup_expr='icontains'
    )

    country = filters.CharFilter(
        field_name='country',
        lookup_expr='icontains'
    )

    class Meta:
        model = Movies
        fields = ['country', 'year', 'categories', 'genres']
