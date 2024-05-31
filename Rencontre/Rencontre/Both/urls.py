from django.urls import path
from app.views import index, about, contact, informations_personnelles, login, watch, inscription
urlpatterns = [

    path('' ,index , name="index"),
    path('' ,about , name="about"),
    path('' ,contact , name="contact"),
    path('' ,informations_personnelles , name="informations_personnelles"),
    path('' ,login , name="login"),
    path('' ,watch , name="watch"),
    path('' ,inscription , name="inscription"),



]
