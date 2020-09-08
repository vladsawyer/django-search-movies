from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from movies.services.model_managers import MovieManager, VoteManager
from movies.utils import (
    get_comment_hashed_path,
    get_member_hashed_path,
    get_movie_hashed_path
)


class Categories(MPTTModel):
    """
    Categories with a tree structure, genres are defined as a subcategory of "genres"
    """
    title = models.CharField(verbose_name="Name of category", max_length=150)
    slug = models.SlugField(verbose_name="Unique identificator", max_length=160, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return self.title

    # for genres
    def get_absolute_url(self):
        return reverse('movies_genre_list', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Vote(models.Model):
    """
    Like/Dislike system for comments, additional rating for films, series, actors, directors, collections.
    """
    LIKE = 1
    DISLIKE = -1
    VOTES = (
        (DISLIKE, '👎'),
        (LIKE, '👍')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='User')
    vote = models.SmallIntegerField(verbose_name="Voice", choices=VOTES, null=True)
    liked_on = models.DateTimeField(auto_now=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = VoteManager()

    class Meta:
        verbose_name = "Vote"
        verbose_name_plural = "Votes"
        unique_together = ('user', 'content_type', 'object_id')


class Comments(MPTTModel):
    """
    For storing comments on films, series, members.
    Tree structure, for convenient display of comments tree on the page
    """
    text = models.TextField(verbose_name="Text comments")
    image = models.ImageField(upload_to=get_comment_hashed_path, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    votes = GenericRelation(Vote, related_query_name='comment')
    commented_on = models.DateTimeField(verbose_name="Date publisher", auto_now=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


class Ratings(models.Model):
    """
    The system of basic evaluation of films, series, actors, directors, collections.
    It is considered as an average score of 10
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(verbose_name="Your rating", null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"
        unique_together = ('user', 'content_type', 'object_id')


class Roles(models.Model):
    """
    Professional activity of the filming participant.
    For example: "Actor, Producer"
    """
    role = models.CharField(verbose_name="Career", max_length=150)

    def __str__(self):
        return self.role

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"


class Members(models.Model):
    """
    All information about actors, directors
    """
    full_name = models.CharField(verbose_name="Full name", max_length=150)
    total_movies = models.PositiveIntegerField(
        verbose_name="Total movies in which member took part",
        null=True,
        blank=True
    )
    description = models.TextField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    categories = models.ManyToManyField(Categories)
    roles = models.ManyToManyField(Roles, verbose_name="Career")
    image = models.ImageField(upload_to=get_member_hashed_path, blank=True)

    comments = GenericRelation(Comments)
    ratings = GenericRelation(Ratings)
    votes = GenericRelation(Vote, related_query_name='member')

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('member', kwargs={"pk": self.id})

    class Meta:
        verbose_name = "Member"
        verbose_name_plural = "Members"


class Movies(models.Model):
    """
    Information about films and series
    """
    title = models.CharField(verbose_name="Title movie", max_length=150)
    description = models.TextField(null=True, blank=True)
    poster = models.ImageField(blank=True, upload_to=get_movie_hashed_path)
    country = models.CharField(max_length=50, null=True, blank=True)
    directors = models.ManyToManyField(Members, related_name='film_director')
    actors = models.ManyToManyField(Members, related_name='film_actor')
    categories = models.ManyToManyField(Categories)
    world_premiere = models.DateField(verbose_name="World premier", null=True, blank=True)
    rating_kp = models.FloatField(verbose_name="Rating Kinopoisk", null=True, blank=True)
    rating_imdb = models.FloatField(verbose_name="Rating IMDB", null=True, blank=True)
    rf_premiere = models.DateField(verbose_name="Date premier in Russian Federation", null=True, blank=True)
    budget = models.BigIntegerField(null=True, blank=True, help_text="indicate the amount in dollars")
    fees_in_usa = models.BigIntegerField(
        verbose_name="Fees in USA",
        null=True,
        blank=True,
        help_text="indicate the amount in dollars"
    )
    fees_in_world = models.BigIntegerField(
        verbose_name="Fees in world",
        null=True,
        blank=True,
        help_text="indicate the amount in dollars"
    )
    age = models.PositiveIntegerField(verbose_name="Age mark", help_text="age mark", null=True, blank=True)
    draft = models.BooleanField(default=False)
    time = models.TimeField(verbose_name="Movie duration", null=True, blank=True)

    comments = GenericRelation(Comments)
    ratings = GenericRelation(Ratings)
    votes = GenericRelation(Vote, related_query_name='movie')

    objects = MovieManager()

    def __str__(self):
        return self.title

    # for serializers(api)
    def genres(self):
        mov = Movies.objects.get(pk=self.id)
        genres = mov.categories.filter(parent__slug='genres')
        return genres

    def get_absolute_url(self):
        mov = Movies.objects.get(pk=self.id)
        if mov.categories.filter(title='фильмы').exists():
            return reverse('movie_detail', kwargs={"pk": self.id})
        elif mov.categories.filter(title='сериалы').exists():
            return reverse('series_detail', kwargs={"pk": self.id})

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"


class PartnerUrls(models.Model):
    """
    Affiliate links leading to streaming services,
    for example: Amediateka
    """
    name_company = models.CharField(verbose_name="Name company", max_length=255)
    url = models.URLField(null=True, blank=True)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)

    def __str__(self):
        return self.name_company

    class Meta:
        verbose_name = "Partner url"
        verbose_name_plural = "Partner urls"


class MovieShots(models.Model):
    image = models.ImageField(upload_to=get_movie_hashed_path)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)

    def __str__(self):
        return self.movie.title

    class Meta:
        verbose_name = "Movie shot"
        verbose_name_plural = "Movie shots"
