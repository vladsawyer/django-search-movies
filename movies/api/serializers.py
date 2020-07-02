from rest_framework import serializers
from movies.models import Movies, Members, Categories


class MemberListSerializer(serializers.ModelSerializer):
    member_url = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Members
        fields = ("full_name", "member_url")


class FilterCategoryListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.exclude(parent__slug='genres').exclude(slug='genres')
        return super().to_representation(data)


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = FilterCategoryListSerializer
        model = Categories
        fields = ("title", "slug")


class GenresListSerializer(serializers.ModelSerializer):
    genre_url = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Categories
        fields = ("title", "slug", "genre_url")


class MovieListSerializers(serializers.ModelSerializer):
    directors = MemberListSerializer(many=True, read_only=True)
    actors = MemberListSerializer(many=True, read_only=True)
    categories = CategoryListSerializer(many=True, read_only=True)
    genres = serializers.ReadOnlyField() and GenresListSerializer(many=True, read_only=True)
    poster = serializers.SerializerMethodField(read_only=True)
    movie_url = serializers.URLField(source='get_absolute_url', read_only=True)
    year = serializers.SerializerMethodField(read_only=True)
    world_premiere = serializers.DateField(format='%d %B %Y', required=False, read_only=True)

    def get_year(self, obj):
        return obj.world_premiere.year

    def get_poster(self, obj):
        return obj.poster.url

    class Meta:
        model = Movies
        fields = ("id", "title", "description", "poster", "country", "directors", "actors", "categories",
                  "genres", "world_premiere", "year", "rating_kp", "rating_imdb", "movie_url")
