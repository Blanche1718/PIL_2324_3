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
    bio = models.CharField(max_length=100)
    numero= models.CharField( blank=True, null=True)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    age = models.CharField(null= True , blank= True)
    date_d_anniversaire = models.DateField(null = True , blank= True)
    profession = models.CharField(max_length=20, null=True)
    genre = models.CharField(max_length=20, null=True)
    sex = models.CharField(max_length=20 , null= True, blank=True)
    Corpulence = models.CharField(max_length=10 , null=True , blank=True)
    Couleur_de_peau = models.CharField(max_length= 20, null=True, blank=True)
    Localisation = models.CharField(max_length=30, null=True , blank= True)
    taille = models.CharField(max_length=20, null=True, blank= True)
    friends = models.ManyToManyField('Friend', related_name="my_friends")
    food_preference = models.CharField(max_length=100,blank=True, null=True)
    def __str__(self):
        return self.user.username


class Restaurant(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    photo_url = models.URLField(blank=True, null=True)
    cuisine_type = models.CharField(max_length=100,blank=True, null=True)
    price_range = models.DecimalField(max_digits=8, decimal_places=2,blank=True, null=True)

    def __str__(self):
        return self.name


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