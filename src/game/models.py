from charset_normalizer.cli import query_yes_no
from django.db import models
import django.db
from dotenv import dotenv_values
import requests

CONFIG_ENV = dotenv_values('.env')
AUTHENTICATOR_URL = 'https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type=client_credentials'
GAMES_END_POINT = 'https://api.igdb.com/v4/games'
POPULAR_END_POINT = 'https://api.igdb.com/v4/popularity_primitives'

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

    def self_search(self,fields='name,cover.*,url,genres.*,themes.*,platforms.*'):
        return self.game_id_search(self.game_id,fields)

    # Static methods for using the API
    @staticmethod
    def _get_access_token():
        access_token = requests.post(
            AUTHENTICATOR_URL.format(CONFIG_ENV['client_id'], CONFIG_ENV['client_secret'])).json()['access_token']
        return access_token

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

    @staticmethod
    def game_id_search(game_id, fields='name,cover.*,url'):
        # get access token and set up header for request
        access_token = Game._get_access_token()
        auth = {'Client-ID': CONFIG_ENV['client_id'],
                'Authorization': ('Bearer ' + access_token)}
        # set up query for batch or single game search
        query = f'fields {fields}; where id='
        if isinstance(game_id,list) or isinstance(game_id,set):
            batch=list()
            for game in game_id:
                batch.append(str(game))
            query = query + '(' + ','.join(batch) + ');'
        else:
            query += f'{game_id};'
        # Search for inputted title
        results = requests.post(GAMES_END_POINT, headers=auth, data=query).json()
        # Format results that came back
        game_info = Game._format_search(results)
        return game_info

    @staticmethod
    def _format_search(query_results):
        # Extract relevant info from query
        extract_fields = {'cover':'url','genres':'name','themes':'name','platforms':'name'}
        for game in query_results:
            for key, value in extract_fields.items():
                if game.get(key):
                    if isinstance(game.get(key),list):
                        all_instances = []
                        for instance in game[key]:
                            all_instances.append(instance[value])
                        game[key] = all_instances
                    else: #it is a dict
                         game[key] = game[key][value]
        # rename query dictionary to align with kwargs of the model
        rename_fields = {'id': 'game_id', 'name': 'title', 'cover': 'cover_art'}
        for game in query_results:
            for old_key, new_key in rename_fields.items():
                if game.get(old_key):
                    game[new_key] = game.pop(old_key)
        # Send query results back in expected format
        return query_results

    @staticmethod
    def add_or_grab_game(game_id):
        batch_games = list()
        batch_info = Game.game_id_search(game_id)
        for game_info in batch_info:
            try: # create game if not in DB
                # temp add in
                game = Game.objects.create(**game_info)
                [game_info] = game.self_search()
                for genre_type in game_info['genres']:
                    try:
                        genre = Genre.objects.create(type=genre_type)
                    except django.db.IntegrityError: # grab instance of genre instead
                        genre = Genre.objects.get(type=genre_type)
                    game.genres.add(genre)
                for theme_type in game_info['themes']:
                    try:
                        theme = Theme.objects.create(type=theme_type)
                    except django.db.IntegrityError: # grab instance of genre instead
                        theme = Theme.objects.get(type=theme_type)
                    game.themes.add(theme)
                for platform_device in game_info['platforms']:
                    try:
                        platform = Platform.objects.create(device=platform_device)
                    except django.db.IntegrityError: # grab instance of genre instead
                        platform = Platform.objects.get(device=platform_device)
                    game.platforms.add(platform)
                game.save()
                # alternatively could grab list of all game_id, genres, and themes but not sure if using try/except is just faster than searching through N instances
            except django.db.IntegrityError: # grab instance of game instead
                game = Game.objects.get(game_id=game_info['game_id'])
            batch_games.append(game)
        if len(batch_games) == 1: batch_games = batch_games[0] # backwards compatibility for when this was set up as single game search only
        return batch_games

    @staticmethod
    def general_igdb_search(endpoint=GAMES_END_POINT, query='fields *;'):
        # get access token and set up header for request
        access_token = Game._get_access_token()
        auth = {'Client-ID': CONFIG_ENV['client_id'],
                'Authorization': ('Bearer ' + access_token)}
        # Search for inputted title
        results = requests.post(endpoint, headers=auth, data=query).json()
        # return results as they come from the API
        return results

    @staticmethod
    def popular_search(pop_type=2, fields='game_id', limit=10):
        # pop_type = 1: Based on IGDB visits
        # pop_type = 2: Based on IGDB want to play
        # pop_type = 3: Based on IGDB playing
        # pop_type = 4: Based on IGDB played
        # pop_type = 5: Based on Steam 24hr peak
        # pop_type = 6: Based on Steam positive reviews
        # pop_type = 7: Based on Steam negative reviews (popular for the wrong reason)
        # pop_type = 8: Based on Steam total reviews

        # get access token and set up header for request
        access_token = Game._get_access_token()
        auth = {'Client-ID': CONFIG_ENV['client_id'],
                'Authorization': ('Bearer ' + access_token)}
        # Search popular games based on inputs
        query = f'fields {fields}; sort value desc; limit {limit}; where popularity_type = {pop_type};'
        results = requests.post(POPULAR_END_POINT, headers=auth, data=query).json()
        return results









