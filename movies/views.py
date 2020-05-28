from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from .models import *
from movies.services import services


# Create your views here.
class MoviesIndexView(View):
    """Movie list"""

    def get(self, request):
        return render(request, "movies/index.html", {
            "movie_premieres": services.get_movies_future_premieres(8),
            "index_slider_movies": services.get_index_slider_movies(15),
            "movies_now_in_cinema": services.get_movies_now_in_cinema(),
            "new_movies": services.get_new_movies(16),
            "popular_movies": services.get_popular_movies(16),
            "popular_series": services.get_popular_series(16),
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
    """movies list certain category or genre"""


class MoviesList(View):
    # slugs
    POPULAR_SERIES = 'popular-series'
    FUTURE_PREMIERES = 'future-premieres'
    RECENT_PREMIERES = 'recent-premieres'
    POPULAR_MOVIES = 'popular-movies'
    EXPECTED_MOVIES = 'expected-movies'
    INTERESTING_TODAY = 'interesting-today'
    NEW_MOVIES = 'new-movies'
    NEW_SERIES = 'new-series'
    MOVIES_OF_THE_MONTH = 'movies-month'

    def get(self, request, slug):
        if slug == self.FUTURE_PREMIERES:
            return render(request, "movies/movie_list.html", {
                "movies": services.get_movies_future_premieres(),
                "page_title": 'Скоро Премьеры'
            })

        elif slug == self.POPULAR_SERIES:
            return render(request, "movies/movie_list.html", {
                "movies": services.get_popular_series(),
                "page_title": 'Популярные сериалы'
            })
        elif slug == self.RECENT_PREMIERES:
            pass
        elif slug == self.POPULAR_MOVIES:
            return render(request, "movies/movie_list.html", {
                "movies": services.get_popular_movies(),
                "page_title": 'Популярные фильмы'
            })
        elif slug == self.EXPECTED_MOVIES:
            pass
        elif slug == self.INTERESTING_TODAY:
            pass
        elif slug == self.NEW_MOVIES:
            return render(request, "movies/movie_list.html", {
                "movies": services.get_new_movies(),
                "page_title": 'Новые фильмы'
            })
        elif slug == self.MOVIES_OF_THE_MONTH:
            pass
        else:
            # temporary stub
            return Http404("Шах и мат! Такой ссылки не существует.")
