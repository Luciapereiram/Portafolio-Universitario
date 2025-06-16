from django.shortcuts import render
from django.http import JsonResponse
from .models import Categoria

# Definicion de las distintas vistas

def home(request):
    return render(request, 'home.html')

def base(request):
    return render(request, 'info.html')

def get_categoria_articulos(request, nombre_categoria):
    try:
        categoria = Categoria.objects.get(nombre=nombre_categoria)
        articulos = categoria.articulos.all()
        
        # Separamos los artículos según su tipo
        history_articles = []
        concept_articles = []
        resource_articles = {
            'libros': [],
            'canales': [],
            'webs': []
        }

        for art in articulos:
            if art.tipo == 'hist':
                history_articles.append({"titulo": art.titulo, "contenido": art.contenido})
            elif art.tipo == 'concept':
                concept_articles.append({"titulo": art.titulo, "contenido": art.contenido})
            elif art.tipo == 'libro':
                resource_articles['libros'].append({"titulo": art.titulo, "contenido": art.contenido, "url": art.url})
            elif art.tipo == 'canal':
                resource_articles['canales'].append({"titulo": art.titulo, "contenido": art.contenido, "url": art.url})
            elif art.tipo == 'web':
                resource_articles['webs'].append({"titulo": art.titulo, "contenido": art.contenido, "url": art.url})

        # Preparar los datos
        data = {
            "categoria": categoria.nombre,
            "history": history_articles,
            "concepts": concept_articles,
            "resources": resource_articles
        }
        
        return JsonResponse(data)
    
    except Categoria.DoesNotExist:
        return JsonResponse({"error": "Categoría no encontrada"}, status=404)