from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request,'inscription.html')

def informations_views(request):
    return render(request,'informations_personnelles.html')