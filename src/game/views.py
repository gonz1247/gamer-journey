from django.shortcuts import render
from .models import Game


# Create your views here.
def search_view(request):
    context = {}
    if request.method == 'POST': # Search has been initiated
        # extract info from POST
        title = request.POST['title']
        # search for title
        results = Game.game_search(title)
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

