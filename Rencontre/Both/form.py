from django import forms 
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from .models import Profile

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Pseudo' , widget=forms.TextInput(attrs={
        'class':'form-control', 
    }))
    password = forms.CharField(label='Pot de passe' , widget=forms.PasswordInput(attrs={
        'class':'form-control',}))


class MyUserForm(UserCreationForm):
    username = forms.CharField(label='Pseudo' , widget=forms.TextInput(attrs={
        'class':'form-control', 
    }))
    first_name = forms.CharField(label='Nom' , widget=forms.TextInput(attrs={
        'class':'form-control',}))
    last_name = forms.CharField(label='Prénom' , widget=forms.TextInput(attrs={
        'class':'form-control',}))
    password1 = forms.CharField(label='Mot de passe' , widget=forms.PasswordInput(attrs={
        'class':'form-control',}))
    password2 = forms.CharField(label='Confirmez le mot de passe' , widget=forms.PasswordInput(attrs={
        'class':'form-control',}))
    email = forms.CharField(label='Email' , widget=forms.EmailInput(attrs={
        'class':'form-control',}))
    
    
    class Meta :
        model = User
        fields = ('first_name','last_name','username','email','password1','password2')






class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo','bio','numero','age','profession','date_d_anniversaire','genre','sex','lieu_de_travail','Corpulence','Couleur_de_peau','Localisation','Secteur_d_activite','taille']