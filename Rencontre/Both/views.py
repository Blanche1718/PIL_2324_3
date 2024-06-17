from typing import Any
from urllib import request
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render , redirect , get_object_or_404
#from django.contrib.auth.forms import UserCreationForm
from .form import MyUserForm, PreferencesForm, ProfileForm
from .models import Preferences, Profile
from django.contrib.auth.views import LoginView


from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .form import MyUserForm, PreferencesForm, ProfileForm
from .models import Preferences, Profile
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


@login_required
def view_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'Both/profil.html', {'profile': profile})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profil')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'Both/modif.html', {'form': form})



def inscription_views(request):
    if request.user.is_authenticated:
        return redirect('profil')
    if request.method == 'POST':
        form = MyUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Try to get existing profile for the user
            try:
                profile = Profile.objects.get(user=user)
                # Update existing profile with new data
                profile.first_name = user.first_name
                profile.last_name = user.last_name
                profile.save()
            except Profile.DoesNotExist:
                # Create profile if it doesn't exist
                Profile.objects.create(user=user)

            # Try to get existing preferences for the user
            try:
                preferences = Preferences.objects.get(user=user)
                # Update existing preferences with new data
                preferences.save()  # Update the preferences fields accordingly
            except Preferences.DoesNotExist:
                # Create preferences if they don't exist
                Preferences.objects.create(user=user)

            return redirect('login')
    else:
        form = MyUserForm()
    context = {
        'form': form,
    }
    return render(request, 'Both/inscription.html', context)


class Myloginview(LoginView):
    template_name = 'Both/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profil')
        return super().dispatch(request, *args, **kwargs)


def index(request):
    return render(request, 'Both/index.html')


def informations_views(request):
    return render(request, 'Both/informations.html')


def contact_views(request):
    return render(request, 'Both/contact.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profil')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'Both/modif.html', {'form': form})

@login_required
def edit_preferences(request):
    preferences, created = Preferences.objects.get_or_create(
        user=request.user,
        defaults={
            'age_min': 18,
            'age_max': 99,
            'taille_min': 150,
            'taille_max': 200,
            'teint_preference': 'Clair',
            'corpulence_preference': 'Normal',
            'localisation_preference': '',
            'genre_preference': 'Féminin',
        }
    )

    if request.method == 'POST':
        form = PreferencesForm(request.POST, instance=preferences)
        if form.is_valid():
            form.save()
            return redirect('suggestions')
    else:
        form = PreferencesForm(instance=preferences)

    return render(request, 'Both/preferences.html', {'form': form})



@login_required
def suggestions(request):
    preferences = get_object_or_404(Preferences, user=request.user)
    profiles = Profile.objects.filter(
        age__gte=preferences.age_min,
        age__lte=preferences.age_max,
        taille__gte=preferences.taille_min,
        taille__lte=preferences.taille_max,
        Couleur_de_peau=preferences.teint_preference,
        Corpulence=preferences.corpulence_preference,  
        Localisation=preferences.localisation_preference,
        genre='Féminin' if request.user.profile.genre == 'Masculin' else 'Masculin'
    )
    return render(request, 'Both/suggestions.html', {'profiles': profiles})


@login_required
def profile_detail(request, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)
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
                    message = (
                f"Bonjour,\n\n"
                f"Vous avez demandé à réinitialiser votre mot de passe pour le site Both. "
                f"Cliquez sur le lien ci-dessous pour réinitialiser votre mot de passe :\n\n"
                f"{reset_url}\n\n"
                f"Si vous n'avez pas fait cette demande, veuillez ignorer cet e-mail.\n\n"
                f"Merci,\nL'équipe Both"
                )
                    
                    
                    
                    c = user.email
                    try:
                        send_mail(subject,message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
                    except Exception as e:
                        return HttpResponse(f"Erreur lors de l'envoi de l'email : {e}")
                    return redirect("password_reset_confirm")
    password_reset_form = PasswordResetForm()
    return render(request, 'Both/password_reset_form.html', context={"form":password_reset_form})

def mailsend(request):
    return render(request, 'Both/password_reset_done.html')

def newpass(request):
    return render(request, 'Both/password_reset_confirm.html')
def done(request):
    return render(request, 'Both/password_reset_complete.html')

