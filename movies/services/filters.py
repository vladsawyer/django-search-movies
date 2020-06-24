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

    sort_by = filters.OrderingFilter(
        fields={
            ('rating_kp', 'rating_kp'),
            ('world_premiere__year', 'year'),
            ('rating_kp', 'rating_kp'),
        }
    )

    class Meta:
        model = Movies
        fields = ['country', 'year', 'categories', 'genres', 'sort_by']
