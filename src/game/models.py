from django.db import models
from dotenv import dotenv_values
import requests

CONFIG_ENV = dotenv_values('.env')
AUTHENTICATOR_URL = 'https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type=client_credentials'
GAMES_END_POINT = 'https://api.igdb.com/v4/games'

# Create your models here.
class Game(models.Model):
    game_id = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    cover_art = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    themes = models.CharField(max_length=100)

    @staticmethod
    def game_search(title, fields='name,cover.*,url', limit=10):
        # get access token and set up header for request
        access_token = Game._get_access_token()
        auth = {'Client-ID': CONFIG_ENV['client_id'],
                'Authorization': ('Bearer ' + access_token)}
        # Search for inputted title
        query = f'fields {fields}; search "{title}"; where version_parent = null; limit {limit};'
        results = requests.post(GAMES_END_POINT, headers=auth, data=query).json()
        # check if results came back
        if len(results) > 0:
            return results
        else:
            # Explicitly send back None
            return None

    @staticmethod
    def _get_access_token():
        access_token = requests.post(
            AUTHENTICATOR_URL.format(CONFIG_ENV['client_id'], CONFIG_ENV['client_secret'])).json()['access_token']
        return access_token



