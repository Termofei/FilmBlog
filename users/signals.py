from django.dispatch import receiver

from users.models import UserProfile


@receiver
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)