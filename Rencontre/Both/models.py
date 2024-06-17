from django.db import models
from django.contrib.auth.models import User
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=100)
    numero= models.CharField(max_length=15, blank=15)
    photo = models.ImageField(upload_to='images/', blank=True , null=True)
    age = models.PositiveIntegerField(null= True , blank= True)
    date_d_anniversaire = models.DateField(null = True , blank= True)
    profession = models.CharField(max_length=20, null=True)
    genre = models.CharField(max_length=20, null=True)
    sex = models.CharField(max_length=20 , null= True, blank=True)
    lieu_de_travail= models.CharField(max_length=100, null= True, blank=True)
    Corpulence = models.CharField(max_length=10 , choices=[('gros', 'Gros'), ('mince', 'Mince'), ('musclé', 'Musclé'), ('normal', 'Normal')])
    Couleur_de_peau = models.CharField(max_length= 20, choices=[('noir', 'Noir'), ('clair', 'Clair')] )
    Localisation = models.CharField(max_length=30, null=True , blank= True)
    Secteur_d_activite= models.CharField(max_length=50, null=True , blank=True)
    taille = models.CharField(max_length=20, null=True, blank= True)

    def __str__(self):
        return self.user.username

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
