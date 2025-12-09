from .models import Notification
from django.contrib.contenttypes.models import ContentType

def create_notification(recipient, actor, verb, target=None):
    if recipient == actor:
        return  # Do not notify self

    content_type = None
    object_id = None

    if target is not None:
        content_type = ContentType.objects.get_for_model(target)
        object_id = target.id

    Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        target_content_type=content_type,
        target_object_id=object_id
    )
