from django.contrib import admin
from .models import *
admin.site.register([Profile, Friend, ChatMessage, Restaurant, Preferences])

# Register your models here.
