from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from django.shortcuts import render , redirect
from .form import LoginForm
from django.http import HttpResponse

urlpatterns = [
    path('', views.index, name='index'),
    path('profil/', views.view_profile, name='profil'),
    path('modif/', views.edit_profile, name='modif'),
    path('inscription/',views.inscription_views,name='inscription'),
    path('login/', views.Myloginview.as_view(), name='login'),
    path('login/',LoginView.as_view(template_name = 'Both/login.html', next_page='profil' ) , name='login'),
    path('informations/',views.informations_views,name='Informations'),
    path('contact/',views.contact_views,name='contact'),
    path('logout/',LogoutView.as_view(next_page='login' ) ,name='logout'),
    path('suggestions/', views.suggestions, name='suggestions'),
    path('user/<int:pk>/', views.user_detail, name='user_detail'),
    path('add_user/', lambda request: HttpResponse('Page blanche vide'), name='add_user'),
    path('chats/', views.chat_index, name='chats'),
    path('friend/<str:pk>', views.detail, name='detail'),
    path("sent_msg",views.sentMessages, name="sent_msg")


]
    
