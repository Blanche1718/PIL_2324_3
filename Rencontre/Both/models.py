from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    # This function defines the upload path for user's profile image
    return f'user_{instance.user.id}/{filename}'


from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    numero = models.CharField(max_length=15, blank=True)
    age = models.IntegerField(blank=True, null=True)
    date_d_anniversaire = models.DateField(blank=True, null=True)
    profession = models.CharField(max_length=50, blank=True)
    genre = models.CharField(max_length=10, choices=(('Masculin', 'Masculin'), ('Feminin', 'Feminin')), blank=True)
    sex = models.CharField(max_length=10, blank=True)
    corpulence = models.CharField(max_length=50, blank=True)
    couleur_de_peau = models.CharField(max_length=50, blank=True)
    localisation = models.CharField(max_length=100, blank=True)
    taille = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    friends = models.ManyToManyField('self', through='Friend', symmetrical=False, related_name='related_to')

    def _str_(self):
        return self.user.username

class Friend(models.Model):
    profile = models.ForeignKey(Profile, related_name='friendship_creator_set', on_delete=models.CASCADE)
    friend = models.ForeignKey(Profile, related_name='friend_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f'{self.profile} est ami avec {self.friend}'

    class Meta:
        unique_together = ('profile', 'friend')

class ChatMessage(models.Model):
    msg_sender = models.ForeignKey(Profile, related_name='sent_messages', on_delete=models.CASCADE)
    msg_receiver = models.ForeignKey(Profile, related_name='received_messages', on_delete=models.CASCADE)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True )
    seen = models.BooleanField(default=False)

    def _str_(self):
        return f'Message de {self.msg_sender} à {self.msg_receiver} : {self.body[:20]}'

class Preferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age_min = models.PositiveIntegerField()
    age_max = models.PositiveIntegerField()
    taille_min = models.PositiveIntegerField()
    taille_max = models.PositiveIntegerField()
    teint_preference = models.CharField(max_length=20, choices=[('noir', 'Noir'), ('clair', 'Clair')] , default='Noir')
    corpulence_preference = models.CharField(max_length=10, choices=[('gros', 'Gros'), ('mince', 'Mince'), ('musclé', 'Musclé'), ('normal', 'Normal')] , default='mince')
    localisation_preference = models.CharField(max_length=50 , default='')


def __str__(self):
     return f"{self.user.username}'s Preferences"


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    preferred_cuisine = models.CharField(max_length=100)
    budget_level = models.CharField(max_length=50)
    website_url = models.URLField(blank=True)  # Champ pour l'URL du site officiel
    image_url = models.URLField(blank=True)    # Champ pour l'URL de l'image du restaurant

    def __str__(self):
        return self.name