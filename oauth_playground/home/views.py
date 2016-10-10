from django.shortcuts import render


def index(request):
    cont = {'frequencies': False, 'calls': False}
    return render(request, 'home/index.html', cont)
