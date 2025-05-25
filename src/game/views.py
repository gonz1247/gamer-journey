import django.db
from django.shortcuts import render, redirect
from .models import Game, Genre, Theme, Platform
from patron.views import wishlist_view


# Create your views here.
def search_view(request):
    user = request.user
    if user.is_authenticated:
        context = {}
        if request.method == "POST":
            if 'game_id' in request.POST: # Search is complete add game to wishlist
                if user.is_authenticated:
                    game_id = request.POST['game_id']
                    game = Game.add_or_grab_game(game_id)
                    user.patron.wishlist.add(game)
                    context = {'confirm_message': (game.title + ' has been added to your wishlist!')}
                else:
                    message = 'Must be signed in add games to a wishlist.'
                    context = {'error_message': message}
                    return render(request, 'error.html', context)
            else: # Search has been initiated
                # extract info from POST
                title = request.POST['title']
                # search for title
                results = Game.title_search(title)
                # show results that come back
                if results:
                    context = {'games': results,
                               'searched_title':title}
                else:
                    context = {'no_results':True,
                               'searched_title':title}
        return render(request,'game/search_game.html',context)
    else:
        message = "Sign in to start using Gamer Journey's search features"
        context = {'error_message':message}
        return render(request, 'error.html', context)

def game_add(request):
    if request.method == 'POST':
        game_id = request.POST['game_id']
        game = Game.add_or_grab_game(game_id)
    return render(request, 'game/search_game.html',{})

def popular_view(request):
    user = request.user
    if user.is_authenticated:
        if 'pop_remove_wishlist_id' in request.POST or 'pop_add_game_id' in request.POST:
            return wishlist_view(request)
        # Get Current Top 10 Games
        results = Game.popular_search(limit=10)
        pop_games = list()
        for r in results:
            game = Game.add_or_grab_game(r['game_id'])
            pop_games.append(game)
        # Grab patron's current wishlist
        current_wishlist = user.patron.wishlist.all()
        context = {'wishlist': current_wishlist}
        context = {'pop_games': pop_games}
        return render(request, 'game/popular_games.html', context)
    else:
        message = "Sign in to start using Gamer Journey's search features"
        context = {'error_message':message}
        return render(request, 'error.html', context)




