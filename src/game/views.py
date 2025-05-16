import django.db
from django.shortcuts import render, redirect
from .models import Game, Genre, Theme, Platform


# Create your views here.
def search_view(request):
    context = {}
    user = request.user
    if request.method == "POST":
        if 'game_id' in request.POST: # Search is complete add game to wishlist
            if user.is_authenticated:
                game_id = request.POST['game_id']
                game = Game.add_or_grab_game(game_id)
                user.patron.wishlist.add(game)
                context = {'confirm_message': (game.title + ' has been added to your wishlist!')}
            else:
                message = 'Must be signed in add games to a wishlist.'
                context = {'error_message': message}  # change this to go to an error page
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
                context = {'no_results':True}

    return render(request,'game/search_game.html',context)

def game_add(request):
    if request.method == 'POST':
        game_id = request.POST['game_id']
        game = Game.add_or_grab_game(game_id)
        print(game.title)
    return render(request, 'game/search_game.html',{})


