from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from movies.models import *
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
    """movies list certain category or genre or years"""
    def get(self, request, country=None, year=None, slug=None):
        if country:
            try:
                return render(request, "movies/movie_list.html", services.get_movie_list_by_country(country))
            except ValueError:
                raise Http404()
        elif year:
            try:
                year = year.split('-')
                if (len(year[0]) and len(year[-1])) == 4:
                    return render(request, "movies/movie_list.html", services.get_movie_list_by_years(year))
                else:
                    raise Http404()
            except ValueError:
                raise Http404()
        elif slug:
            try:
                return render(request, "movies/movie_list.html", services.get_movie_list_by_genre(slug))
            except ValueError:
                raise Http404()


class MoviesTopList(View):
    pass


class MoviesList(View):
    # slugs switch case
    slug_case = {
        "popular-series": {
                "movies": services.get_popular_series(),
                "page_title": 'Популярные сериалы'
            },
        "future-premieres": {
                "movies": services.get_movies_future_premieres(),
                "page_title": 'Скоро Премьеры'
            },
        "recent-premieres": {
            "movies": services.get_movies_recent_premieres(),
            "page_title": 'Недавние премьеры'
        },
        "popular-movies": {
                "movies": services.get_popular_movies(),
                "page_title": 'Популярные фильмы'
            },
        "expected-movies": {},
        "interesting-today": {},
        "new-movies": {
                "movies": services.get_new_movies(),
                "page_title": 'Новые фильмы'
            },
        "movies-month": {},
    }

    def get(self, request, slug):
        if slug in self.slug_case.keys():
            return render(request, "movies/movie_list.html", self.slug_case[slug])
        else:
            # temporary stub
            return Http404("Шах и мат! Такой ссылки не существует.")
