from django.contrib import admin
from django.urls import path
from report import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dash/', views.index, name="dash"),
    path('api/ventas/', views.ventas_api, name='ventas_api'),
    path('api/ventas/<int:venta_id>/', views.ventas_api, name='ventas_api_detail'),  # Endpoint para operaciones específicas
]
