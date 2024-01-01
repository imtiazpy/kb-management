from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from staffs.models import Staff


USER = get_user_model()


@receiver(post_save, sender=USER)
def create_staff(sender, instance, created, **kwargs):
    if created:
        Staff.objects.create(user=instance)

@receiver(post_save, sender=USER)
def save_staff(sender, instance, **kwargs):
	instance.user_staff.save()

