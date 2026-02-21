from django.db.models.query import QuerySet
from django.db import models, IntegrityError
import os, requests

IGDB_CLIENT_ID = os.environ.get("IGDB_CLIENT_ID")
IGDB_CLIENT_SECRET = os.environ.get("IGDB_CLIENT_SECRET")
AUTHENTICATOR_URL = "https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type=client_credentials"
GAMES_END_POINT = "https://api.igdb.com/v4/games"
POPULAR_END_POINT = "https://api.igdb.com/v4/popularity_primitives"


# Create your models here.
class Game(models.Model):
    game_id = models.IntegerField(primary_key=True)

    def self_search(self, fields="name,cover.*,url,genres.*,themes.*,platforms.*"):
        return self.game_id_search(self.game_id, fields)

    # Static methods for using the API
    @staticmethod
    def _get_access_token():
        access_token = requests.post(
            AUTHENTICATOR_URL.format(IGDB_CLIENT_ID, IGDB_CLIENT_SECRET)
        ).json()["access_token"]
        return access_token

    @staticmethod
    def title_search(title, fields="name,cover.*,url", limit=10):
        # get access token and set up header for request
        access_token = Game._get_access_token()
        auth = {
            "Client-ID": IGDB_CLIENT_ID,
            "Authorization": ("Bearer " + access_token),
        }
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
    def game_id_search(game_id, fields="name,cover.*,url"):
        # get access token and set up header for request
        access_token = Game._get_access_token()
        auth = {
            "Client-ID": IGDB_CLIENT_ID,
            "Authorization": ("Bearer " + access_token),
        }
        # set up query for batch or single game search
        query = f"fields {fields}; where id="
        if (
            isinstance(game_id, list)
            or isinstance(game_id, set)
            or isinstance(game_id, QuerySet)
        ):
            batch = list()
            for game in game_id:
                batch.append(str(game))
            query = query + "(" + ",".join(batch) + ");"
        else:
            query += f"{game_id};"
        # Search for inputted title
        results = requests.post(GAMES_END_POINT, headers=auth, data=query).json()
        # Format results that came back
        game_info = Game._format_search(results)
        return game_info

    @staticmethod
    def _format_search(query_results):
        # Extract relevant info from query
        extract_fields = {
            "cover": "url",
            "genres": "name",
            "themes": "name",
            "platforms": "name",
            "similar_games": "id",
        }
        for game in query_results:
            for key, value in extract_fields.items():
                if game.get(key):
                    if isinstance(game.get(key), list):
                        all_instances = []
                        for instance in game[key]:
                            all_instances.append(instance[value])
                        game[key] = all_instances
                    else:  # it is a dict
                        game[key] = game[key][value]
        # rename query dictionary to align with kwargs of the model
        rename_fields = {"id": "game_id", "name": "title", "cover": "cover_art"}
        for game in query_results:
            for old_key, new_key in rename_fields.items():
                if game.get(old_key):
                    game[new_key] = game.pop(old_key)
        # Send query results back in expected format
        return query_results

    @staticmethod
    def add_or_grab_game(game_id_list):
        if not isinstance(game_id_list, list):
            game_id_list = [game_id_list]
        batch_games = list()
        for game_id in game_id_list:
            try:  # create game if not in DB
                game = Game.objects.create(game_id=game_id)
            except IntegrityError:  # grab instance of game instead
                game = Game.objects.get(game_id=game_id)
            batch_games.append(game)
        if len(batch_games) == 1:
            # backwards compatibility for when this was set up as single game search only
            batch_games = batch_games[0]
        return batch_games

    @staticmethod
    def general_igdb_search(endpoint=GAMES_END_POINT, query="fields *;"):
        # get access token and set up header for request
        access_token = Game._get_access_token()
        auth = {
            "Client-ID": IGDB_CLIENT_ID,
            "Authorization": ("Bearer " + access_token),
        }
        # Search for inputted title
        results = requests.post(endpoint, headers=auth, data=query).json()
        # return results as they come from the API
        return results

    @staticmethod
    def popular_search(pop_type=2, fields="game_id", limit=10):
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
        auth = {
            "Client-ID": IGDB_CLIENT_ID,
            "Authorization": ("Bearer " + access_token),
        }
        # Search popular games based on inputs
        query = f"fields {fields}; sort value desc; limit {limit}; where popularity_type = {pop_type};"
        results = requests.post(POPULAR_END_POINT, headers=auth, data=query).json()
        return results
