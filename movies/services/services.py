from django.forms import ModelChoiceField
from movies.models import *
from dateutil.relativedelta import relativedelta
import locale
from django.db.models.functions import datetime
from service_objects.services import Service

locale.setlocale(locale.LC_ALL, '')


class GetMovieDetail(Service):
    movie = ModelChoiceField(queryset=Movies.objects.all())

    def process(self):
        movie = self.cleaned_data['movie']
        patent_genre = Categories.objects.get(title='жанры')

        genres = ', '.join([q.title for q in movie.categories.filter(parent=patent_genre)])
        directors = ', '.join(
            [f'<a class="text-decoration-none person" href="{q.get_absolute_url()}"><span itemprop="director">'
             f'{q.full_name}</span></a>' for q in movie.directors.all()])
        actors = ', '.join(
            [f'<a class="text-decoration-none person" href="{q.get_absolute_url()}"><span itemprop="actor">'
             f'{q.full_name}</span></a>' for q in movie.actors.all()])

        if movie.fees_in_world:
            fees_in_world = f'{movie.fees_in_world:n}'
        else:
            fees_in_world = movie.fees_in_world

        if movie.budget:
            budget = f'{movie.budget:n}'
        else:
            budget = movie.budget

        if movie.fees_in_usa:
            fees_in_usa = f'{movie.fees_in_usa:n}'
        else:
            fees_in_usa = movie.fees_in_usa

        movie_shot = movie.movieshots_set.last().image.url
        movie_shots = [mov_shot.image.url for mov_shot in movie.movieshots_set.all()]

        return {
            "genres": genres,
            "directors": directors,
            "actors": actors,
            "fees_in_world": fees_in_world,
            "budget": budget,
            "fees_in_usa": fees_in_usa,
            "description": movie.description,
            "movie_shot": movie_shot,
            "movie_shots": movie_shots,
            "title": movie.title,
            "rating_imdb": movie.rating_imdb,
            "rating_kp": movie.rating_kp,
            "world_premiere": movie.world_premiere,
            "rf_premiere": movie.rf_premiere,
            "country": movie.country,
            "trailer": movie.trailer,
        }


def get_index_slider_movies(limit=None):
    index_slider_movies = Movies.objects.filter(
        world_premiere__range=(datetime.datetime.today() + relativedelta(months=-4), datetime.datetime.today())) \
        .filter(rating_kp__isnull=False) \
        .order_by('-rating_kp')

    if limit:
        return index_slider_movies[:limit]

    return index_slider_movies


def get_movie_premieres(limit=None):
    movie_premieres = Movies.objects.filter(world_premiere__gt=datetime.datetime.now()).order_by('world_premiere')

    if limit:
        return movie_premieres[:limit]

    return movie_premieres


def get_movies_now_in_cinema():
    return Movies.objects.filter(
        world_premiere__range=(datetime.datetime.today() + relativedelta(months=-1, days=-15),
                               datetime.datetime.today())
    ).filter(categories__title='фильмы')


def get_popular_movies(limit=None):
    popular_movies = Movies.objects.filter(
        world_premiere__range=(datetime.datetime.today() + relativedelta(years=-5),
                               datetime.datetime.today() + relativedelta(months=-2))) \
        .filter(rating_imdb__gte=5) \
        .order_by('-rating_kp') \
        .filter(categories__title='фильмы') \
        .exclude(categories__title='мультфильм')

    if limit:
        return popular_movies[:limit]

    return popular_movies


def get_popular_series(limit=None):
    popular_series = Movies.objects.filter(
        world_premiere__range=(datetime.datetime.today() + relativedelta(years=-10),
                               datetime.datetime.today() + relativedelta(months=-2))) \
        .filter(rating_imdb__gte=5) \
        .order_by('-rating_imdb') \
        .filter(categories__title='сериалы')
    if limit:
        return popular_series[:limit]

    return popular_series


def get_new_movies(limit=None):
    new_movies = Movies.objects.filter(
        world_premiere__range=(datetime.datetime.today() + relativedelta(months=-8),
                               datetime.datetime.today() + relativedelta(months=-2))) \
        .order_by('-world_premiere') \
        .filter(world_premiere__isnull=False) \
        .filter(rating_imdb__gte=5)

    if limit:
        return new_movies[:limit]

    return new_movies
