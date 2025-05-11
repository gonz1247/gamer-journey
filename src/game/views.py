from django.shortcuts import render
import requests
from dotenv import dotenv_values
import json

CONFIG_ENV = dotenv_values('.env')
AUTHENTICATOR_URL = 'https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type=client_credentials'

API_URL = 'https://api.igdb.com/v4/games'

# Create your views here.
def search_view(request):
    context = {}
    if request.method == 'POST': # Search has been initiated
        # extract info from POST
        title = request.POST['title']
        # Set up credentials for using the API
        access_token = requests.post(
            AUTHENTICATOR_URL.format(CONFIG_ENV['client_id'], CONFIG_ENV['client_secret'])).json()['access_token']
        auth = {'Client-ID':CONFIG_ENV['client_id'],
                   'Authorization':('Bearer ' + access_token) }
        # Search for inputted title
        query = f'fields name,cover.*,url; search "{title}"; where version_parent = null; limit 15;'
        results = requests.post(API_URL, headers=auth,data=query).json()
        if len(results) > 0:
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

