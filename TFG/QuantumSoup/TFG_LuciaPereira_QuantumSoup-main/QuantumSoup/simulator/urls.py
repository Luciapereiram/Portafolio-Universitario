from django.urls import path
from . import views, services

# Rutas para el uso del simulador

urlpatterns = [
    # Pagina del simulador
    path('', views.simulator, name='simulator'),

    # API de simulacion
    path('api/', services.exec_simulation, name='exec_simulation'),
    path('api/draw/', services.draw_circuit_view, name='draw_circuit'),
]