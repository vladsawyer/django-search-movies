from django import template
from movies.models import Movies, Categories
from dateutil.relativedelta import relativedelta
from django.db.models.functions import datetime
register = template.Library()


@register.simple_tag()
def get_genres():
    return Categories.objects.filter(parent__slug='genres')


@register.simple_tag()
def get_years():
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
    return Movies.objects.values_list('country', flat=True).distinct()


@register.filter(name='genres')
def genres(queryset):
    return queryset.filter(parent__slug='genres')
