from django.shortcuts import render

from .forms import DiaryEntryForm
from game.models import Game

# Create your views here.
def diary_entry_view(request, game_id):
    game = Game.add_or_grab_game(game_id)
    form = DiaryEntryForm()
    context = {
        'form':form,
        'game':game,
    }
    print(form)
    return render(request, 'diary/diary_entry.html', context)
