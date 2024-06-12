
from django.shortcuts import render , redirect
#from django.contrib.auth.forms import UserCreationForm
from .form import MyUserForm

#from django.contrib.auth.decorators import login_required

def profil_views(request):
    return render(request, 'Both/profil.html')

def modif_views(request):
    return render(request, 'Both/modif.html')



def inscription_views(request):
    #if request.user.is_authenticated:
        #return redirect('index')
    if request.method == 'POST':
        form = MyUserForm(request.POST)

        if form.is_valid():
            form.save()
    
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

