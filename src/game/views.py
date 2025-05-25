import django.db, random
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
        context = {'pop_games': pop_games}
        return render(request, 'game/popular_games.html', context)
    else:
        message = "Sign in to start using Gamer Journey's search features"
        context = {'error_message':message}
        return render(request, 'error.html', context)

def suggestions_view(request):
    user = request.user
    if user.is_authenticated:
        if 'suggest_remove_wishlist_id' in request.POST or 'suggest_add_game_id' in request.POST:
            # update wishlist
            return wishlist_view(request)
        # grab top 3 games from diary & start to create a set of what games the patron knows about already
        current_diary_sorted = sorted(user.patron.diaryentry_set.all(), key=lambda entry: entry.rating)
        top3_games = list()
        known_games = set()
        for entry in current_diary_sorted:
            if len(top3_games) < 3: top3_games.append(entry.game.game_id)
            known_games.add(entry.game.game_id)
        # Add patron's wishlist to set of known games
        for game in user.patron.wishlist.all():
            known_games.add(game.game_id)
        # find all new games that can be suggested to the patron
        new_games = set()
        for game_id in top3_games:
            [results] = Game.game_id_search(game_id=game_id, fields='similar_games.*')
            for sg in results['similar_games']:
                new_game = sg['id']
                if new_game not in known_games:
                    new_games.add(new_game)
        new_games = list(new_games)
        # grab up to 10 games to suggest to the patron
        suggested_games = list()
        max_games = min(10, len(new_games))
        while len(suggested_games) < max_games:
            suggested_games.append(new_games.pop(random.randint(0, len(new_games)-1)))
        # Populate info for the suggested games
        for idx, game_id in enumerate(suggested_games):
            suggested_games[idx] = Game.add_or_grab_game(game_id)
        context = {'pop_games': suggested_games}
        return render(request, 'game/suggested_games.html', context)
    else:
        message = "Sign in to start using Gamer Journey's search features"
        context = {'error_message': message}
        return render(request, 'error.html', context)





