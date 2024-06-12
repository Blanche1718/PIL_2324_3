from django.urls import path
from django.contrib.auth import views  as auth_views
from . import views
from django.shortcuts import render , redirect
from .form import LoginForm

urlpatterns = [
    path('', views.index, name='index'),
    path('profil/', views.profil_views, name='profil'),
    path('modif/', views.modif_views, name='modif'),
    path('inscription/',views.inscription_views,name='inscription'),
    path('login/',auth_views.LoginView.as_view(template_name = 'Both/login.html', ) , name='login'),
    path('informations/',views.informations_views,name='Informations'),
    path('contact/',views.contact_views,name='contact'),
    path('logout/',auth_views.LogoutView.as_view(template_name = 'Both/logout.html', next_page='login') , name='logout'),
]
    
