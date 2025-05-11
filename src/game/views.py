from django.shortcuts import render
import requests
from dotenv import dotenv_values

CONFIG_ENV = dotenv_values('.env')
AUTHENTICATOR_URL = 'https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type=client_credentials'

API_URL = 'https://api.igdb.com/v4/games'

# Create your views here.
def add_game_view(request):
    if request.method == 'POST':
        r_1 = requests.post(
            AUTHENTICATOR_URL.format(CONFIG_ENV['client_id'], CONFIG_ENV['client_secret'])).json()
        print(r_1)
        r_2 = requests.post(API_URL, headers={
                                        'Client-ID':CONFIG_ENV['client_id'],
                                        'Authorization':('Bearer ' + r_1['access_token']),}).json()
                                        #'Body': '"fields name; limit 5"'}).json()
        print(r_2)

    context = {}
    return render(request,'new_game.html',context)

