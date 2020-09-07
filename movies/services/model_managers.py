from django.db.models.aggregates import Count, Sum
from random import randint
from django.db import models


class MovieManager(models.Manager):
    def get_random_movie(self):
        """
        functionality to select a random object movie or series
        """
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]


class VoteManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        """
        We take a queryset with records greater than 0.
        :return: queryset
        """
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        """
        We take a queryset with records less than 0.
        :return: queryset
        """
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        """
        We take the total rating.
        :return: queryset
        """
        return self.votes.aggregate(Sum('vote')).get('vote__sum') or 0
