from django.db.models.aggregates import Count
from random import randint
from django.db import models


class MovieManager(models.Manager):
    def get_random_movie(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]
