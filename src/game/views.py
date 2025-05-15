import django.db
from django.shortcuts import render, redirect
from .models import Game, Genre, Theme, Platform


# Create your views here.
def search_view(request):
    context = {}
    if request.method == 'POST': # Search has been initiated
        # extract info from POST
        title = request.POST['title']
        # search for title
        results = Game.title_search(title)
        # show results that come back
        if results:
            context = {'games': results}
        else:
            context = {'no_results':True}

    return render(request,'game/search_game.html',context)

def game_add(request):
    if request.method == 'POST':
        game_id = request.POST['game_id']
        game = Game.add_or_grab_game(game_id)
        print(game.title)
    return render(request, 'game/search_game.html',{})


