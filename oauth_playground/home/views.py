from django.shortcuts import render
from oauth_playground.configs import Configs


def index(request):
    cont = {'callback_url': Configs.get_callback_url()}
    return render(request, 'home/index.html', cont)
