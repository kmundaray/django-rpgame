# Validate login information
from django.db import connections


# Display game page
def play_game(game_details):

    user_name = game_details['user_name']
    join_game_id = game_details['user_game_id']
    map_display_str = ""
    game_display_stats = []
    turn = 0

    with connections['default'].cursor() as cursor:
        qstring = f"SELECT ShowMap('{user_name}', {join_game_id});"
        cursor.execute(qstring)
        qresult = cursor.fetchall()
        for row in qresult:
            map_display_str += str(row[0]) + "\n"

        qstring = f"SELECT Turn FROM Game WHERE GameId = {join_game_id} LIMIT 1;"
        cursor.execute(qstring)
        qresult = cursor.fetchall()
        for row in qresult:
            turn = row[0]

        qstring = f"SELECT ShowPlanetList('{user_name}', {join_game_id});"
        cursor.execute(qstring)
        qresult = cursor.fetchall()
        if qresult[0][0] is not None:
            for row in qresult[0][0]:
                display_character = row['displaycharacter']
                owner_done = row['ownerdone']
                ships = row['ships']
                allocated_ships = row['allocatedships']
                production = row['production']
                defense = row['defense']
                if owner_done is None:
                    owner_done = "-"
                game_display_stats.append({'display_character':display_character
                                            ,'owner_done':owner_done
                                            ,'ships': ships
                                            ,'allocated_ships': allocated_ships
                                            ,'production': production
                                            ,'defense': defense
                                            })
        else:
            game_display_stats.append({'display_character':'-'
                                    ,'owner_done':'-'
                                    ,'ships': '-'
                                    ,'allocated_ships': '-'
                                    ,'production': '-'
                                    ,'defense': '-'
                                    })
        
        battle_log = ''
        qstring = f"SELECT battles('{join_game_id}','{user_name}');"
        cursor.execute(qstring)
        result = cursor.fetchall()
        for row in result:
            battle_log += str(row[0]) + "\n"
        if len(battle_log) < 1:
            battle_log = "No logs available for this game."

    sorted_game_display_stats = sorted(game_display_stats, key=lambda x: x['display_character'])
    game_details['user_name'] = user_name
    game_details['user_game_id'] = join_game_id
    game_details['map_display_str'] = map_display_str 
    game_details['game_display_stats'] = sorted_game_display_stats
    game_details['game_turn'] = turn
    game_details['battle_log'] = battle_log
    return game_details


# Get available games
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

# Host a new game
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


# Get last game ID
def get_last_game(user_name):
    with connections['default'].cursor() as cursor:
        qstring = f"SELECT gameid FROM PlayerGame WHERE PlayerName = '{user_name}' ORDER BY gameid DESC LIMIT 1;"
        cursor.execute(qstring)
        result = cursor.fetchall()
        if result is None:
            return None
        for row in result:
            return row[0]


# Send fleets
def add_command(command_details):
    user_name = command_details['user_name']
    user_game_id = command_details['user_game_id']
    source_planet = command_details['source_planet']
    destination_planet = command_details['destination_planet']
    fleet_size = command_details['fleet_size']

    with connections['default'].cursor() as cursor:
        qstring = f"Select AddCommand('{user_name}','{source_planet}','{destination_planet}','{fleet_size}','{user_game_id}');"
        cursor.execute(qstring)
        return True


# Finish turn
def commands_done(command_details):
    user_name = command_details['user_name']
    user_game_id = command_details['user_game_id']

    with connections['default'].cursor() as cursor:
        qstring = f"Select CommandsDone('{user_name}','{user_game_id}');"
        cursor.execute(qstring)
        return True
