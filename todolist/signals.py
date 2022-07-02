from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from todolist.celery_tasks import send_email_done_status_changed
from todolist.models import Task


@receiver(pre_save, sender=Task)
def send_email_if_field_done_changed(sender, instance, *args, **kwargs):
    if not instance._state.adding:
        new_done_status = instance.done
        old_done_status = Task.objects.get(id=instance.id).done

        if new_done_status != old_done_status:
            send_email_done_status_changed(old_done_status, new_done_status, instance.id)
