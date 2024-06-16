from django.db import models
from django.contrib.auth.models import User
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=100)
    numero= models.CharField(max_length=15, blank=15)
    photo = models.ImageField(upload_to='profile_photos/', blank=True , null=True)
    age = models.PositiveIntegerField(null= True , blank= True)
    date_d_anniversaire = models.DateField(null = True , blank= True)
    profession = models.CharField(max_length=20, null=True)
    genre = models.CharField(max_length=20, null=True)
    sex = models.CharField(max_length=20 , null= True, blank=True)
    lieu_de_travail= models.CharField(max_length=100, null= True, blank=True)

    def __str__(self):
        return self.user.username

# Create your models here.
