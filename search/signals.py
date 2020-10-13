from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from movies.models import (
    Members,
    Movies,
    Collection
)
from search.serializers import (
    MemberDocumentSerializer,
    MovieDocumentSerializer,
    CollectionDocumentSerializer
)


# Movie signals for elasticsearch
@receiver(post_save, sender=Movies, dispatch_uid="update_record")
def update_es_record(sender, instance, **kwargs):
    obj = MovieDocumentSerializer(instance)
    obj.save()


@receiver(post_delete, sender=Movies, dispatch_uid="delete_record")
def delete_es_record(sender, instance, *args, **kwargs):
    obj = MovieDocumentSerializer(instance)
    obj.delete(ignore=404)


# Member signals for elasticsearch
@receiver(post_save, sender=Members, dispatch_uid="update_record")
def update_es_record(sender, instance, **kwargs):
    obj = MemberDocumentSerializer(instance)
    obj.save()


@receiver(post_delete, sender=Members, dispatch_uid="delete_record")
def delete_es_record(sender, instance, *args, **kwargs):
    obj = MemberDocumentSerializer(instance)
    obj.delete(ignore=404)


# Collection signals for elasticsearch
@receiver(post_save, sender=Collection, dispatch_uid="update_record")
def update_es_record(sender, instance, **kwargs):
    obj = CollectionDocumentSerializer(instance)
    obj.save()


@receiver(post_delete, sender=Members, dispatch_uid="delete_record")
def delete_es_record(sender, instance, *args, **kwargs):
    obj = CollectionDocumentSerializer(instance)
    obj.delete(ignore=404)
