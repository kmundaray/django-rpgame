# Validate login information
from django.db import connections
from django.core.serializers import serialize
from django.http import JsonResponse
from json import loads, dumps

def play_game(game_details):

    user_name = game_details['user_name']
    join_game_id = game_details['join_game_id']

    with connections['default'].cursor() as cursor:
        qstring = f"SELECT 1;"
        cursor.execute(qstring)
        return True

def get_game_list(user_name):
    with connections['default'].cursor() as cursor:
        qstring = f"SELECT gameid,commandsdone FROM PlayerGame WHERE PlayerName = '{user_name}';"
        cursor.execute(qstring)
        results = cursor.fetchall()
        # Fetch all rows from the result set
        game_list = []
        if len(results) == 0:
            game_list = [{'game_id':'N/A','turn_completed':'N/A'}]
            return game_list
        for row in results:
            game_id = row[0]
            turn_completed = row[1]
            if turn_completed is None:
                turn_completed = "-"
            game_list.append({'game_id':game_id,'turn_completed':turn_completed})
        sorted_game_list = sorted(game_list, key=lambda x: x['game_id'])
        return sorted_game_list


def host_new_game(game_details):

    user_name = game_details['player1']
    player2 = game_details['player2']
    player3 = game_details['player3']
    player4 = game_details['player4']
    fogofwar = game_details['fogofwar']

    player_list = [user_name, player2, player3, player4]

    if fogofwar:
        fogofwar = 1
    else:
        fogofwar = 0

    for player in player_list:
        if player == '':
            player_list.remove(player)

    num_planets = game_details['num_planets']
    map_width = game_details['map_width']
    map_height = game_details['map_height']
    
    with connections['default'].cursor() as cursor:
        qstring = f"Call InitializeGame(array{player_list}, {num_planets}, {map_width}, {map_height});"
        cursor.execute(qstring)
        return get_last_game(user_name)

def get_last_game(user_name):
    with connections['default'].cursor() as cursor:
        qstring = f"SELECT gameid FROM PlayerGame WHERE PlayerName = '{user_name}' ORDER BY gameid DESC LIMIT 1;"
        cursor.execute(qstring)
        result = cursor.fetchall()
        if result is None:
            return None
        for row in result:
            return row[0]