
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path('Both/', include('Both.urls')),
    path('', include('Both.urls')),
    path('accounts/', include ('allauth.urls')),
    path('chat/', include('a_rtchat.urls')),
    # vos autres URL patterns ici
]
if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
