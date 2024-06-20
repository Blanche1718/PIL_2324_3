from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    # This function defines the upload path for user's profile image
    return f'user_{instance.user.id}/{filename}'


from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):

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


