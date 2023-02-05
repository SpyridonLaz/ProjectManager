

from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from assessment.apps.manager.models import Project


@receiver(post_delete, sender=Project, dispatch_uid='post_deleted')
def object_post_delete_handler(sender, **kwargs):
    cache.delete('project_objects')


@receiver(post_save, sender=Project, dispatch_uid='posts_updated')
def object_post_save_handler(sender, **kwargs):
    cache.delete('project_objects')
