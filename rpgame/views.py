from django.shortcuts import render, redirect
from . import login, host
# from django.http import HttpRequest

# Create your views here.

# Page form receives user input
def loginform(request):

    user_login = ''
    user_password = ''

    if request.method == 'GET':
        if request.session.get('user_login'):
            return redirect('mainmenu')
        return render(request, 'index.html', {'user_login': user_login, 'user_password': user_password})

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
def mainmenu(request):
    if request.method == 'GET':
        return render(request, 'mainmenu.html', {'user_name': request.session['user_name'],'user_game_id': request.session['user_game_id']})

# Host new game page
def hostgame(request):
    if request.method == 'GET':
        return render(request, 'hostgame.html', {'user_name': request.session['user_name'],'user_game_id': request.session['user_game_id']})
    
    if request.method == 'POST':
        
        game_details = {'player1': request.session['user_name'], 
                        'player2': request.POST.get('player2'),
                        'player3': request.POST.get('player3'),
                        'player4': request.POST.get('player4'),
                        'num_planets': request.POST.get('num_planets'),
                        'map_width': request.POST.get('map_width'),
                        'map_height': request.POST.get('map_height'),
                        'fogofwar': request.POST.get('fogofwar')}

        host.host_new_game(game_details)

        return redirect('joingame')

# Join a game page
def joingame(request):

    return render(request, 'joingame.html', {'user_name': request.session['user_name'],'user_game_id': request.session['user_game_id']})
    # if request.method == 'GET':
    #     return render(request, 'joingame.html', {'user_name': request.session['user_name'],'user_game_id': request.session['user_game_id']})
    
    # if request.method == 'POST':
    #     user_ = request.POST.get('')
    #     user_ = request.POST.get('')

# Log out function
def clearsession(request):
    # Clear the entire session
    request.session.clear()

    # Optionally, you can also delete specific keys from the session
    # del request.session['your_key']

    return render(request, 'index.html', {})