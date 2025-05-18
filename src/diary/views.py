from django.shortcuts import render, redirect

from .forms import DiaryEntryForm
from game.models import Game
from game.models import Platform

# Create your views here.
def diary_entry_view(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            # add game to diary
            form = DiaryEntryForm(request.POST)
            # add in choice field since this is dynamically when first loading the diary add page
            form.fields['platform'].choices = {request.POST['platform']:request.POST['platform']}
            if form.is_valid():
                form.save()
                return redirect('home')
            else:
                error_message = []
                for [error] in form.errors.values():
                    error_message.append(error)
                context = {'error_message':error_message}
                return render(request, 'error.html', context)
        else: # get method being sent from game search
            # grab game info to display on the diary entry page
            game_id = request.GET['game_id']
            game = Game.add_or_grab_game(game_id)
            # look up what platforms the game is available on and add options to form
            platforms = {p.device:p.device for p in game.platforms.all()}
            form = DiaryEntryForm(initial={'game':game_id, 'patron':user.patron.pk})
            form.fields['platform'].choices = platforms
            context = {
                'form':form,
                'game':game,
            }
        return render(request, 'diary/diary_entry.html', context)
    else:
        message = 'Must be signed in to add entries to your diary.'
        context = {'error_message':message}# change this to go to an error page
        return render(request, 'error.html', context)

def my_diary_view(request):
    user = request.user
    if user.is_authenticated:
        current_diary = user.patron.diaryentry_set.all()
        context = {'diary': current_diary}
        return render(request, 'diary/my_diary.html', context)
    else:
        message = 'Must be signed in to view diary.'
        context = {'error_message': message}  # change this to go to an error page
        return render(request, 'error.html', context)
