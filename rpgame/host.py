# Validate login information
from django.db import connections


def host_new_game(game_details):

    user_name = game_details['player1']
    player2 = game_details['player2']
    player3 = game_details['player3']
    player4 = game_details['player4']
    fogofwar = game_details['fogofwar']

    player_list = [user_name, player2, player3, player4]

    #TEST
    print('HERE>>>>>>>>>>> FOG of WAR', fogofwar)
    
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
        # TEST
        print('HERE>>>>>>>>>>>', qstring)
        cursor.execute(qstring)
        return True

# TEST
# print('HERE>>>>>>>>>>>', host_new_game({'player1': 'player1',
#                                         'player2': 'player2',
#                                         'player3': 'player3',
#                                         'player4': 'player4', 
#                                         'num_planets': 30,
#                                         'map_width': 20,
#                                         'map_height': 20,
#                                         'fogofwar': True}))