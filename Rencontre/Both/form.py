from django import forms 
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from .models import Profile , Preferences,ChatMessage
from django.forms import ModelForm

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




class PreferencesForm(forms.ModelForm):
    class Meta:
        model = Preferences
        fields = ['age_min', 'age_max', 'taille_min', 'taille_max', 'teint_preference', 'corpulence_preference', 'localisation_preference']




class ChatMessageForm(ModelForm):
    body=forms.CharField(widget=forms.Textarea(attrs={"class":"forms", "rows":3, "placeholder":"Type message here"}))
    class Meta:
        model = ChatMessage
        fields=["body",]