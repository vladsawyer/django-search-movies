from django.db.models.functions import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from .models import *
from dateutil.relativedelta import relativedelta


# Create your views here.
class MoviesIndexView(View):
    """Movie list"""

    def get(self, request):
        index_movies = Movies.objects.exclude(
            world_premiere__gte=datetime.datetime.today()
        ).filter(
            world_premiere__gte=datetime.datetime.today() + relativedelta(months=-3)
        ).filter(
            rating_kp__isnull=False
        ).order_by('-rating_kp')[:15]

        premieres = Movies.objects.filter(
            world_premiere__gte=datetime.datetime.now()
        ).order_by('world_premiere')

        return render(request, "movies/index.html", {
            "premieres": premieres[:8],
            "index_movies": index_movies,
        })


class MovieDetailsView(View):

    def get(self, request, pk):
        movie = Movies.objects.get(pk=pk)
        return HttpResponse(movie.title)


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
