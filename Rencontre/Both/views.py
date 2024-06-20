
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
            form.save()
            return redirect('login')
    else:
        form = MyUserForm()
    return render(request, 'Both/inscription.html', {'form': form})


@login_required
def edit_profile(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)

    if request.method == 'POST':
        bio = request.POST.get('bio', '')
        numero = request.POST.get('numero', '')
        age = request.POST.get('age', '')
        date_d_anniversaire = request.POST.get('date_d_anniversaire', '')
        profession = request.POST.get('profession', '')
        genre = request.POST.get('genre', '')
        sex = request.POST.get('sex', '')
        corpulence = request.POST.get('corpulence', '')
        couleur_de_peau = request.POST.get('couleur_de_peau', '')
        localisation = request.POST.get('localisation', '')
        taille = request.POST.get('taille', '')

        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()

        profile.bio = bio
        profile.localisation = localisation
        profile.date_d_anniversaire = date_d_anniversaire
        profile.numero = numero
        profile.age = age
        profile.profession = profession
        profile.genre = genre
        profile.sex = sex
        profile.corpulence = corpulence
        profile.couleur_de_peau = couleur_de_peau
        profile.taille = taille

        if 'image' in request.FILES:
            profile.image = request.FILES['image']

        profile.save()

        messages.success(request, 'Votre profil a été mis à jour avec succès!')
        return redirect('profil')

    return render(request, 'Both/modif.html', {'user': user, 'profile': profile})


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
def chat_index(request):
    user = request.user.profile
    friends = user.friends.all()
    return render(request, "Both/chat_index.html", {"user": user, "friends": friends})


def detail(request, pk):
    friend = get_object_or_404(Profile, id=pk)
    user_profile = request.user.profile

    if not user_profile.friends.filter(id=friend.id).exists():
        messages.error(request, "Vous devez être amis pour discuter.")
        return redirect('profil')

    if request.method == "POST":
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.msg_sender = user_profile
            chat_message.msg_receiver = friend
            chat_message.save()
            messages.success(request, "Message envoyé avec succès.")
            return redirect('detail', pk=friend.id)
        else:
            messages.error(request, "Erreur lors de l'envoi du message.")
    else:
        form = ChatMessageForm()

    return render(request, "Both/detail.html", {"friend": friend, "form": form, "user": user_profile})


@csrf_exempt
@require_POST
@login_required
def sentMessages(request, pk):
    try:
        user_profile = request.user.profile
        friend = get_object_or_404(Profile, id=pk)
        data = json.loads(request.body)
        new_chat = data.get("msg", "").strip()
        if not new_chat:
            return JsonResponse({"error": "Message vide."}, status=400)

        new_chat_message = ChatMessage.objects.create(
            body=new_chat,
            msg_sender=user_profile,
            msg_receiver=friend,
            seen=False
        )
        return JsonResponse({"message": "Message envoyé avec succès."})
    except json.JSONDecodeError:
        return JsonResponse({"error": "Données JSON invalides."}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_POST
@login_required
def receivedMessages(request, pk):
    try:
        user_profile = request.user.profile
        friend = get_object_or_404(Profile, id=pk)
        chats = ChatMessage.objects.filter(msg_sender=friend, msg_receiver=user_profile)
        messages = [chat.body for chat in chats]
        if not messages:
            return JsonResponse({"messages": [], "info": "Aucun message reçu."})
        return JsonResponse({"messages": messages})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def suggestions(request):
    preferences = get_object_or_404(Preferences, user=request.user)
    profiles = Profile.objects.filter(
        age__gte=preferences.age_min,
        age__lte=preferences.age_max,
        taille__gte=preferences.taille_min,
        taille__lte=preferences.taille_max,
        couleur_de_peau=preferences.teint_preference,
        corpulence=preferences.corpulence_preference,
        localisation=preferences.localisation_preference,
        genre='Feminin' if request.user.profile.genre == 'Masculin' else 'Masculin'
    )
    return render(request, 'Both/suggestions.html', {'profiles': profiles})


@login_required
def respond_to_suggestion(request, profile_id):
    user = request.user.profile
    profile = get_object_or_404(Profile, id=profile_id)

    if request.method == 'POST':
        response = request.POST.get('response')  # "yes" ou "no"

        if response == "yes":
            # Créer une relation Friend si elle n'existe pas déjà
            friend, created = Friend.objects.get_or_create(profile=user)
            friend_of_profile, created = Friend.objects.get_or_create(profile=profile)

            # Ajouter les amis mutuels
            user.friends.add(friend_of_profile)
            profile.friends.add(friend)

            # Vérifiez si l'autre utilisateur a aussi accepté la suggestion
            if profile.friends.filter(id=user.id).exists():
                # Les deux utilisateurs ont accepté, la messagerie peut être débloquée
                pass

        # Rediriger vers la page des suggestions après avoir enregistré la réponse
        return redirect('suggestions')

    return render(request, 'Both/connect_request.html', {'target_profile': profile})


@login_required
def load_suggestions(request):
    suggestions = Profile.objects.all()[:5]

    suggestions_data = []
    for profile in suggestions:
        suggestions_data.append({
            'user': {
                'username': profile.user.username,
            },
            'photo_url': profile.photo.url
        })

    return JsonResponse(suggestions_data, safe=False)


@login_required
def chatNotification(request):
    user = request.user.profile
    friends = user.friends.all()
    arr = []
    for friend in friends:
        chats = ChatMessage.objects.filter(msg_sender__id=friend.profile.id, msg_receiver=user, seen=False)
        arr.append(chats.count())
    return JsonResponse(arr, safe=False)