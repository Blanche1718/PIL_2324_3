from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    # This function defines the upload path for user's profile image
    return f'user_{instance.user.id}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=100)
    numero= models.CharField( blank=True, null=True)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    age = models.CharField(null= True , blank= True)
    date_d_anniversaire = models.DateField(null = True , blank= True)
    profession = models.CharField(max_length=20, null=True)
    gender = models.CharField(max_length=10, choices=(('M', 'Masculin'), ('F', 'Féminin')), blank=True)
    sex = models.CharField(max_length=20 , null= True, blank=True)
    Corpulence = models.CharField(max_length=10 , null=True , blank=True)
    Couleur_de_peau = models.CharField(max_length= 20, null=True, blank=True)
    Localisation = models.CharField(max_length=30, null=True , blank= True)
    taille = models.CharField(max_length=20, null=True, blank= True)
    budget_level = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    preferred_cuisine = models.CharField(max_length=100, null=True)  # Peut être un choix limité via un champ ChoiceField si nécessaire
    is_first_login = models.BooleanField(default=True)
    def __str__(self):
        return self.user.username

class Restaurant(models.Model):
    BUDGET_CHOICES = [
        ('bon_marche', 'Bon marché'),
        ('modere', 'Modéré'),
        ('chic', 'Chic'),
    ]
    
    CUISINE_CHOICES = [
        ('italienne', 'Cuisine italienne'),
        ('francaise', 'Cuisine française'),
        ('japonaise', 'Cuisine japonaise'),
    ]

    name = models.CharField(max_length=255)
    preferred_cuisine = models.CharField(max_length=100, choices=CUISINE_CHOICES)
    budget_level = models.CharField(max_length=50, choices=BUDGET_CHOICES)
    website_url = models.URLField(blank=True)  # Champ pour l'URL du site officiel
    image_url = models.URLField(blank=True)    # Champ pour l'URL de l'image du restaurant

    def __str__(self):
        return self.name
    
from django.db.models.signals import post_save
from django.dispatch import receiver



class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')

    @classmethod
    def create_conversation(cls, user1, user2):
        # Créer une nouvelle conversation entre user1 et user2
        conversation = cls.objects.create()
        conversation.participants.add(user1, user2)
        return conversation

    def _str_(self):
        participant_names = ', '.join([user.username for user in self.participants.all()])
        return f"Conversation between {participant_names}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


