from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import FREE_TRIAL_DAYS, Profile, User


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create Profile automatically when a new User is created."""
    if created:
        Profile.objects.create(
            user=instance,
            free_until=timezone.now() + timedelta(days=FREE_TRIAL_DAYS),
        )
