from django.db import models

class User(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    profession = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    description = models.TextField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Preference(models.Model):
     GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'), 
    ]

     user = models.OneToOneField(User, on_delete=models.CASCADE)
     preferred_gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
     age_min = models.IntegerField()
     age_max = models.IntegerField()
     preferred_profession = models.CharField(max_length=100, blank=True, null=True)
     description_partner = models.TextField()

     def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} Preferences'
