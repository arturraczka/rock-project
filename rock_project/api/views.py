from django.shortcuts import render


def lobby(request):
    return render(request, 'api/lobby.html')
