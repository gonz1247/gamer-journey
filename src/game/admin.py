from django.contrib import admin
from .models import Game, Theme, Genre

# Register your models here.
admin.site.register(Theme)
admin.site.register(Genre)
admin.site.register(Game)