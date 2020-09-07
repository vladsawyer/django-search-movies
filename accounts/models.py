from django.db import models
from movies.utils import get_hashed_path, get_random_default_user_avatar
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from movies.models import Movies


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=f'users/avatars/{get_hashed_path}',
                               verbose_name='Avatar',
                               default=get_random_default_user_avatar())
    favorites = models.ManyToManyField(Movies, verbose_name='Favorite movies', blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
