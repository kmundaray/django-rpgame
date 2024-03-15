# rpgame/urls.py
from django.urls import path
from .views import loginform, mainmenu, clearsession, joingame, hostgame

urlpatterns = [
    path('index.html', loginform, name='loginform'),
    path('mainmenu.html', mainmenu, name='mainmenu'),
    path('clearsession/', clearsession, name='clearsession'),
    path('joingame.html', joingame, name='joingame'),
    path('hostgame.html', hostgame, name='hostgame'),
]