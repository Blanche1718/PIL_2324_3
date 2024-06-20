from typing import Any
from urllib import request
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render , redirect , get_object_or_404
#from django.contrib.auth.forms import UserCreationForm
from .form import MyUserForm
from django.contrib.auth.views import LoginView
from PIL import Image   


from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .form import MyUserForm
from .models import  Profile , Restaurant
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'login.html'  # Template pour la vue de connexion

    def form_valid(self, form):
        # Récupérer l'utilisateur qui vient de se connecter
        user = self.request.user

        # Vérifier si c'est la première connexion
        if user.is_authenticated and user.is_first_login:
            # Mettre à jour l'indicateur de première connexion
            user.is_first_login = False
            user.save()

            # Rediriger vers la page1 après la première connexion
            return redirect('modif')
        else:
            # Rediriger vers la page2 pour les connexions suivantes
            return redirect('profil')

@login_required
def view_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'Both/profil.html', {'profile': profile})


def restaurant_suggestions(request):
    if request.method == 'GET':
        cuisine = request.GET.get('cuisine')
        budget = request.GET.get('budget')

        # Filtrer les restaurants en fonction du type de cuisine et du niveau de budget
        restaurants = Restaurant.objects.filter(preferred_cuisine=cuisine, budget_level=budget)

        context = {
            'restaurants': restaurants,
            'cuisine': cuisine,
            'budget': budget,
        }
        return render(request, 'Both/recherche_restaurants.html', context)

    return render(request, 'Both/recherche_restaurants.html')

def liste_restaurants(request):
    restaurants = Restaurant.objects.all()
    context = {
        'restaurants': restaurants
    }
    return render(request, 'Both/liste_restaurants.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire POST
        bio = request.POST.get('bio', '')
        numero = request.POST.get('numero', '')
        age = request.POST.get('age', '')
        date_d_anniversaire= request.POST.get('date_d_anniversaire', '')
        profession= request.POST.get('profession', '')
        gender = request.POST.get('gender', '')
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
        profile.gender = gender
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
    if request.user.is_authenticated:
        return redirect('profil')
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




def index(request):
    return render(request, 'Both/index.html')




def contact_views(request):
    return render(request, 'Both/contact.html')




@login_required
def profile_detail(request, user_id):
    profile = get_object_or_404(Profile, id=user_id)
    return render(request, 'Both/user_detail.html', {'profile': profile})



from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from django.conf import settings
import json




class CustomPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        
        site_name = get_current_site(self.request).name


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
                  
    password_reset_form = PasswordResetForm()
    return render(request, 'Both/password_reset_form.html', context={"form":password_reset_form})

def mailsend(request):
    return render(request, 'Both/password_reset_done.html')

def newpass(request):
    return render(request, 'Both/password_reset_confirm.html')
def done(request):
    return render(request, 'Both/password_reset_complete.html')


from django.shortcuts import render
from .models import Profile


@login_required
def suggestion_view(request):
    current_user_profile = request.user.profile  # Récupérer le profil de l'utilisateur connecté
    
    if current_user_profile.gender == 'M':
        suggested_profiles = Profile.objects.filter(gender='F').exclude(user=request.user)
    elif current_user_profile.gender == 'F':
        suggested_profiles = Profile.objects.filter(gender='M').exclude(user=request.user)
    else:
        suggested_profiles = Profile.objects.none()  # Aucune suggestion si le genre n'est pas défini correctement
    
    context = {
        'suggested_profiles': suggested_profiles
    }
    
    return render(request, 'Both/suggestions.html', context)

def profile_detail_view(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    context = {
        'profile': profile
    }
    return render(request, 'Both/profile_detail.html', context)