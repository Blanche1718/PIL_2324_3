<<<<<<< HEAD

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static



=======
"""
URL configuration for Rencontre project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

app_name = 'Both'
app_name = 'a_rtchat'
>>>>>>> 5dc269b1eb8fbed39675ddfca1070a22da0419d4

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Both/', include('Both.urls')),
<<<<<<< HEAD
<<<<<<< HEAD:Rencontre/Rencontre/Rencontre/urls.py
    path('', include('Both.urls')),
    path('accounts/', include ('allauth.urls')),
    path('chat/', include('a_rtchat.urls')),
=======
=======
>>>>>>> 5dc269b1eb8fbed39675ddfca1070a22da0419d4
    path('', include('Both.urls')),  # Route racine dirigée vers Both
    path('accounts/', include ('allauth.urls')),
    path('home/', include('a_rtchat.urls')),
]
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView , LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Both.urls')),
    path('accounts/', include ('allauth.urls')),
    path('home/', include('a_rtchat.urls')),
    path('logout', LogoutView.as_view(next_page='login' ), name='logout')
<<<<<<< HEAD
>>>>>>> 5dc269b1eb8fbed39675ddfca1070a22da0419d4:Rencontre/Rencontre/urls.py
    # vos autres URL patterns ici
]
if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
    # vos autres URL patterns ici
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
>>>>>>> 5dc269b1eb8fbed39675ddfca1070a22da0419d4
