from typing import Any
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render , redirect , get_object_or_404
#from django.contrib.auth.forms import UserCreationForm
from .form import MyUserForm, ProfileForm,ChatMessageForm
from .models import Friend, Profile
from django.contrib.auth.views import LoginView


@login_required
def view_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'Both/profil.html', {'profile': profile})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        print(request.FILES)
        form = ProfileForm(request.POST,request.FILES, instance=request.user.profile)
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


def chat_index(request):
    user=request.user.profile
    friends= user.friends.all()
    context = {"user": user , "friends":friends}
    return render (request , "Both/chat_index.html" , context)

def detail(request, pk):
    friend=Friend.objects.get(profile_id=pk)
    form = ChatMessageForm
    context = {"friend" : friend , "form":form}
    return render (request , "Both/detail.html" , context)