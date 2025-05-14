import django.db
from django.shortcuts import render, redirect
from .models import Game, Genre, Theme


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

    return render(request,'search_game.html',context)

def game_add(request):
    if request.method == 'GET':
        game_id = request.GET['game_id']
        try: # create game if not in DB
            game_info = Game.game_id_search(game_id)
            # temp add in
            game = Game.objects.create(**game_info)
            game_info = game.self_search()
            for genre_type in game_info['genres']:
                try:
                    genre = Genre.objects.create(type=genre_type)
                except django.db.IntegrityError: # grab instance of genre instead
                    genre = Genre.objects.get(type=genre_type)
                game.genres.add(genre)
            for theme_type in game_info['themes']:
                try:
                    theme = Theme.objects.create(type=theme_type)
                except django.db.IntegrityError: # grab instance of genre instead
                    theme = Theme.objects.get(type=theme_type)
                game.themes.add(theme)
            game.save()
            # alternatively could grab list of all game_id, genres, and themes but not sure if using try/except is just faster than searching through N instances
        except django.db.IntegrityError: # grab instance of game instead
            game = Game.objects.get(game_id=game_id)
    return render(request, 'search_game.html',{})


