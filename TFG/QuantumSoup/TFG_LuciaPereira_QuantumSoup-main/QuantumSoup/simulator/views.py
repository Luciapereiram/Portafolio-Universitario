from django.shortcuts import render

# Definicion de vista del simulador

def simulator(request):
    return render(request, 'simulator.html')