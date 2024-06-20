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


from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .form import MyUserForm, PreferencesForm
from .models import Preferences, Profile , Restaurant
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
        genre='Feminin' if request.user.profile.genre == 'Masculin' else 'Masculin'
    )
    return render(request, 'Both/suggestions.html', {'profiles': profiles})


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

def chat_index(request):
    user=request.user.profile
    friends= user.friends.all()
    context = {"user": user , "friends":friends}
    return render (request , "Both/chat_index.html" , context)

def detail(request, pk):
    friend=Friend.objects.get(profile_id=pk)
    user=request.user.profile
    profile = Profile.objects.get(id = friend.profile.id)
    chats=ChatMessage.objects.all()
    rec_chats=ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user)
    rec_chats.update(seen=True)
    form = ChatMessageForm
    if request.method == "POST":
        form = ChatMessageForm(request.POST)
        if form.is_valid():
           chat_message=form.save(commit=False)
           chat_message.msg_sender=user
           chat_message.msg_receiver= profile
           chat_message.save()
           return redirect("detail", pk=friend.profile.id) 
    context = {"friend" : friend , "form":form, "user":user ,"profile":profile ,"chats":chats,"num":rec_chats.count() }
    return render (request , "Both/detail.html" , context)


def sentMessages(request, pk):
    user=request.user.profile
    friend= Friend.objects.get(profile_id=pk)
    profile = Profile.objects.get(id=friend.profile.id)
    data= json.loads(request.body)
    new_chat= data["msg"]
    new_chat_message = ChatMessage.objects.create(body=new_chat,msg_sender=user, msg_receiver=profile, seen=False)
    print(new_chat)
    return JsonResponse(new_chat_message.body, safe=False)

def receivedMessages(request, pk):
    user= request.user.profile
    friend= Friend.objects.get(profile_id=pk)
    profile = Profile.objects.get(id=friend.profile.id)
    arr=[]
    chats=ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user)
    for chat in chats:
        arr.append(chat.body)
    return JsonResponse(arr , safe=False)


def chatNotification(request):
    user=request.user.profile
    friends= user.friends.all()
    arr=[]
    for friend in friends:
        chats=ChatMessage.objects.filter(msg_sender__id=friend.profile.id, msg_receiver=user, seen=False)
        arr.append(chats.count())
    return JsonResponse(arr , safe=False)