from django import forms
from .models import DiaryEntry
from game.models import Platform, Game
from patron.models import Patron
from datetime import date
import django.db

class DiaryEntryForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea, max_length=200, label='', required=False)
    platform = forms.ChoiceField(label='Played Platform*', required=True)
    rating = forms.ChoiceField(choices={val/10:val/10 for val in range(0,55,5)}, help_text='Star Rating', required=False)
    completed_date = forms.DateField(initial=date.today(), label='Date Completed*', required=True)
    completion_status = forms.BooleanField(label='Did you complete the game?', initial=False, required=False)
    hours = forms.IntegerField(min_value=0, required=False)
    # these will be initialized with the form
    game = forms.IntegerField(widget=forms.HiddenInput)
    patron = forms.IntegerField(widget=forms.HiddenInput)
    class Meta:
        model = DiaryEntry
        fields = ('review', 'platform', 'rating', 'completed_date', 'completion_status', 'hours', 'game', 'patron')


    def clean_platform(self):
        platform_name = self.cleaned_data['platform']
        try:
            platform = Platform.objects.create(device=platform_name)
        except django.db.IntegrityError:
            platform = Platform.objects.get(device=platform_name)
        return platform

    def clean_game(self):
        game_id = self.cleaned_data['game']
        game = Game.add_or_grab_game(game_id)
        return game

    def clean_patron(self):
        patron_id = self.cleaned_data['patron']
        patron = Patron.objects.get(pk=patron_id)
        return patron

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if isinstance(rating,int):
            rating = float(rating)
        return rating




