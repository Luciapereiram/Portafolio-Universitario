from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=60)

    def __str__(self):
        return self.nombre


class Articulo(models.Model):
    # Tipos de contenido posibles
    TIPO_CONTENIDO = [
        ('hist', 'Texto Histórico'),
        ('concept', 'Texto Conceptual'),
        ('libro', 'Libro'),
        ('canal', 'Canal de Youtube'),
        ('web', 'Página Web')
    ]
    
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="articulos")
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    tipo = models.CharField(max_length=10, choices=TIPO_CONTENIDO)
    url = models.URLField(blank=True, null=True)  # Solo para libros, canales de youtube y páginas web

    def __str__(self):
        return self.titulo
