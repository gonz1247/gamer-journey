from django import forms
from django.forms import HiddenInput

class CacheSearch(forms.Form):
    games = forms.CharField(max_length=100, widget=HiddenInput)