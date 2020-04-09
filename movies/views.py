from django.shortcuts import render
from django.views import View
from .models import Movies


# Create your views here.
# class MoviesView(View):
#     """Movie list"""

def index(request):
    return render(request, "movies/index.html")


def get(request):
    movies = Movies.objects.all()
    return render(request, "movies/index.html", {"movie_list": movies})
