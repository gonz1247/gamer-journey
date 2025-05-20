"""
URL configuration for gamer_journey project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from .views import diary_entry_view, my_diary_view, diary_edit_view, diary_delete_view

urlpatterns = [
    path('', my_diary_view, name='diary'),
    path('add/', diary_entry_view),
    path('edit/<int:entry_id>/', diary_edit_view),
    path('delete/<int:entry_id>/', diary_delete_view)
]
