from charset_normalizer.cli import query_yes_no
from django.db import models
from dotenv import dotenv_values
import requests

CONFIG_ENV = dotenv_values('.env')
AUTHENTICATOR_URL = 'https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type=client_credentials'
GAMES_END_POINT = 'https://api.igdb.com/v4/games'

# Create your models here.

class Genre(models.Model):
    type = models.CharField(max_length=25, unique=True)

class Theme(models.Model):
    type = models.CharField(max_length=25, unique=True)

class Platform(models.Model):
    device = models.CharField(max_length=25, unique=True)


class Game(models.Model):
    game_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    cover_art = models.CharField(max_length=100, blank=True)
    genres = models.ManyToManyField(Genre)
    themes = models.ManyToManyField(Theme)
    platforms = models.ManyToManyField(Platform)

    @staticmethod
    def title_search(title, fields='name,cover.*,url', limit=10):
        # get access token and set up header for request
        access_token = Game._get_access_token()
        auth = {'Client-ID': CONFIG_ENV['client_id'],
                'Authorization': ('Bearer ' + access_token)}
        # Search for inputted title
        query = f'fields {fields}; search "{title}"; where version_parent = null; limit {limit};'
        results = requests.post(GAMES_END_POINT, headers=auth, data=query).json()
        # check if results came back
        if len(results) > 0:
            return Game._format_search(results)
        else:
            # Explicitly send back None
            return None

    def self_search(self,fields='name,cover.*,url,genres.*,themes.*,platforms.*'):
        return self.game_id_search(self.game_id,fields)

    @staticmethod
    def game_id_search(game_id, fields='name,cover.*,url'):
        # get access token and set up header for request
        access_token = Game._get_access_token()
        auth = {'Client-ID': CONFIG_ENV['client_id'],
                'Authorization': ('Bearer ' + access_token)}
        # Search for inputted title
        query = f'fields {fields}; where id={game_id};'
        results = requests.post(GAMES_END_POINT, headers=auth, data=query).json()
        # check if results came back
        assert len(results) == 1, 'Invalid game_id'
        game_info = Game._format_search(results)
        return game_info[0]

    @staticmethod
    def _get_access_token():
        access_token = requests.post(
            AUTHENTICATOR_URL.format(CONFIG_ENV['client_id'], CONFIG_ENV['client_secret'])).json()['access_token']
        return access_token

    @staticmethod
    def _format_search(query_results):
        reformat_fields = {'cover':'url','genres':'name','themes':'name','platforms':'name'}
        for game in query_results:
            for key, value in reformat_fields.items():
                if game.get(key):
                    if isinstance(game.get(key),list):
                        all_instances = []
                        for instance in game[key]:
                            all_instances.append(instance[value])
                        game[key] = all_instances
                    else: #it is a dict
                         game[key] = game[key][value]

        query_results = Game._rename_fields(query_results)

        return query_results

    @staticmethod
    def _rename_fields(query_results):
        rename_fields = {'id': 'game_id', 'name': 'title', 'cover': 'cover_art'}
        for game in query_results:
            for old_key, new_key in rename_fields.items():
                if game.get(old_key):
                    game[new_key] = game.pop(old_key)
        return query_results







