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
    path('login/',LoginView.as_view(template_name = 'Both/login.html', next_page='suggestions' ) , name='login'),
    path('contact/',views.contact_views,name='contact'),
    path('logout/',LogoutView.as_view(next_page='login' ) ,name='logout'), 
    path('suggestions/', views.suggestion_view, name='suggestions'), 
    path('profile/<str:username>/', views.profile_detail_view, name='profile_detail'),
    path('add_user/', lambda request: HttpResponse('Page blanche vide'), name='add_user'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset/done/', views.mailsend, name='password_reset_done'),
    path('reset/', views.newpass, name='password_reset_confirm'),
    path('done/',views.done , name='password_reset_complete'),
    path('formulaire_recherche/', views.formulaire_recherche, name='formulaire_recherche'),
    path('recherche-restaurants/', views.recherche_restaurants, name='recherche_restaurants'),
    path('accept_suggestions/<int:profile_id>/', views.accept_suggestion, name='accept_suggestions'),
    path('conversation_list/', views.conversation_list , name='conversation_list'),
    path('conversation_detail/<int:coversation_id>/', views.conversation_detail , name='conversation_detail'),
    path('send_message/',views.send_message , name = 'send_message'),

]



    

