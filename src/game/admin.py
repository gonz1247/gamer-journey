from django.contrib import admin
from .models import Game, Theme, Genre, Platform

# Register your models here.
admin.site.register(Theme)
admin.site.register(Genre)
admin.site.register(Platform)
admin.site.register(Game)