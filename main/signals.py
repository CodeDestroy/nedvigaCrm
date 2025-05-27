from django.contrib.admin.options import get_content_type_for_model

from main.models import UserLogEntry
from main.tools import object_to_dict


def log_update(sender, instance, **kwargs):
    if instance.id and instance.updated_by:
        old = sender.objects.get(id=instance.id)
        UserLogEntry.objects.create(user=instance.updated_by, content_type=get_content_type_for_model(old),
                                    object_id=old.id, fields=object_to_dict(old), action_flag=1)


def log_delete(sender, instance, **kwargs):
    old = sender.objects.get(id=instance.id)
    UserLogEntry.objects.create(content_type=get_content_type_for_model(old),
                                object_id=old.id, fields=object_to_dict(old), action_flag=2)
