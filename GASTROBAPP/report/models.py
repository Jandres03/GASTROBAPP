from django.db import models

class ConexionDB(models.Model):
    name = models.CharField(max_length=100, unique=True)
    host = models.CharField(max_length=100)
    port = models.IntegerField()
    name_db = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Venta(models.Model):
    fecha = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    producto = models.CharField(max_length=100)

    def __str__(self):
        return f"Venta del {self.fecha} - Valor: {self.valor}"