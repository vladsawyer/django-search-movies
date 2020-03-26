from django.shortcuts import render
from django.views import View
from .models import Movies


# Create your views here.
class MoviesView(View):
    """Movie list"""

    def home(self):
        return render("movie/dj_index.html")

    def get(self, request):
        movies = Movies.objects.all()
        return render(request, "movie/dj_index.html", {"movie_list": movies})
