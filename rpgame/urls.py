# rpgame/urls.py
from django.urls import path
from .views import loginform, mainmenu, clearsession, joingame

urlpatterns = [
    path('', loginform, name='loginform'),
    path('mainmenu.html', mainmenu, name='mainmenu'),
    path('clearsession/', clearsession, name='clearsession'),
    path('joingame.html', joingame, name='joingame'),
    path('hostgame.html', joingame, name='hostgame'),
]