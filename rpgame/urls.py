# rpgame/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', login_form),
    path('index.html', login_form, name='loginform'),
    path('mainmenu.html', main_menu, name='mainmenu'),
    path('host_game/', host_game, name='hostgame'),
    path('playgame.html', play_game, name='playgame' ),
    path('clear_session/', clear_session, name='clearsession'),
    path('send_ships/', send_ships, name='sendships'),
    path('finish_turn/', finish_turn, name='finishturn'),
]