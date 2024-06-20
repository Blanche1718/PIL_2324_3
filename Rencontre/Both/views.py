from typing import Any
from urllib import request
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render , redirect , get_object_or_404
#from django.contrib.auth.forms import UserCreationForm
from .form import MyUserForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Conversation, Message, Restaurant
from .form import MessageForm
from .models import  Profile
from django.contrib.auth.views import LoginView
from PIL import Image   
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
    if request.method == 'POST':
        budget_level = request.POST.get('budget_level')
        preferred_cuisine = request.POST.get(' preferred_cuisine')
        
        return redirect('suggestions', budget_level=budget_level,  preferred_cuisine= preferred_cuisine)
    
    return render(request, 'Both/resto_preferences.html')

def show_results(request, budget_level, preferred_cuisine):
    restaurants = Restaurant.objects.filter(budget_level=budget_level, preferred_cuisine=preferred_cuisine)

    print(restaurants)  
    
    return render(request, 'Both/liste_resto.html', {'restaurants': restaurants})

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







@login_required
def conversation_list(request):
    conversations = request.user.conversations.all()
    conversations_with_participants = []
    for conversation in conversations:
        participant = conversation.participants.exclude(id=request.user.id).first()
        conversations_with_participants.append({
            'conversation': conversation,
            'participant_name': participant.username if participant else 'N/A'
        })
    return render(request, 'Both/conversation_list.html', {'conversations_with_participants': conversations_with_participants})


@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    messages = conversation.messages.all()
    form = MessageForm()
    return render(request, 'Both/conversation_detail.html', {'conversation': conversation, 'messages': messages, 'form': form})

@login_required
def send_message(request):
    if request.method == 'POST':
        conversation_id = request.POST.get('conversation_id')
        message_content = request.POST.get('message_content')
        conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
        message = Message.objects.create(conversation=conversation, sender=request.user, content=message_content)
        return JsonResponse({'status': 'success', 'message': message.content, 'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')})
    return JsonResponse({'status': 'error'})