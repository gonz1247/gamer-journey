from django.shortcuts import render
from .models import Game


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
            # Grab picture of resulting games
            for game in results:
                if game.get('cover'):
                    game['cover'] = game['cover']['url']
                else:
                    game['cover'] = None
            context = {'games': results}
        else:
            context = {'no_results':True}

    context['patron'] = "Gonzo"
    return render(request,'search_game.html',context)

def game_add(request):
    context = {}
    if request.method == 'GET':
        game_id = request.GET['game_id']
        game_info = Game.game_id_search(game_id)
        print(game_info)
    return render(request, 'search_game.html', context)

