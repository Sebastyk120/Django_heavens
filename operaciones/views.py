from django.shortcuts import render


def home_operaciones(request):
    return render(request, 'home_operaciones.html')
