from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Preferences

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Preferences.objects.create(
            user=instance,
            age_min=18,
            age_max=99,
            taille_min=150,
            taille_max=200,
            teint_preference='Clair',
            corpulence_preference='Normal',
            localisation_preference='',
            
        )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    instance.preferences.save()
