# Validate login information
from django.db import connections

def is_valid_login(login_details):
    # Check if login details are valid
    # login_details = {'user_login': user_login, 'user_password': user_password}
    with connections['default'].cursor() as cursor:
        qstring = f"Select LoginPlayer('{login_details['user_login']}', '{login_details['user_password']}');"
        cursor.execute(qstring)
    # loginPlayerResult contains a tuple with true or false flags. 
    # One for successful login and another to identify if a new user was created.
        loginPlayerResult = cursor.fetchall()
    if loginPlayerResult[0][0][0] == 't':
        if loginPlayerResult[0][0][1] == 't':
            # PLACEHOLDER
            print('HERE>>>>>>>>>>>', 'New user created')
        return True
    return False