# Create your views here.

from django.http import HttpResponse
from ServiSoft.apps.ventas.models import producto
# Integramos la serializacion de los objetos
from django.core import serializers

def wsProductos_view(request):
    data = serializers.serialize("xml", producto.objects.filter(status=True))
    # Retorna la informacion en formato json o xml segun lo especificado
    return HttpResponse(data, mimetype='application/xml')
