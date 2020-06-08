from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from movies.models import *
from movies.services import services
from movies import utils


# Create your views here.
class MoviesIndexView(View):
    """Movie list"""
    def get(self, request):
        return render(request, "movies/index.html", {
            "movie_premieres": services.get_movies_future_premieres(limit=8),
            "index_slider_movies": services.get_index_slider_movies(limit=15),
            "movies_now_in_cinema": services.get_movies_now_in_cinema(),
            "new_movies": services.get_new_movies_and_series(limit=16),
            "popular_movies": services.get_popular_movies(limit=16),
            "popular_series": services.get_popular_series(limit=16),
        })


class MovieDetailsView(View):
    def get(self, request, pk):
        movie = get_object_or_404(Movies, pk=pk)
        context = services.GetMovieDetail.execute({
            "movie": movie.id
        })
        return render(request, "movies/movie_detail.html", context)


class SeriesDetailsView(View):
    def get(self, request, pk):
        response = "series %s."
        return HttpResponse(response % pk)


class MemberDetailsView(View):
    def get(self, request, pk):
        member = Members.objects.get(pk=pk)
        categories = ', '.join([q.title for q in member.categories.all()])
        roles = ', '.join([q.role for q in member.roles.all()])
        return render(request, "movies/member.html", {
            "name": member.full_name,
            "total_movies": member.total_movies,
            "description": member.description,
            "birthday": member.birthday,
            "image": member.image.url,
            "categories": categories,
            "roles": roles,
        })


class MoviesCategoriesList(View):
    """movies list certain category, genre, years"""
    def get(self, request, country=None, year=None, slug=None):
        if country:
            try:
                movies = services.get_movie_list_by_country(country, category_type='movies')
                return render(request, "movies/movie_list.html", {
                    "movies": utils.get_pagination(request, queryset=movies, count_show_list=32),
                    "page_title": 'Фильмы по странам'
                })
            except ValueError:
                raise Http404()

        elif year:
            try:
                year = year.split('-')
                if (len(year[0]) and len(year[-1])) == 4:
                    movies = services.get_movie_list_by_years(year, category_type='movies')
                    return render(request, "movies/movie_list.html", {
                        "movies": utils.get_pagination(request, queryset=movies, count_show_list=32),
                        "page_title": 'Фильмы по годам'
                    })
                else:
                    raise Http404()
            except ValueError:
                raise Http404()

        elif slug:
            try:
                movies = services.get_movie_list_by_genre(slug, category_type='movies')
                return render(request, "movies/movie_list.html", {
                    "movies": utils.get_pagination(request, queryset=movies, count_show_list=32),
                    "page_title": 'Фильмы по жанрам'
                })
            except ValueError:
                raise Http404()


class MoviesTopList(View):
    message_movies_not_exists = None
    # slugs switch case
    slug_case = {
        "russian-classics": {
            "movies": services.get_top_movies_russian_classics(),
            "page_title": "Русская классика",
            "message_movies_not_exists": message_movies_not_exists
        },
        "foreign-classics": {
            "movies": services.get_top_movies_foreign_classics(),
            "page_title": "Зарубежная классика",
            "message_movies_not_exists": message_movies_not_exists
        },
        "by-rating-kp": {
            "movies": services.get_top_movies_by_rating_kp(),
            "page_title": "По рейтингу Кинопоиска",
            "message_movies_not_exists": message_movies_not_exists
        },
        "by-rating-imdb": {
            "movies": services.get_top_movies_by_rating_imdb(),
            "page_title": "По рейтингу IMDB",
            "message_movies_not_exists": message_movies_not_exists
        },
        "cartoon": {
            "movies": services.get_top_cartoon(),
            "page_title": "Топ мультфильмы",
            "message_movies_not_exists": message_movies_not_exists
        },
    }

    def get(self, request, slug):
        if slug in self.slug_case.keys():
            self.slug_case[slug]["movies"] = utils.get_pagination(request,
                                                                  queryset=self.slug_case[slug]["movies"],
                                                                  count_show_list=32)
            return render(request, "movies/movie_list.html", self.slug_case[slug])
        else:
            # temporary stub
            return Http404("Шах и мат! Такой ссылки не существует.")


class MoviesList(View):
    message_movies_not_exists = None
    # slugs switch case
    slug_case = {
        "popular-series": {
            "movies": services.get_popular_series(),
            "page_title": "Популярные сериалы",
            "message_movies_not_exists": message_movies_not_exists
        },
        "future-premieres": {
            "movies": services.get_movies_future_premieres(),
            "page_title": "Скоро Премьеры",
            "message_movies_not_exists": message_movies_not_exists
        },
        "recent-premieres": {
            "movies": services.get_movies_recent_premieres(),
            "page_title": "Недавние премьеры",
            "message_movies_not_exists": message_movies_not_exists
        },
        "popular-movies": {
            "movies": services.get_popular_movies(),
            "page_title": "Популярные фильмы",
            "message_movies_not_exists": message_movies_not_exists
        },
        "expected-movies": {
            "movies": services.get_expected_movies(),
            "page_title": "Ожидаемые фильмы",
            "message_movies_not_exists": message_movies_not_exists
        },
        "interesting-today": {
            "movies": services.get_new_movies_and_series(),
            "page_title": "Интересное сегодня",
            "message_movies_not_exists": message_movies_not_exists
        },
        "new-movies-series": {
            "movies": services.get_new_movies_and_series(),
            "page_title": "Новинки",
            "message_movies_not_exists": message_movies_not_exists
        },
        "movies-month": {
            "movies": services.get_movie_of_month(),
            "page_title": "Фильмы месяца",
            "message_movies_not_exists": message_movies_not_exists
        },
    }

    def get(self, request, slug):
        if slug in self.slug_case.keys():
            self.slug_case[slug]["movies"] = utils.get_pagination(request,
                                                                  queryset=self.slug_case[slug]["movies"],
                                                                  count_show_list=32)
            return render(request, "movies/movie_list.html", self.slug_case[slug])
        else:
            # temporary stub
            return Http404("Шах и мат! Такой ссылки не существует.")
