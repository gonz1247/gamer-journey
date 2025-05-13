from django.shortcuts import render
from .models import Game, Genre,Theme


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

    context['patron'] = "Gonzo"
    return render(request,'search_game.html',context)

def game_add(request):
    context = {}
    if request.method == 'GET':
        game_id = request.GET['game_id']
        game_info = Game.game_id_search(game_id)
        # temp add in
        game = Game.objects.create(**game_info)
        game_info = game.self_search()
        for genre_type in game_info['genres']:
            genre = Genre.objects.create(type=genre_type)
            game.genres.add(genre)
        for theme_type in game_info['themes']:
            theme = Theme.objects.create(type=theme_type)
            game.themes.add(theme)
        game.save()


    return render(request, 'search_game.html', context)

