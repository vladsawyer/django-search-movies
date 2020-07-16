from django import template
from movies.models import Movies, Categories
from dateutil.relativedelta import relativedelta
from django.db.models.functions import datetime


register = template.Library()


@register.simple_tag()
def get_genres():
    """
    List of genres from the database for header page
    :return: QuerySet
    """
    return Categories.objects.filter(parent__slug='genres')


@register.simple_tag()
def get_years():
    """
    List of years for header page
    :return: list
    """
    years = []
    one_range_date = 2015
    two_range_date = 2020
    for i in range(7):
        current_date = datetime.datetime.today() + relativedelta(years=-i)
        years.append(str(current_date.year))

    for i in range(7):
        years.append(f'{one_range_date}-{two_range_date}')
        one_range_date -= 5
        two_range_date -= 5

    return years


@register.simple_tag()
def get_countries():
    """
    List of ountries from the database for header page
    :return: list
    """
    return Movies.objects.values_list('country', flat=True).distinct()


@register.filter(name='genres')
def genres(queryset):
    return queryset.filter(parent__slug='genres')


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Return encoded URL parameters that are the same as the current
    request's parameters, only with the specified GET parameters added or changed.
    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()


@register.simple_tag()
def get_random_movie_or_series():
    """
    Random movie or series from the database
    :return: movie object
    """
    movie = Movies.objects.get_random_movie()
    return movie
