from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django import forms
from .models import Patron
from django.contrib.auth.models import User

# Keeping the platform choice to last two generations
# Could in theory query the database to grab all possible options but that seems like it would be too much
PLATFORM_CHOICES = {
        'none':'No Preference',
        'Android': 'Android',
        'iOS': 'iOS',
        'Mac': 'Mac',
        'Nintendo Switch': 'Nintendo Switch',
        'Nintendo Switch 2': 'Nintendo Switch 2',
        'PlayStation 4':'PlayStation 4',
        'PlayStation 5':'PlayStation 5',
        'PC (Microsoft Windows)': 'PC',
        'Xbox One': 'Xbox One',
        'Xbox Series X|S':'Xbox Series X|S',
    }

class PatronRegisterForm(UserCreationForm):
    fav_platform = forms.ChoiceField(label='Preferred Platform', choices=PLATFORM_CHOICES, initial='none')
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'fav_platform')
        help_texts = {
            'username': None,
            'password1': None, # these do no work for some reason
            'password2': None, # these do no work for some reason
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Required'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Optional'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Optional'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Optional'}),
        }


    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=True)
        patron = Patron(user=user, fav_platform=self.cleaned_data['fav_platform'])
        patron.save()
        return user

class PatronUpdateForm(UserChangeForm):
        password = None
        fav_platform = forms.ChoiceField(label='Preferred Platform', choices=PLATFORM_CHOICES, initial='none')
        success_message = forms.CharField(widget=forms.HiddenInput, max_length=50, initial='Profile Was Successfully Updated.')

        class Meta:
            model = User
            fields = ('first_name', 'last_name', 'email', 'fav_platform')

        def save(self, commit=True):
            user = super(UserChangeForm, self).save(commit=True)
            patron = User.objects.get(pk=user.pk).patron
            patron.fav_platform = self.cleaned_data['fav_platform']
            patron.save()
            return user

class PasswordUpdateForm(PasswordChangeForm):
    # Only making my own form so that I can add the success message
    success_message = forms.CharField(widget=forms.HiddenInput, max_length=50, initial='Password Was Successfully Updated.')

    class Meta:
        model = User