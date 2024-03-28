from django.shortcuts import render, redirect
from . import login, play

# Create your views here.

# Login form
def login_form(request):

    if request.method == 'GET':
        if request.session.get('user_login'):
            return redirect('mainmenu')
        return render(request, 'index.html', {})

    if request.method == 'POST':
        # Process form data here
        user_login = request.POST.get('user_login')
        user_password = request.POST.get('user_password')

        if user_login == "" or user_password == "":
            return render(request, 'index.html', {'form_not_valid':'You must enter a login and password.'})

        login_details = {'user_login': user_login, 'user_password': user_password}

        if login.is_valid_login(login_details):
            request.session['user_name'] = login_details['user_login']
            request.session['user_game_id'] = 0
            return redirect('mainmenu')
        return render(request, 'index.html', {'form_not_valid':'Invalid Login Credentials. Please try again.'})

# Menu page
def main_menu(request):
    user_name = request.session['user_name']
    request.session['user_game_id'] = play.get_last_game(request.session['user_name'])
    game_list = play.get_game_list(user_name)
    return render(request, 'mainmenu.html', {'user_name': request.session['user_name'],'user_game_id': request.session['user_game_id'], 'game_list': game_list})


# Play a game
def play_game(request):

    if request.method == 'GET':
        return redirect('joingame')
        

    if request.method == 'POST':
        game_details = {'user_name': request.session['user_name'], 
                        'join_game_id': request.POST.get('joingameid')}

        play.play_game(game_details)

        return render(request, 'playgame.html',  {'user_name': request.session['user_name'],'user_game_id': request.session['user_game_id']})


# Host new game form
def host_game(request):
    if request.method == 'POST':
        game_details = {'player1': request.session['user_name'], 
                        'player2': request.POST.get('player2'),
                        'player3': request.POST.get('player3'),
                        'player4': request.POST.get('player4'),
                        'num_planets': request.POST.get('num_planets'),
                        'map_width': request.POST.get('map_width'),
                        'map_height': request.POST.get('map_height'),
                        'fogofwar': request.POST.get('fogofwar')}
        play.host_new_game(game_details)
        request.session['user_game_id'] = play.get_last_game(request.session['user_name'])
        return render(request, 'playgame.html', {'user_name': request.session['user_name'],'user_game_id': request.session['user_game_id']})


# Log out function
def clear_session(request):
    # Clear the entire session
    request.session.clear()

    # Optionally, you can also delete specific keys from the session
    # del request.session['your_key']
    return redirect('loginform')
    # return render(request, 'index.html', {})