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
    path('preferences/', views.edit_preferences, name='edit_preferences'),  
    path('suggestions/', views.suggestions, name='suggestions'), 
    path('restaurant/', views.restaurant_suggestions, name='restaurant'),
    path('results/<str:budget_level>/<str:preferred_cuisine>/', views.show_results, name='suggestions'),
    path('add_user/', lambda request: HttpResponse('Page blanche vide'), name='add_user'),
    path('chats/', views.chat_index, name='chats'),
    path('friend/<str:pk>', views.detail, name='detail'),
    path('sent_msg/<str:pk>',views.sentMessages, name='sent_msg'),
    path('rec_msg/<str:pk>',views.receivedMessages, name='rec_msg'),
    path('notification',views.chatNotification, name='notification'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('connect_request/',views.respond_to_suggestion, name='suggestion_reponse'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset/done/', views.mailsend, name='password_reset_done'),
    path('reset/', views.newpass, name='password_reset_confirm'),
    path('done/',views.done , name='password_reset_complete'),




    
]
    
