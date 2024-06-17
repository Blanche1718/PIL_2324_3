from typing import Any
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render , redirect , get_object_or_404
#from django.contrib.auth.forms import UserCreationForm
from .form import MyUserForm, ProfileForm
from .models import Profile
from django.contrib.auth.views import LoginView


@login_required
def view_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'Both/profil.html', {'profile': profile})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
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
            form.save()
            return redirect('login')
    else :
        form = MyUserForm()
    context = {
        'form': form,
    }
    return render(request, 'Both/inscription.html', context)

class Myloginview(LoginView):
    template_name= 'Both/login.html'
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
def suggestions(request):
    user_profile = request.user.profile
    if user_profile.genre.lower() == 'masculin':
        suggestions = Profile.objects.filter(genre='Féminin', age__range=(user_profile.age - 4, user_profile.age + 4))
    else:
        suggestions = Profile.objects.filter(genre='Masculin', age__range=(user_profile.age - 4, user_profile.age + 4))
    return render(request, 'Both/suggestions.html', {'suggestions': suggestions})

@login_required
def user_detail(request, pk):
    user_profile = get_object_or_404(Profile, pk=pk)
    return render(request, 'Both/user_detail.html', {'user_profile': user_profile})

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
