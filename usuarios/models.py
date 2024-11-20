from django.db import models


class Usuario(models.Model):
    nombre = models.CharField(max_length= 300)
    apellido = models.CharField(max_length= 300)
    dni = models.CharField(max_length=8, unique=True)
    fecha_creacion = models.DateTimeField(auto_created=True)
    
    