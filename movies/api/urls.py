from django.urls import path
from . import views

urlpatterns = [
    path("movielist/", views.TestMovieList.as_view(), name='api-movie-list'),
]
