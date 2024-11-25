from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from report import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dash/', views.index, name="dash"),
    path('api/ventas/', views.ventas_api, name='ventas_api'),
    path('api/ventas/<int:venta_id>/', views.ventas_api, name='ventas_api_detail'),
    path('api/ventas/<int:venta_id>/', views.ventas_api, name='ventas_api_detail'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='report/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), 
]

