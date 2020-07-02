from rest_framework.generics import ListAPIView
from movies.api.serializers import MovieListSerializers
from movies.api.pagination import StandardResultsSetPagination
from movies.models import Movies


class TestMovieList(ListAPIView):
    serializer_class = MovieListSerializers
    pagination_class = StandardResultsSetPagination
    queryset = Movies.objects.all()[:100]