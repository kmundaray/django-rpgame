# rpgame/urls.py
from django.urls import path
from .views import login_form, main_menu, clear_session, play_game, host_game

urlpatterns = [
    path('', login_form),
    path('index.html', login_form, name='loginform'),
    path('mainmenu.html', main_menu, name='mainmenu'),
    path('clear_session/', clear_session, name='clearsession'),
    path('host_game/', host_game, name='hostgame'),
    path('playgame.html', play_game, name='playgame' ),
]