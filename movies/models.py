import os
from hashlib import sha1
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


# create image path for models
def get_members_image_path(instance, filename):
    hashname = sha1(filename.encode('utf-8')).hexdigest() + '.jpg'
    return os.path.join('member', hashname[:2], hashname[2:4], hashname)


def get_movie_posters_image_path(instance, filename):
    hashname = sha1(filename.encode('utf-8')).hexdigest() + '.jpg'
    return os.path.join('movie_posters', hashname[:2], hashname[2:4], hashname)


def get_movie_shots_image_path(instance, filename):
    hashname = sha1(filename.encode('utf-8')).hexdigest() + '.jpg'
    return os.path.join('movie_shots', hashname[:2], hashname[2:4], hashname)


class Categories(MPTTModel):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movies_category_list', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"


class Likes(models.Model):
    like = 1
    dislike = -1
    VALUE_CHOICES = (
        (like, "\U0001F44D"),
        (dislike, "\U0001F44E")
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=VALUE_CHOICES, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    liked_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "like"
        verbose_name_plural = "likes"
        unique_together = ('user', 'content_type', 'object_id')


class Comments(MPTTModel):
    text = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    likes = GenericRelation(Likes)
    commented_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    @property
    def total_likes(self):
        return self.likes.count()

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"


class Ratings(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = "rating"
        verbose_name_plural = "ratings"
        unique_together = ('user', 'content_type', 'object_id')


class Roles(models.Model):
    role = models.CharField(max_length=150)

    def __str__(self):
        return self.role

    class Meta:
        verbose_name = "role"
        verbose_name_plural = "roles"


class Members(models.Model):
    full_name = models.CharField(max_length=150)
    total_movies = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    categories = models.ManyToManyField(Categories)
    roles = models.ManyToManyField(Roles)
    image = models.ImageField(upload_to=get_members_image_path, blank=True)

    comments = GenericRelation(Comments)
    ratings = GenericRelation(Ratings)

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('member', kwargs={"pk": self.id})

    class Meta:
        verbose_name = "member"
        verbose_name_plural = "members"


class Movies(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    poster = models.ImageField(upload_to=get_movie_posters_image_path, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    directors = models.ManyToManyField(Members, related_name='film_director')
    actors = models.ManyToManyField(Members, related_name='film_actor')
    categories = models.ManyToManyField(Categories)
    world_premiere = models.DateField(null=True, blank=True)
    rating_kp = models.FloatField(null=True, blank=True)
    rating_imdb = models.FloatField(null=True, blank=True)
    rf_premiere = models.DateField(null=True, blank=True)
    budget = models.BigIntegerField(null=True, blank=True, help_text="indicate the amount in dollars")
    fees_in_usa = models.BigIntegerField(null=True, blank=True, help_text="indicate the amount in dollars")
    fees_in_world = models.BigIntegerField(null=True, blank=True, help_text="indicate the amount in dollars")
    age = models.PositiveIntegerField(help_text="age mark", null=True, blank=True)
    draft = models.BooleanField(default=False)
    slug = models.SlugField(max_length=160, null=True, blank=True)
    time = models.TimeField(null=True, blank=True)

    comments = GenericRelation(Comments)
    ratings = GenericRelation(Ratings)
    likes = GenericRelation(Likes)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        mov = Movies.objects.get(pk=self.id)
        if mov.categories.filter(title='фильмы').exists():
            return reverse('movie_detail', kwargs={"pk": self.id})
        elif mov.categories.filter(title='сериалы').exists():
            return reverse('series_detail', kwargs={"pk": self.id})

    class Meta:
        verbose_name = "movie"
        verbose_name_plural = "movies"


class PartnerUrls(models.Model):
    name_company = models.CharField(max_length=255)
    url = models.URLField(null=True, blank=True)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)

    def __str__(self):
        return self.name_company

    class Meta:
        verbose_name = "partner url"
        verbose_name_plural = "partner urls"


class MovieShots(models.Model):
    image = models.ImageField(upload_to=get_movie_shots_image_path)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)

    def __str__(self):
        return self.movie.title

    class Meta:
        verbose_name = "movie shot"
        verbose_name_plural = "movie shots"


