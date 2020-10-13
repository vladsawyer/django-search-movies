from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from movies.models import Movies
from search.documents import (
    movie,
    member,
    collection
)


class MovieDocumentSerializer(DocumentSerializer):
    class Meta:
        document = movie.MovieDocument
        fields = ("movie_url", "title", "country", "rating_kp", "rating_imdb", "world_premiere", "image", "directors")


class MemberDocumentSerializer(DocumentSerializer):
    class Meta:
        document = member.MemberDocument
        fields = ("image", "full_name", "birthday", "roles", "member_url")


class CollectionDocumentSerializer(DocumentSerializer):
    class Meta:
        document = collection.CollectionDocument
        fields = ("title", "image")
