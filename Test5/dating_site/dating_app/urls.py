from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('preferences/<int:user_id>/', views.preferences, name='preferences'),
    path('suggestions/<int:user_id>/', views.suggestions, name='suggestions'),
    
]
