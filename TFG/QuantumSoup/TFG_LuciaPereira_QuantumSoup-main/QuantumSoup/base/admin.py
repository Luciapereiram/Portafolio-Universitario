from django.contrib import admin
from .models import Categoria, Articulo

# Register your models here.
admin.site.register(Categoria)

# Registro de los artículos
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'tipo', 'contenido')
    search_fields = ('titulo', 'contenido')
    list_filter = ('categoria', 'tipo')

admin.site.register(Articulo, ArticuloAdmin)