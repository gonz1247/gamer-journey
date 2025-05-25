# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash

from .forms import PatronRegisterForm, PatronUpdateForm, PasswordUpdateForm
from .models import User
from game.models import Game
import datetime

def profile_view(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            success_message = request.POST['success_message']
        else:
            success_message = None
        # generate gamer stats based on diary entries
        current_diary = user.patron.diaryentry_set.all()
        genre_track = dict()
        theme_track = dict()
        fav_genre = ('N/A',-1)
        fav_theme = ('N/A', -1)
        fav_game = ('N/A', -1)
        longest_game = ('N/A', -1)
        most_recent_game = ('N/A', datetime.date(1, 1, 1))
        for entry in current_diary:
            # track favorite genre
            for genre in entry.game.genres.all():
                if genre.type in genre_track:
                    # increment times this genre has appeared in diary
                    genre_track[genre.type] += 1
                    if fav_genre[1] < genre_track[genre.type]:
                        fav_genre = (genre.type, genre_track[genre.type])
                else:
                    genre_track[genre.type] = 1
            # track favorite theme
            for theme in entry.game.themes.all():
                if theme.type in theme_track:
                    # increment times this genre has appeared in diary
                    theme_track[theme.type] += 1
                    if fav_theme[1] < theme_track[theme.type]:
                        fav_theme = (theme.type, theme_track[theme.type])
                else:
                    theme_track[theme.type] = 1
            # track favorite game
            if entry.rating >= fav_game[1]:
                fav_game = (entry.game, entry.rating)
            # track game that took the longest to beat
            if entry.hours: # default is None
                if entry.hours >= longest_game[1]:
                    longest_game = (entry.game, entry.hours)
            # track most recently completed game (may not be last added entry)
            if entry.completed_date >= most_recent_game[1]:
                most_recent_game = (entry.game, entry.completed_date)

        context = {
            'fav_genre':fav_genre[0],
            'fav_theme':fav_theme[0],
            'fav_game':fav_game[0],
            'longest_game':longest_game[0],
            'most_recent_game':most_recent_game[0],
            'success_message': success_message,
        }
        return render(request, 'patron/profile.html', context)
    else:
        message = 'Must be signed in to view your profile.'
        context = {'error_message': message}
        return render(request, 'error.html', context)

def register_view(request):
    error_message = None
    if request.method == "POST":
        form = PatronRegisterForm(request.POST)
        if form.is_valid():
            patron = form.save()
            login(request, patron)
            return redirect('home')
        else:
            error_message = []
            for [error] in form.errors.values():
                error_message.append(error)
    form = PatronRegisterForm()
    # Can only make edits to how password1 and password2 appear after form has been initialized, only way I got it to work
    form.fields['password1'].help_text = None
    form.fields['password1'].widget.attrs['placeholder'] = 'Required'
    form.fields['password2'].help_text = None
    form.fields['password2'].widget.attrs['placeholder'] = 'Required'
    context = {
        'form': form,
        'error': error_message,
    }
    return render(request, "patron/register.html", context)

def update_info_view(request):
    user = request.user
    if user.is_authenticated:
        error_message = None
        if request.method == "POST":
            form = PatronUpdateForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return  profile_view(request)
            else:
                error_message = []
                for [error] in form.errors.values():
                    error_message.append(error)
        form = PatronUpdateForm(instance=user)
        form.initial['fav_platform'] = user.patron.fav_platform
        context = {
            'form': form,
            'error': error_message,
        }
        return render(request, "patron/update_profile.html", context)
    else:
        return redirect('/profile/register/')

def update_pw_view(request):
    user = request.user
    if user.is_authenticated:
        error_message = None
        if request.method == "POST":
            form = PasswordUpdateForm(user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                return  profile_view(request)
            else:
                error_message = []
                for errors in form.errors.values():
                    for error in errors:
                        error_message.append(error)
        form = PasswordUpdateForm(user)
        form.fields['new_password1'].help_text = None
        form.fields['new_password2'].help_text = None
        context = {
            'form': form,
            'error': error_message,
        }
        return render(request, "patron/update_pw.html", context)
    else:
        return redirect('/profile/register/')

def login_view(request):
    error_message = None
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Incorrect login credentials.'
    context = {
        'error': error_message,
    }
    return render(request, "patron/login.html", context)

def logout_view(request):
    logout(request)
    return render(request, "patron/logout_success.html", {})

def wishlist_view(request):
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            if 'game_id' in request.POST: # add a game
                game_id = request.POST['game_id']
                game = Game.add_or_grab_game(game_id)
                user.patron.wishlist.add(game)
            elif 'wishlist_id' in request.POST: # remove a game with wishlist_id
                wishlist_id = request.POST['wishlist_id']
                game = user.patron.wishlist.get(game_id=wishlist_id)
                user.patron.wishlist.remove(game)
            elif 'pop_add_game_id' in request.POST: # add a game to wishlist and then go back to popular games screen
                game_id = request.POST['pop_add_game_id']
                game = Game.add_or_grab_game(game_id)
                user.patron.wishlist.add(game)
                return redirect('/game/popular/')
            elif 'pop_remove_wishlist_id' in request.POST: # remove a game from wishlist and then go back to popular games screen
                wishlist_id = request.POST['pop_remove_wishlist_id']
                game = user.patron.wishlist.get(game_id=wishlist_id)
                user.patron.wishlist.remove(game)
                return redirect('/game/popular/')
            elif 'suggest_add_game_id' in request.POST: # add a game to wishlist and then go back to suggested games screen
                game_id = request.POST['suggest_add_game_id']
                game = Game.add_or_grab_game(game_id)
                user.patron.wishlist.add(game)
                return redirect('/game/suggestions/')
            elif 'suggest_remove_wishlist_id' in request.POST: # remove a game from wishlist and then go back to suggested games screen
                wishlist_id = request.POST['suggest_remove_wishlist_id']
                game = user.patron.wishlist.get(game_id=wishlist_id)
                user.patron.wishlist.remove(game)
                return redirect('/game/suggestions/')
        current_wishlist = user.patron.wishlist.all()
        context = {'wishlist':current_wishlist}
        return render(request, 'patron/wishlist.html', context)
    else:
        message = 'Must be signed in to view or add to a wishlist.'
        context = {'error_message':message}
        return render(request, 'error.html', context)

