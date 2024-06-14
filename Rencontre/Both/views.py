from django.contrib.auth.decorators import login_required
from django.shortcuts import render , redirect , get_object_or_404
#from django.contrib.auth.forms import UserCreationForm
from .form import MyUserForm, ProfileForm
from .models import Profile
#from django.contrib.auth.decorators import login_required

def view_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'Both/profil.html', {'profile': profile})

def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('suggestions')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'Both/modif.html', {'form': form})


def inscription_views(request):
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