from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from core.views import BaseView
from django_filters.views import FilterView
from movies.models import Members, Movies, Comments, Vote
from movies.services import services
from movies.services.filters import MovieFilter


class MoviesIndexView(BaseView):
    """
    The main page of the "Search Movies" site, only the most important is displayed.
    """

    def get(self, request):
        context = {
            "movie_premieres": services.get_movies_and_series_future_premieres(limit=8),
            "index_slider_movies": services.get_movies_and_series_index_slider(limit=15),
            "movies_now_in_cinema": services.get_movies_now_in_cinema(),
            "new_movies": services.get_new_movies_and_series(limit=16),
            "popular_movies": services.get_popular_movies(limit=16),
            "popular_series": services.get_popular_series(limit=16),
        }
        return render(request, "movies/index.html", context)


class MovieDetailsView(BaseView):
    """
    Detailed information about the film, accessed through id in the database,
    if such an object does not exist, then 404
    """

    def get(self, request, pk):
        movie = get_object_or_404(Movies, pk=pk)
        context = services.GetMovieDetail.execute({
            "movie": movie.id
        })
        return render(request, "movies/movie_detail.html", context)


class SeriesDetailsView(BaseView):
    """
    Detailed information about the series, accessed through id in the database,
    if such an object does not exist, then 404
    """

    def get(self, request, pk):
        response = "series %s."
        return HttpResponse(response % pk)


class MemberDetailsView(BaseView):
    """
    Detailed information about filming participants, accessed through id in the database,
    if such an object does not exist, then 404
    """

    def get(self, request, pk):
        member = get_object_or_404(Members, pk=pk)
        context = services.GetMemberDetail.execute({
            "member": member.id
        })
        return render(request, "movies/member.html", context)


class FilteredListView(FilterView, BaseView):
    """
    Your Base View, to add general functionality, then most of the View is inherited from it.
    """
    page_title = None
    filterset_class = MovieFilter
    paginate_by = 32
    template_name = "movies/movie_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context


class MoviesByYearView(FilteredListView):
    """
    List of films released in the year or in the range of years
    """
    page_title = "Фильмы по годам"

    def get_queryset(self):
        # data extraction
        year = self.kwargs['year'].split('-')
        # check for length. The year cannot be more or less than four digits
        if (len(year[0]) and len(year[-1])) != 4:
            raise Http404()
        try:
            queryset = services.get_movies_list_by_years(year, category_type='movies')
        except ValueError:
            # if they try to enter something that does not look like a date, then 404
            raise Http404()

        return queryset


class MoviesByCountryView(FilteredListView):
    """
    list of films released in a particular country
    """
    page_title = "Фильмы по странам"

    def get_queryset(self):
        try:
            queryset = services.get_movies_list_by_country(self.kwargs['country'], category_type='movies')
        except ValueError:
            raise Http404()

        return queryset


class MoviesByGenreView(FilteredListView):
    """
    list of films with a specific genre
    """
    page_title = "Фильмы по жанрам"

    def get_queryset(self):
        try:
            queryset = services.get_movies_list_by_genre(self.kwargs['slug'], category_type='movies')
        except ValueError:
            raise Http404()

        return queryset


class CartoonView(FilteredListView):
    """
    Top list of cartoons
    """
    queryset = services.get_top_cartoon()
    page_title = "Топ мультфильмы"


class ByRatingImdbView(FilteredListView):
    """
    Top list of movies and series according to IMDB
    """
    queryset = services.get_top_movies_and_series_by_rating_imdb()
    page_title = "По рейтингу IMDB"


class ByRatingKinopoiskView(FilteredListView):
    """
    Top list of movies and series according to Kinopoisk version
    """
    queryset = services.get_top_movies_and_series_by_rating_kp()
    page_title = "По рейтингу Кинопоиска"


class ForeignClassicsView(FilteredListView):
    """
    Top list of films and series filmed abroad.
    """
    queryset = services.get_top_movies_and_series_foreign_classics()
    page_title = "Зарубежная классика"


class RussianClassicsView(FilteredListView):
    """
    Top list of films and series made in Russia and the USSR.
    """
    queryset = services.get_top_movies_and_series_russian_classics()
    page_title = "Российская классика"


class PopularSeriesView(FilteredListView):
    """
    List of popular series according to IMDB.
    """
    queryset = services.get_popular_series()
    page_title = "Популярные Сериалы"


class FuturePremieresView(FilteredListView):
    """
    List films and series of future premieres.
    """
    queryset = services.get_movies_and_series_future_premieres()
    page_title = "Скоро Премьеры"


class RecentPremieresView(FilteredListView):
    """
    Recent movie and series premieres.
    """
    queryset = services.get_movies_and_series_recent_premieres()
    page_title = "Недавние премьеры"


class PopularMoviesView(FilteredListView):
    """
    List of popular films according to kinopoisk.
    """
    queryset = services.get_popular_movies()
    page_title = "Популярные фильмы"


class ExpectedMoviesView(FilteredListView):
    """
    List of future premieres with the most likes.
    """
    queryset = services.get_expected_movies()
    page_title = "Ожидаемые фильмы"


class InterestingTodayView(FilteredListView):
    """
    List films and series with the highest number of likes and comments for the previous day
    """
    queryset = services.get_movies_interesting_today()
    page_title = "Интересное сегодня"


class NewMoviesSeriesView(FilteredListView):
    """
     New movies and series.
    """
    queryset = services.get_new_movies_and_series()
    page_title = "Новинки"


class MoviesMonthView(FilteredListView):
    """
    List of the most talked about films of the last month.
    """
    queryset = services.get_movie_of_month()
    page_title = "Фильмы месяца"


def get_filter_countries(request):
    """
    Get all the countries from the database excluding
    null and blank values
    :param request:
    :return: JSON
    """

    if request.method == "GET" and request.is_ajax():
        countries = services.DataFilters.get_countries()
        data = {
            "countries": countries,
        }
        return JsonResponse(data, status=200)


def get_filter_categories(request):
    """
    Get all the categories from the database excluding
    null and blank values
    :param request:
    :return: JSON
    """

    if request.method == "GET" and request.is_ajax():
        categories = services.DataFilters.get_categories()
        data = {
            "categories": categories,
        }
        return JsonResponse(data, status=200)


def get_filter_year(request):
    """
    Get all the years from the database excluding
    null and blank values
    :param request:
    :return: JSON
    """

    if request.method == "GET" and request.is_ajax():
        years = services.DataFilters.get_years()
        data = {
            "years": years,
        }
        return JsonResponse(data, status=200)


def get_filter_genres(request):
    """
    Get all the genres from the database excluding
    null and blank values
    :param request:
    :return: JSON
    """

    if request.method == "GET" and request.is_ajax():
        genres = services.DataFilters.get_genres()
        data = {
            "genres": genres,
        }
        return JsonResponse(data, status=200)


class CommentView(BaseView):
    """
    Adding comments to movies and series
    """
    model = None

    def post(self, request, pk):

        _mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST['user'] = request.user
        request.POST._mutable = _mutable

        obj = get_object_or_404(self.model, pk=pk)
        services.add_comment(request_post=request.POST, content_object=obj)
        return redirect(obj.get_absolute_url() + '#comments')


add_comment_to_movie = CommentView.as_view(model=Movies)
add_comment_to_member = CommentView.as_view(model=Members)


class VoteView(BaseView):
    """
    Like/Dislike system
    """
    model = None  # Model data - example: Movies or Comments
    vote_type = None  # Type vote: Like/Dislike

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        if request.is_ajax():
            context = services.add_vote(user=request.user,
                                        vote_type=self.vote_type,
                                        obj=obj)
            return JsonResponse(context)


add_like_to_comment = login_required(VoteView.as_view(model=Comments, vote_type=Vote.LIKE))
add_dislike_to_comment = login_required(VoteView.as_view(model=Comments, vote_type=Vote.DISLIKE))
add_like_to_movie = login_required(VoteView.as_view(model=Movies, vote_type=Vote.LIKE))
add_dislike_to_movie = login_required(VoteView.as_view(model=Movies, vote_type=Vote.DISLIKE))
add_like_to_member = login_required(VoteView.as_view(model=Members, vote_type=Vote.LIKE))
add_dislike_to_member = login_required(VoteView.as_view(model=Members, vote_type=Vote.DISLIKE))
