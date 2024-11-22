from django.shortcuts import render
import pandas as pd
import plotly.express as px
from .models import Venta
from django.views.generic import ListView
from .tables import VentaTable
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def index(request):
    sells = Venta.objects.all().order_by('fecha') 
    df = pd.DataFrame(list(sells.values("fecha", "valor")))

    fig =  px.line(df, x="fecha", y="valor", markers=True)
    plot_div = fig.to_html(full_html=False)
    

    ventas = Venta.objects.all()
    df = pd.DataFrame(list(ventas.values("producto")))

    productos_mas_vendidos = df['producto'].value_counts()


    df_productos_mas_vendidos = pd.DataFrame(productos_mas_vendidos).reset_index()
    df_productos_mas_vendidos.columns = ['Producto', 'Ventas']


    df_productos_mas_vendidos = df_productos_mas_vendidos.sort_values(by='Ventas', ascending=False)

    df_top_productos = df_productos_mas_vendidos.head(10)

    fig = px.bar(df_top_productos, x='Ventas', y='Producto', orientation='h')
    
    plot_div2 = fig.to_html(full_html=False)

    

    return render(request, "report/index.html" , context={'plot_div': plot_div, 'plot_div2': plot_div2,'ventas': ventas})




@csrf_exempt
def ventas_api(request, venta_id=None):
    
    try:
        if request.method == 'GET':
            if venta_id:
                # Obtener una venta específica por ID
                venta = Venta.objects.get(id=venta_id)
                return JsonResponse({
                    "id": venta.id,
                    "producto": venta.producto,
                    "valor": venta.valor,
                    "fecha": venta.fecha.strftime("%Y-%m-%d")
                })
            else:
                # Obtener todas las ventas
                ventas = list(Venta.objects.values("id", "producto", "valor", "fecha"))
                return JsonResponse(ventas, safe=False)

        elif request.method == 'POST':
            # Crear una nueva venta
            try:
                data = json.loads(request.body)  
                producto = data.get('producto')
                valor = data.get('valor')
                fecha = data.get('fecha')

                if not producto or not valor or not fecha:
                    return JsonResponse({"error": "Faltan datos requeridos (producto, valor, fecha)."}, status=400)

                nueva_venta = Venta.objects.create(producto=producto, valor=valor, fecha=fecha)
                return JsonResponse({"message": "Venta creada exitosamente.", "id": nueva_venta.id}, status=201)

            except json.JSONDecodeError:
                return JsonResponse({"error": "El cuerpo de la solicitud debe estar en formato JSON."}, status=400)

        elif request.method == 'PUT':
            # Actualizar una venta existente
            if not venta_id:
                return JsonResponse({"error": "Se requiere el ID de la venta para actualizar."}, status=400)

            try:
                data = json.loads(request.body)
                venta = Venta.objects.get(id=venta_id)

               
                venta.producto = data.get('producto', venta.producto)
                venta.valor = data.get('valor', venta.valor)
                venta.fecha = data.get('fecha', venta.fecha)
                venta.save()

                return JsonResponse({"message": "Venta actualizada exitosamente."}, status=200)

            except Venta.DoesNotExist:
                return JsonResponse({"error": "Venta no encontrada."}, status=404)
            except json.JSONDecodeError:
                return JsonResponse({"error": "El cuerpo de la solicitud debe estar en formato JSON."}, status=400)

        elif request.method == 'DELETE':
          
            if not venta_id:
                return JsonResponse({"error": "Se requiere el ID de la venta para eliminar."}, status=400)

            try:
                venta = Venta.objects.get(id=venta_id)
                venta.delete()
                return JsonResponse({"message": "Venta eliminada exitosamente."}, status=200)

            except Venta.DoesNotExist:
                return JsonResponse({"error": "Venta no encontrada."}, status=404)

        else:
            return JsonResponse({"error": "Método no permitido."}, status=405)

    except Exception as e:
        return JsonResponse({"error": f"Ocurrió un error inesperado: {str(e)}"}, status=500)
