
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path('Both/', include('Both.urls')),
<<<<<<< HEAD:Rencontre/Rencontre/Rencontre/urls.py
    path('', include('Both.urls')),
    path('accounts/', include ('allauth.urls')),
    path('chat/', include('a_rtchat.urls')),
=======
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
>>>>>>> 5dc269b1eb8fbed39675ddfca1070a22da0419d4:Rencontre/Rencontre/urls.py
    # vos autres URL patterns ici
]
if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
