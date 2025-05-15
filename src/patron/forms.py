from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Patron
from django.contrib.auth.models import User

class PatronRegisterForm(UserCreationForm):
    PLATFORM_CHOICES = [
        ('ps4', 'PlayStation 5'),
        ('ps5', 'PlayStation 5'),
        ('xbox-xs', 'XBOX Series X|S'),
        ('xbox-one', 'Xbox One'),
        ('switch', 'Nintendo Switch'),
        ('pc', 'PC / Steam'),
    ]
    fav_platform = forms.ChoiceField(label='Preferred Platform', choices=PLATFORM_CHOICES)
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('fav_platform',)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=True)
        patron = Patron(user=user, fav_platform=self.cleaned_data['fav_platform'])
        patron.save()
        return user

