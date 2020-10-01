from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum, Count
from django.db.transaction import atomic
from django.forms import ModelChoiceField
from django.shortcuts import get_object_or_404

from movies.models import (
    Movies,
    Members,
    Categories,
    Vote, Collection
)
from dateutil.relativedelta import relativedelta
import locale
from django.db.models.functions import datetime
from service_objects.services import Service
from movies.forms import CommentForm
import logging


locale.setlocale(locale.LC_ALL, '')
logger = logging.getLogger(__name__)


class GetMovieDetail(Service):
    """
    We receive and process all the data about the film, then pass it to views
    """
    movie = ModelChoiceField(queryset=Movies.objects.all())

    def process(self):
        movie = self.cleaned_data['movie']

        genres = self._get_genres(movie)
        directors = self._get_directors(movie)
        actors = self._get_actors(movie)
        fees_in_world = self._get_fees_in_world(movie)
        budget = self._get_budget(movie)
        fees_in_usa = self._get_fees_in_usa(movie)
        movie_shot = self._get_movie_shot(movie)
        movie_shots = self._get_movie_shots(movie)
        comments = movie.comments.all()
        likes_count = movie.votes.likes().count()
        dislikes_count = movie.votes.dislikes().count()

        context = {
                "movie_id": movie.id,
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
                "comments": comments,
                "likes_count": likes_count,
                "dislikes_count": dislikes_count
        }

        return context

    @staticmethod
    def _get_genres(movie):
        return ', '.join([q.title for q in movie.categories.filter(parent__title='жанры')])

    @staticmethod
    def _get_directors(movie):
        directors = ', '.join(
            [f'<a class="text-decoration-none person" href="{q.get_absolute_url()}"><span itemprop="director">'
             f'{q.full_name}</span></a>' for q in movie.directors.all()])

        return directors

    @staticmethod
    def _get_actors(movie):
        actors = ', '.join(
            [f'<a class="text-decoration-none person" href="{q.get_absolute_url()}"><span itemprop="actor">'
             f'{q.full_name}</span></a>' for q in movie.actors.all()])

        return actors

    @staticmethod
    def _get_fees_in_world(movie):
        if movie.fees_in_world:
            fees_in_world = f'{movie.fees_in_world:n}'
        else:
            fees_in_world = movie.fees_in_world

        return fees_in_world

    @staticmethod
    def _get_budget(movie):
        if movie.budget:
            budget = f'{movie.budget:n}'
        else:
            budget = movie.budget

        return budget

    @staticmethod
    def _get_fees_in_usa(movie):
        if movie.fees_in_usa:
            fees_in_usa = f'{movie.fees_in_usa:n}'
        else:
            fees_in_usa = movie.fees_in_usa

        return fees_in_usa

    @staticmethod
    def _get_movie_shot(movie):
        return movie.movieshots_set.last().image.url

    @staticmethod
    def _get_movie_shots(movie):
        return [mov_shot.image.url for mov_shot in movie.movieshots_set.all()]


class GetMemberDetail(Service):
    """
    We receive and process all the data about the actor or director,
    then in the finished form we transmit to views
    """
    member = ModelChoiceField(queryset=Members.objects.all())

    def process(self):
        member = self.cleaned_data['member']
        name = member.full_name
        total_movies = member.total_movies
        description = member.description
        birthday = member.birthday
        image = member.image.url
        categories = self._get_categories(member)
        roles = self._get_roles(member)
        movies_actors = member.film_actor.all()
        movies_directors = member.film_director.all()
        comments = member.comments.all()
        likes_count = member.votes.likes().count()
        dislikes_count = member.votes.dislikes().count()

        context = {
            "member_id": member.id,
            "name": name,
            "total_movies": total_movies,
            "description": description,
            "birthday": birthday,
            "image": image,
            "categories": categories,
            "roles": roles,
            "movies_actors": movies_actors,
            "movies_directors": movies_directors,
            "comments": comments,
            "likes_count": likes_count,
            "dislikes_count": dislikes_count
        }

        return context

    @staticmethod
    def _get_categories(member):
        return ', '.join([q.title for q in member.categories.all()])

    @staticmethod
    def _get_roles(member):
        return ', '.join([q.role for q in member.roles.all()])


def get_movies_and_series_index_slider(limit=None):
    """
    QuerySet films and series for the main slider on the main page.
    Sampling: films released in the last 4 months and sorted by rating descending Kinopoisk
    :param limit: int, None
    :return: QuerySet
    """
    index_slider_movies = Movies.objects.filter(
        world_premiere__range=(datetime.datetime.today() + relativedelta(months=-10), datetime.datetime.today())) \
        .filter(rating_kp__isnull=False) \
        .order_by('-rating_kp')

    if limit:
        return index_slider_movies[:limit]

    return index_slider_movies


def get_movies_and_series_future_premieres(limit=None):
    """
    QuerySet films and series of future premieres.
    Sampling: films and series not released until today
    :param limit: int, None
    :return: QuerySet
    """
    movie_premieres = Movies.objects.filter(world_premiere__gt=datetime.datetime.now()).order_by('world_premiere')

    if limit:
        return movie_premieres[:limit]

    return movie_premieres


def get_movies_now_in_cinema():
    """
    QuerySet of films going to the movies now.
    Sampling: films released no earlier than 1.5 months ago
    :return: QuerySet
    """
    movies_now_in_cinema = Movies.objects.filter(
        rf_premiere__range=(datetime.datetime.today() + relativedelta(months=-2, days=-15),
                            datetime.datetime.today())
    ).filter(categories__slug='movies')

    return movies_now_in_cinema


def get_popular_movies(limit=None):
    """
    QuerySet of popular films according to kinopoisk.
    Sample: films released no earlier than 5 years ago and no later than 2 months ago,
    sorted in descending order of Kinopoisk
    :param limit: int, None
    :return: QuerySet
    """
    popular_movies = Movies.objects.filter(
        world_premiere__range=(datetime.datetime.today() + relativedelta(years=-5),
                               datetime.datetime.today() + relativedelta(months=-2))
    ).filter(
        rating_imdb__gte=5,
        categories__slug='movies'
    ).order_by(
        '-rating_kp'
    ).exclude(categories__slug='cartoon')

    if limit:
        return popular_movies[:limit]

    return popular_movies


def get_popular_series(limit=None):
    """
    QuerySet of popular series according to IMDB.
    Sample: films released no earlier than 10 years ago and no later than 2 months ago,
    sorted in descending order of IMDB
    :param limit: int, None
    :return: QuerySet
    """
    popular_series = Movies.objects.filter(
        world_premiere__range=(datetime.datetime.today() + relativedelta(years=-10),
                               datetime.datetime.today() + relativedelta(months=-2))) \
        .filter(rating_imdb__gte=5) \
        .order_by('-rating_imdb') \
        .filter(categories__title='сериалы')
    if limit:
        return popular_series[:limit]

    return popular_series


def get_new_movies_and_series(limit=None):
    """
    New movies and series.
    Sample: films and series released no earlier than 8 months ago and no later than 2 months ago,
    IMDB rating more than 5 and sorted by world release date
    :param limit: int, None
    :return: QuerySet
    """
    new_movies = Movies.objects.filter(
        world_premiere__range=(datetime.datetime.today() + relativedelta(months=-8),
                               datetime.datetime.today() + relativedelta(months=-2))) \
        .order_by('-world_premiere') \
        .filter(world_premiere__isnull=False) \
        .filter(rating_imdb__gte=5)

    if limit:
        return new_movies[:limit]

    return new_movies


def get_movies_list_by_genre(slug: str, category_type: str):
    """
    All films of a particular genre.
    :param slug: str
    :param category_type: is categories slug "movies" or "series"
    :return: QuerySet
    """

    return Movies.objects.filter(categories__slug=slug).filter(categories__slug=category_type).distinct()


def get_movies_list_by_years(year: iter, category_type: str):
    """
    All films are of the same year or range of years.
    Examples: 2005, 2010-2020.
    :param year: list
    :param category_type: is categories slug "movies" or "series"
    :return: QuerySet
    """

    return Movies.objects.filter(world_premiere__year__range=(year[0], year[-1]),
                                 categories__slug=category_type).distinct()


def get_movies_list_by_country(country: str, category_type: str):
    """
    All films are in one country.
    :param country: str
    :param category_type: is categories slug "movies" or "series"
    :return: QuerySet
    """

    return Movies.objects.filter(country__icontains=country,
                                 categories__slug=category_type).distinct()


def get_movies_and_series_recent_premieres():
    """
    Recent movie and series premieres.
    Sampling: films released no earlier than 6 months ago and sorted by world release date.
    :return: QuerySet
    """
    return Movies.objects.filter(
        world_premiere__range=(datetime.datetime.today() + relativedelta(months=-6),
                               datetime.datetime.today())
    ).order_by('-world_premiere').distinct()


def get_expected_movies():
    """
    We take all movies with future premieres and sort them by
    descending the number of positive votes posted by users
    :return: QuerySet
    """
    expected_movies = Movies.objects.filter(world_premiere__gt=datetime.datetime.now()).annotate(
        votes_sum=Sum('votes__vote'))
    # if there are no likes, then we output future premieres without sorting
    if expected_movies.exclude(votes_sum=None).exists():
        expected_movies = expected_movies.exclude(votes_sum=None).order_by('-votes_sum').distinct()

    return expected_movies


def get_movie_of_month():
    """
    We sort movies by the number of positive votes and comments left over the past month
    :return: QuerySet
    """
    movie_of_month = Movies.objects.filter(
        votes__liked_on__range=(datetime.datetime.today() + relativedelta(months=-1),
                                datetime.datetime.today()),
        comments__commented_on__range=(datetime.datetime.today() + relativedelta(months=-1),
                                       datetime.datetime.today()),
    ).annotate(
        votes_sum=Sum('votes__vote'),
        comments_count=Count('comments__text')
    ).exclude(
        votes_sum=None
    ).order_by('-votes_sum', '-comments_count').distinct()

    return movie_of_month


def get_movies_interesting_today():
    """
    Films and series with the highest number of likes and comments for the previous day
    :return: QuerySet
    """


def get_top_movies_and_series_russian_classics():
    """
    Top list of films and series made in Russia and the USSR.
    Sampling: films released no later than 3 months ago and sorted in descending order of rating of Kinopoisk
    :return: QuerySet
    """
    russian_classics = Movies.objects.filter(
        country__icontains=('СССР' and 'Россия')
    ).exclude(
        rf_premiere__gt=datetime.datetime.today() + relativedelta(months=-3)
    ).exclude(
        rating_kp__isnull=True
    ).exclude(
        rf_premiere__isnull=True
    ).order_by('-rating_kp').distinct()

    return russian_classics


def get_top_movies_and_series_foreign_classics():
    """
    Top list of films and series filmed abroad.
    Sampling: films released no later than 3 months ago and sorted in descending order of rating IMDB
    :return: QuerySet
    """
    foreign_classics = Movies.objects.exclude(
        country='СССР' and 'Россия'
    ).exclude(
        world_premiere__gt=datetime.datetime.today() + relativedelta(months=-3)
    ).exclude(
        rating_imdb__isnull=True
    ).exclude(
        world_premiere__isnull=True
    ).order_by('-rating_imdb').distinct()

    return foreign_classics


def get_top_movies_and_series_by_rating_kp():
    """
    Top list of films and series according to Kinopoisk.
    Sampling: sorted in descending order of rating Kinopoisk
    :return: QuerySet
    """
    movies_by_rating_kp = Movies.objects.exclude(
        rating_kp__isnull=True
    ).order_by('-rating_kp').distinct()

    return movies_by_rating_kp


def get_top_movies_and_series_by_rating_imdb():
    """
    Top list of films and series according to IMDB.
    Sampling: Sorted in descending order of rating IMDB
    :return: QuerySet
    """
    movies_by_rating_imdb = Movies.objects.exclude(
        rating_imdb__isnull=True
    ).order_by('-rating_imdb').distinct()

    return movies_by_rating_imdb


def get_top_cartoon():
    """
    Top list of cartoon and animated series.
    Sampling: Sorted in descending order of rating IMDB
    :return: QuerySet
    """
    movies_cartoon = Movies.objects.filter(categories__slug='cartoon')\
        .exclude(rating_imdb__isnull=True)\
        .order_by('-rating_imdb')

    return movies_cartoon


# for movie filters
class DataFilters:
    """
    Sample data for the search filter, we suggest that the user select only
    the item in each filter that is in the database.
    The output is a list.
    """

    @staticmethod
    def get_categories():
        categories = Categories.objects.exclude(parent__slug='genres')\
            .exclude(slug='genres')\
            .order_by('title')\
            .values('title', 'slug')\
            .distinct()

        return list(categories)

    @staticmethod
    def get_years():
        years = Movies.objects.exclude(world_premiere__isnull=True)\
            .exclude(world_premiere__exact=None)\
            .values_list('world_premiere__year', flat=True)\
            .order_by('-world_premiere__year')\
            .distinct()

        return list(years)

    @staticmethod
    def get_countries():
        countries = Movies.objects.exclude(country__isnull=True). \
            exclude(country__exact='')\
            .order_by('country')\
            .values_list('country', flat=True)\
            .distinct()

        return list(countries)

    @staticmethod
    def get_genres():
        genres = Categories.objects.filter(parent__slug='genres')\
            .order_by('title')\
            .values('title', 'slug')\
            .distinct()

        return list(genres)


def add_comment(request_post, content_object):
    """
    Comment form validation and entry into the database
    :param request_post:
    :param content_object:
    :return:
    """
    form = CommentForm(request_post)
    if form.is_valid():
        form = form.save(commit=False)
        form.content_object = content_object
        if request_post.get('parent', None):
            form.parent_id = int(request_post.get('parent'))
        form.save()
    else:
        logger.error(form.errors)


@atomic
def add_vote(obj, vote_type: int, user):
    """
    Adding like or disliking. If the user did not add anything, then create.
    If the user has already liked or disliked and tries to do it again,
    the entry is deleted.
    If the user wants to change his / her own, then we update.
    :param obj:
    :param vote_type:
    :param user:
    :return:
    """
    try:
        like_dislike = Vote.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id,
                                        user=user)
        if like_dislike.vote is not vote_type:
            like_dislike.vote = vote_type
            like_dislike.save(update_fields=['vote'])
            result = True
        else:
            like_dislike.delete()
            result = False
    except Vote.DoesNotExist:
        obj.votes.create(user=user, vote=vote_type)
        result = True

    context = {
        "result": result,
        "like_count": obj.votes.likes().count(),
        "dislike_count": obj.votes.dislikes().count(),
    }

    return context


def add_favorite_movies(movie_id, user_id):
    """
    Add movies in User favorite list.
    :param movie_id:
    :param user_id:
    :return:
    """

    movie = get_object_or_404(Movies, pk=movie_id)
    user = get_object_or_404(User, pk=user_id)
    if user.profile.favorites.filter(pk=movie.id).exists():
        user.profile.favorites.remove(movie)
    else:
        user.profile.favorites.add(movie)


def get_popular_collection():
    """
    Collections of films and serials.
    Sample: sorted in descending order by the number of positive votes.
    :return: qs
    """
    collections = Collection.objects.exclude(
        movies__isnull=False
    ).annotate(
        votes_sum=Sum('votes__vote')
    ).order_by('-votes_sum')

    return collections


def get_movies_of_collection(collection_id):
    """
    Get all the films in the collection.
    :param collection_id:
    :return: qs
    """
    collection = get_object_or_404(Collection, pk=collection_id)
    movies = collection.movies.all().prefetch_related()
    return movies
