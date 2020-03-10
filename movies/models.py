from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.
class Categories(MPTTModel):
    title = models.CharField(max_length=150)
    description = models.TextField()
    slug = models.SlugField(max_length=160, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"


class Likes(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='likes',
                             on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Comments(MPTTModel):
    text = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='comments',
                             on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    likes = GenericRelation(Likes)

    def __str__(self):
        return self.text

    @property
    def total_likes(self):
        return self.likes.count()


class Ratings(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='ratings',
                             on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = "rating"
        verbose_name_plural = "rating"


class Members(models.Model):
    full_name = models.CharField(max_length=150)
    age = models.PositiveIntegerField(default=0)
    description = models.TextField()
    image = models.ImageField(upload_to="member/")
    slug = models.SlugField(max_length=160, unique=True)

    comments = GenericRelation(Comments)
    ratings = GenericRelation(Ratings)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "member"
        verbose_name_plural = "members"


class Movies(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    tagline = models.CharField(max_length=150, default='')
    poster = models.ImageField(upload_to="movie/")
    year = models.DateField()
    country = models.CharField(max_length=50)
    directors = models.ManyToManyField(Members, related_name='film_director')
    actors = models.ManyToManyField(Members, related_name='film_actor')
    categories = models.ManyToManyField(Categories)
    world_premiere = models.DateField(default=timezone.now().strftime('%d.%m.%y'))
    budget = models.PositiveIntegerField(default=0, help_text="indicate the amount in dollars")
    fees_in_usa = models.PositiveIntegerField(default=0, help_text="indicate the amount in dollars")
    fees_in_world = models.PositiveIntegerField(default=0, help_text="indicate the amount in dollars")
    age = models.PositiveIntegerField(default=0, help_text="age mark")
    draft = models.BooleanField(default=False)
    slug = models.SlugField(max_length=160, unique=True)

    comments = GenericRelation(Comments)
    ratings = GenericRelation(Ratings)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "movie"
        verbose_name_plural = "movies"


class PartnerUrls(models.Model):
    name_company = models.CharField(max_length=255)
    url = models.URLField(null=True)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)

    def __str__(self):
        return self.name_company

    class Meta:
        verbose_name = "partner url"
        verbose_name_plural = "partner urls"


class MovieShots(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to="movie_shots/")
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "movie shot"
        verbose_name_plural = "movie shots"
