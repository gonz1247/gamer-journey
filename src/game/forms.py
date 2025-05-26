from django import forms
from django.forms import HiddenInput
from dotenv.main import with_warn_for_invalid_lines


class CacheSearch(forms.Form):
    games = forms.CharField(max_length=100, widget=HiddenInput)