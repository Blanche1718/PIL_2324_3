
from typing import Any
from urllib import request
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render , redirect , get_object_or_404
#from django.contrib.auth.forms import UserCreationForm
from .form import MyUserForm, PreferencesForm,ChatMessageForm
from .models import Preferences, Profile,ChatMessage,Friend
from django.contrib.auth.views import LoginView
from PIL import Image   
from .form import RestaurantSearchForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.db.models import Q
from .form import MyUserForm, PreferencesForm, ChatMessageForm
from .models import Preferences, Profile, Restaurant, Friend, ChatMessage
from django.views.decorators.http import require_POST
import json
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User





class CustomPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        site_name = get_current_site(self.request).name
        # Logic for sending email here


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    reset_url = f"{'https'}://{'domain'}/reset/{'uid'}/{'token'}"
                    subject = "Réinitialisation du mot de passe demandée"
                    message = (
                        f"Bonjour,\n\n"
                        f"Vous avez demandé à réinitialiser votre mot de passe pour le site Both. "
                        f"Cliquez sur le lien ci-dessous pour réinitialiser votre mot de passe :\n\n"
                        f"{reset_url}\n\n"
                        f"Si vous n'avez pas fait cette demande, veuillez ignorer cet e-mail.\n\n"
                        f"Merci,\nL'équipe Both"
                    )
                    try:
                        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
                    except Exception as e:
                        return HttpResponse(f"Erreur lors de l'envoi de l'email : {e}")
                    return redirect("password_reset_confirm")
    password_reset_form = PasswordResetForm()
    return render(request, 'Both/password_reset_form.html', context={"form": password_reset_form})


def mailsend(request):
    return render(request, 'Both/password_reset_done.html')


def newpass(request):
    return render(request, 'Both/password_reset_confirm.html')


def done(request):
    return render(request, 'Both/password_reset_complete.html')


@login_required
def view_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'Both/profil.html', {'profile': profile})


def set_user_preferences(request):
    if request.method == 'POST':

        form = RestaurantSearchForm(request.POST)
        if form.is_valid():
            food_preference = form.cleaned_data['food_preference']
            
            # Enregistrer les préférences de l'utilisateur s'il n'en a pas encore
            user_preferences, created = Restaurant.objects.get_or_create(user=request.user)
            user_preferences.food_preference = food_preference
            user_preferences.save()

            return render(request, 'Both/preferences_saved.html')
    else:
        form = RestaurantSearchForm()
    
    return render(request, 'Both/set_preferences.html', {'form': form})

@login_required
def restaurant_search(request):
    user_preferences = get_object_or_404(Restaurant, user=request.user)
    
    if request.method == 'POST':
        form = RestaurantSearchForm(request.POST)
        if form.is_valid():
            budget = form.cleaned_data['budget']
            
            # Recherche des restaurants en fonction du budget et des préférences alimentaires de l'utilisateur
            restaurants = Restaurant.objects.filter(price_range__lte=budget, cuisine_type__icontains=user_preferences.food_preference)
            
            return render(request, 'restaurant_search_results.html', {'restaurants': restaurants})
    else:
        form = RestaurantSearchForm()
    
    return render(request, 'restaurant_search.html', {'form': form})



@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire POST
        bio = request.POST.get('bio', '')
        numero = request.POST.get('numero', '')
        age = request.POST.get('age', '')
        date_d_anniversaire= request.POST.get('date_d_anniversaire', '')
        profession= request.POST.get('profession', '')
        genre = request.POST.get('genre', '')
        sex = request.POST.get('sex', '')
        Corpulence= request.POST.get('Corpulence', '')
        Couleur_de_peau = request.POST.get('Couleur_de_peau', '')
        Localisation = request.POST.get('age', '')
        taille = request.POST.get('age', '')

    user = request.user

    if request.method == 'POST':
        # Mettre à jour les informations de l'utilisateur à partir des données POST
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()

        #messages.success(request, 'Votre profil a été mis à jour avec succès!')

        # Récupérer le profil de l'utilisateur connecté
        profile = Profile.objects.get(user=user)

        # Mettre à jour les champs du profil avec les nouvelles données
        profile.bio = bio
        profile.Localisation = Localisation
        profile.date_d_anniversaire = date_d_anniversaire
        profile.numero = numero
        profile.age = age
        profile.profession = profession
        profile.genre = genre
        profile.sex = sex 
        profile.Corpulence= Corpulence
        profile.Couleur_de_peau = Couleur_de_peau
        profile.taille = taille

        if 'image' in request.FILES:
            profile.image = request.FILES['image']
            
            
        profile.save()

        return redirect('profil')
    context = {
        'user': user,
    }


    return render(request, 'Both/modif.html', context)



def inscription_views(request):
    #if request.user.is_authenticated:
        #return redirect('profil')
    if request.method == 'POST':
        form = MyUserForm(request.POST)
        if form.is_valid():
            user = form.save()

        return redirect('login')
    else:
        form = MyUserForm()
    context = {
        'form': form,
        
    }
    return render(request, 'Both/inscription.html', context)


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        user = self.request.user
        if user.is_authenticated and user.is_first_login:
            user.is_first_login = False
            user.save()
            return redirect('modif')
        else:
            return redirect('profil')


def index(request):
    return render(request, 'Both/index.html')


def contact_views(request):
    return render(request, 'Both/contact.html')


def inscription_views(request):
    if request.method == 'POST':
        form = MyUserForm(request.POST)
        if form.is_valid():
           user= form.save()
        return redirect('login')
    else:
        form = MyUserForm()
    return render(request, 'Both/inscription.html', {'form': form})


