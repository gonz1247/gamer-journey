from django.shortcuts import render, redirect, get_object_or_404

from .forms import DiaryEntryForm
from game.models import Game
from .models import DiaryEntry

# Create your views here.
def diary_entry_view(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST' and 'game' in request.POST:
            # add game to diary
            form = DiaryEntryForm(request.POST)
            # add in choice fields again since this is generated dynamically when first loading the diary add page
            game = Game.add_or_grab_game(request.POST['game']) # potential security concern since they can change the game they are adding midway (by changing HTML), but then it just adds a different game so not a big deal
            [game_info] = Game.game_id_search(game.game_id, fields='platforms.*')
            platforms = {p: p for p in game_info['platforms']}
            form.fields['platform'].choices = platforms
            if form.is_valid():
                form.save()
                # check to see if need to remove game from wishlist
                if game in user.patron.wishlist.all():
                    #remove game from wishlist
                    user.patron.wishlist.remove(game)
                return redirect('/diary/')
            else:
                error_message = []
                for [error] in form.errors.values():
                    error_message.append(error)
                context = {'error_message':error_message}
                return render(request, 'error.html', context)
        elif request.method == 'POST' and 'game_id' in request.POST:
            # grab game info to display on the diary entry page
            game_id = request.POST['game_id']
            [game_info] = Game.game_id_search(game_id, fields='name,cover.*,platforms.*')
            # look up what platforms the game is available on and add options to form
            platforms = {p:p for p in game_info['platforms']}
            form = DiaryEntryForm(initial={'game':game_id, 'patron':user.patron.pk})
            form.fields['platform'].choices = platforms
            if user.patron.fav_platform in platforms:
                form.initial['platform'] = user.patron.fav_platform
            context = {
                'form':form,
                'game':game_info,
            }
            return render(request, 'diary/diary_entry.html', context)
        else:
            return redirect('search_general')
    else:
        message = 'Must be signed in to add entries to your diary.'
        context = {'error_message':message}
        return render(request, 'error.html', context)

def my_diary_view(request):
    user = request.user
    if user.is_authenticated:
        current_diary = user.patron.diaryentry_set.all()
        if current_diary:
            # Get game info for each entry
            game_info = Game.game_id_search(current_diary.values_list('game_id',flat=True),fields='name,cover.*')
            # Convert entry and game info to dictionary so that game_info can be matched up with entry (API returns info in order of game_id, not order or request list)
            current_diary_sorted = list()
            for info in game_info:
                # find all instances of this game in the diary
                entries = current_diary.filter(game_id=info['game_id'])
                for entry in entries:
                    current_diary_sorted.append(entry.__dict__ | info)
            # sort by completion date
            current_diary_sorted = sorted(current_diary_sorted, key=lambda entry: (entry['completed_date'], entry['entry_datetime']))
        else:
            current_diary_sorted = current_diary
        context = {'diary': current_diary_sorted}
        return render(request, 'diary/my_diary.html', context)
    else:
        message = 'Must be signed in to view diary.'
        context = {'error_message': message}
        return render(request, 'error.html', context)

def diary_edit_view(request, entry_id):
    user = request.user
    if user.is_authenticated:
        try:
            # grab diary entry
            entry = user.patron.diaryentry_set.get(pk=entry_id)
            [game_info] = Game.game_id_search(entry.game.game_id, fields='name,cover.*,platforms.*')
        except DiaryEntry.DoesNotExist:
            message = "Cannot edit another patron's diary entry."
            context = {'error_message': message}
            return render(request, 'error.html', context)
        if 'entry_id' in request.POST or request.method == 'GET': # user to manually type out URL if they really want
            form = DiaryEntryForm(instance=entry)
            # update platform choices that were done dynamically the first time
            platforms = {p: p for p in game_info['platforms']}
            form.fields['platform'].choices = platforms
            # Add in intial data for fields that had their data structure type changed in cleaning
            form.initial['platform'] = entry.platform
            form.initial['game'] = entry.game.game_id
            context = {
                'form':form,
                'game':game_info,
            }
            return render(request, 'diary/diary_entry.html', context)
        elif request.method == 'POST': # entry has been updated if post, if get then just manually trying to come to page
            form = DiaryEntryForm(request.POST, instance=entry)
            # update platform choices that were done dynamically the first time
            platforms = {p: p for p in game_info['platforms']}
            form.fields['platform'].choices = platforms
            if form.is_valid():
                form.save()
                # maybe need to add in some logic for if a form isn't valid, but not updating is an okay default
        return redirect('diary')
    else:
        message = 'Must be signed in to add entries to your diary.'
        context = {'error_message':message}
        return render(request, 'error.html', context)

def diary_delete_view(request, entry_id):
    user = request.user
    if user.is_authenticated:
        try:
            # grab diary entry
            entry = user.patron.diaryentry_set.get(pk=entry_id)
            [game_info] = Game.game_id_search(entry.game.game_id, fields='name,cover.*')
        except DiaryEntry.DoesNotExist:
            message = "Cannot delete another patron's diary entry."
            context = {'error_message': message}
            return render(request, 'error.html', context)
        if 'confirmation' in request.POST:
            if request.POST['confirmation'] == 'yes':
                entry.delete()
            return redirect('diary')
        else:
            context = {
                'game':game_info,
            }
            return render(request, 'diary/delete_confirmation.html', context)

def diary_detailed_view(request, entry_id):
    # grab diary entry, don't really care if it's that users or not
    entry = get_object_or_404(DiaryEntry.objects.all(),pk=entry_id)
    [game_info] = Game.game_id_search(entry.game.game_id, fields='name,cover.*')
    context = {
        'entry':entry,
        'game':game_info,
    }
    return render(request, 'diary/view_detailed.html', context)

def game_reviews_view(request, game_id):
    try:
        # grab all diary entries associated with this game
        game = Game.objects.get(game_id=game_id)
        entries = game.diaryentry_set.all()
        assert len(entries)>0
        # Get game info
        [game_info] = game.self_search(fields='name,cover.*')
        # Generate review stats
        total = 0
        n_reviews = 0
        for entry in entries:
            if entry.rating >= 0:
                total += entry.rating
                n_reviews += 1
        review_stats = dict()
        if n_reviews > 0: review_stats['ave_rating'] = total / (n_reviews)
        # Can add more stats later if I want
        context = {
            'entries': entries,
            'game':game_info,
            'review_stats':review_stats,
        }
        return render(request, 'diary/view_all_reviews.html', context)
    except Game.DoesNotExist:
        pass # to the error message
    except AssertionError:
        pass # to the error message
    message = 'No reviews for this game yet.'
    context = {'error_message': message}
    return render(request, 'error.html', context)

