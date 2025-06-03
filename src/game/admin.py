from django.contrib import admin
from .models import Game, Platform

# Register your models here.
admin.site.register(Platform)
admin.site.register(Game)