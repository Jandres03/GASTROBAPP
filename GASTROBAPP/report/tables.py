import django_tables2 as tables
from .models import Venta

class VentaTable(tables.Table):
    class Meta:
        model = Venta
        template_name = "django_tables2/bootstrap.html"
        fields = ("fecha", "valor", "producto")