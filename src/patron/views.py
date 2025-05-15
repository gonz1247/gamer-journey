#from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from .forms import PatronRegisterForm
from game.models import Game

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
                error_message.append(error) # = error_message + error + ' '
    form = PatronRegisterForm()
    context = {
        'form': form,
        'error': error_message,
    }
    return render(request, "patron/register.html", context)

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
            game_id = request.POST['game_id']
            game = Game.add_or_grab_game(game_id)
            user.patron.wishlist.add(game)
        current_wishlist = user.patron.wishlist.all()
        context = {'wishlist':current_wishlist}
        return render(request, 'patron/wishlist.html', context)
    else:
        message = 'Must be signed in to view or add to a wishlist.'
        context = {'error_message':message}# change this to go to an error page
        return render(request, 'error.html', context)

