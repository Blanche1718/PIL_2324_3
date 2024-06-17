import profile
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
    Corpulence = models.CharField(max_length=10 , null=True , blank=True)
    Couleur_de_peau = models.CharField(max_length= 20, null=True, blank=True)
    Localisation = models.CharField(max_length=30, null=True , blank= True)
    Secteur_d_activite= models.CharField(max_length=50, null=True , blank=True)
    taille = models.CharField(max_length=20, null=True, blank= True)
    friends = models.ManyToManyField('Friend', related_name="my_friends")

    def __str__(self):
        return self.user.username

class Friend(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self) :
        return self.profile.user.username

class ChatMessage(models.Model):
    body = models.TextField()
    msg_sender=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="msg_sender" )
    msg_receiver=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="msg_receiver" )
    seen = models.BooleanField(default=False)


    def __str__(self) :
        return self.body
