from django.urls import path
from . import views

# Rutas a las distintas paginas

urlpatterns = [
    # Principal
    path('', views.home, name='home'),

    # Informacion divulgativa
    path('info', views.base, name='info'),

    path("api/articulos/<str:nombre_categoria>/", views.get_categoria_articulos, name="get_categoria_articulos"),
]