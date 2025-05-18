from django import forms
from .models import DiaryEntry
from datetime import date

class DiaryEntryForm(forms.ModelForm):
    PLATFORM_CHOICES = [
        ('none', 'No Preference'),
        ('ps4', 'PlayStation 4'),
        ('ps5', 'PlayStation 5'),
        ('xbox-xs', 'XBOX Series X|S'),
        ('xbox-one', 'Xbox One'),
        ('switch', 'Nintendo Switch'),
        ('pc', 'PC / Steam'),
    ]

    review = forms.CharField(widget=forms.Textarea, max_length=200, label='')
    platform = forms.ChoiceField(choices=PLATFORM_CHOICES, required=True)
    rating = forms.FloatField(min_value=0, max_value=5, step_size=0.5)
    completed_date = forms.DateField(initial=date.today())
    completion_status = forms.BooleanField(label='Did you complete the game?')
    hours = forms.IntegerField(min_value=0)
    class Meta:
        model = DiaryEntry
        fields = ('review', 'platform', 'rating', 'completed_date', 'completion_status', 'hours')
