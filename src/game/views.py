import django.db, random
from django.shortcuts import render, redirect
from .models import Game
from .forms import CacheSearch

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
                    [game_info] = Game.game_id_search(game_id,fields='name')
                    user.patron.wishlist.add(game)
                    context = {'confirm_message': (game_info['title'] + ' has been added to your wishlist!')}
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
        if request.method == 'POST':
            if 'pop_add_game_id' in request.POST:  # add a game to wishlist and then go back to popular games screen
                game_id = request.POST['pop_add_game_id']
                game = Game.add_or_grab_game(game_id)
                user.patron.wishlist.add(game)
            if 'pop_remove_wishlist_id' in request.POST:  # remove a game from wishlist and then go back to popular games screen
                wishlist_id = request.POST['pop_remove_wishlist_id']
                game = user.patron.wishlist.get(game_id=wishlist_id)
                user.patron.wishlist.remove(game)
            # recall cached data for suggestions page and recache it
            pop_games = request.POST['games']
            form = CacheSearch(initial={'games': pop_games})
            pop_games = pop_games.split(',')
            # Populate info for the suggested games
            pop_games = Game.game_id_search(pop_games, fields='name,cover.*,platforms.*')
            # Check to see which games are in user wishlist
            for game in pop_games:
                if game['game_id'] in user.patron.wishlist.all().values_list('game_id', flat=True):
                    game['in_wishlist'] = True
                else:
                    game['in_wishlist'] = False
            context = {'pop_games': pop_games,
                       'form': form}
        else:
            # Get Current Top 10 Games
            results = Game.popular_search(limit=10)
            pop_games = [str(r['game_id']) for r in results]
            # cache the top 10 games so can display the exact same list after patron adds games to wishlist (incase IGDB changes right at that time)
            initial = ','.join(pop_games)
            form = CacheSearch(initial={'games': initial})
            # Populate info for the suggested games
            pop_games = Game.game_id_search(pop_games, fields='name,cover.*,platforms.*')
            # Check to see which games are in user wishlist
            for game in pop_games:
                if game['game_id'] in user.patron.wishlist.all().values_list('game_id',flat=True):
                    game['in_wishlist'] = True
                else:
                    game['in_wishlist'] = False
            context = {'pop_games': pop_games,
                       'form': form}
        return render(request, 'game/popular_games.html', context)
    else:
        message = "Sign in to start using Gamer Journey's search features"
        context = {'error_message':message}
        return render(request, 'error.html', context)

def suggestions_view(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            if 'suggest_add_game_id' in request.POST:  # add a game to wishlist and then go back to suggested games screen
                game_id = request.POST['suggest_add_game_id']
                game = Game.add_or_grab_game(game_id)
                user.patron.wishlist.add(game)
            elif 'suggest_remove_wishlist_id' in request.POST:  # remove a game from wishlist and then go back to suggested games screen
                wishlist_id = request.POST['suggest_remove_wishlist_id']
                game = user.patron.wishlist.get(game_id=wishlist_id)
                user.patron.wishlist.remove(game)
            # recall cached data for suggestions page and recache it
            suggested_games = request.POST['games']
            form = CacheSearch(initial={'games':suggested_games})
            suggested_games = suggested_games.split(',')
            # Populate info for the suggested games
            suggested_games = Game.game_id_search(suggested_games, fields='name,cover.*,platforms.*')
            # Check to see which games are in user wishlist (since just added one or more form suggested list)
            for game in suggested_games:
                if game['game_id'] in user.patron.wishlist.all().values_list('game_id', flat=True):
                    game['in_wishlist'] = True
                else:
                    game['in_wishlist'] = False
            context = {'pop_games': suggested_games,
                       'form': form}
        else:
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
            top3_games_info = Game.game_id_search(game_id=top3_games, fields='similar_games.*')
            for game_info in top3_games_info:
                for new_game in game_info['similar_games']:
                    if new_game not in known_games:
                        new_games.add(new_game)
            new_games = list(new_games)
            # grab up to 10 games to suggest to the patron
            suggested_games = list()
            max_games = min(10, len(new_games))
            while len(suggested_games) < max_games:
                suggested_games.append(new_games.pop(random.randint(0, len(new_games)-1)))
            # cache the suggested items so can display the exact same list after patron adds games to wishlist
            initial = ','.join([str(game_id) for game_id in suggested_games])
            form = CacheSearch(initial={'games':initial})
            # Populate info for the suggested games
            suggested_games = Game.game_id_search(suggested_games, fields='name,cover.*,platforms.*')
            context = {'pop_games': suggested_games,
                       'form': form}
        return render(request, 'game/suggested_games.html', context)
    else:
        message = "Sign in to start using Gamer Journey's search features"
        context = {'error_message': message}
        return render(request, 'error.html', context)