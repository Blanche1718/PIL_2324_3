from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    """
    path('login/', views.login_views, name='connexion'),  # URL pour la page de connexion
    """
    path('informations/', views.informations_views, name='Informations'),  # URL pour la page d'informations
]
