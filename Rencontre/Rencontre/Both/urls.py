from django.urls import path
from Both.views import index, about, contact, informations_personnelles, login, watch, inscription
urlpatterns = [
<<<<<<< HEAD
    path('', views.index, name='index'),
    path('profil', views.profil_views, name='profil'),
    path('modif/', views.modif_views, name='modif'),
    path('inscription/',views.inscription_views,name='inscription'),
    path('login/',views.login_views,name='login'),
    path('informations/',views.informations_views,name='Informations'),
    path('contact/',views.contact_views,name='contact'),
=======

    path('' ,index , name="index"),
    path('' ,about , name="about"),
    path('' ,contact , name="contact"),
    path('' ,informations_personnelles , name="informations_personnelles"),
    path('' ,login , name="login"),
    path('' ,watch , name="watch"),
    path('' ,inscription , name="inscription"),



>>>>>>> 53ae2a3799fe4bf72b3dd84ebe5b2618958a8ef4
]
    
