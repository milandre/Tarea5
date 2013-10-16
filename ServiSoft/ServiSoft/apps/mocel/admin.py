
from django.contrib import admin
from ServiSoft.apps.mocel.models import cliente, producto, paquete, servicio, asociacion, consumo, inclucion, afiliacion

admin.site.register(cliente)
admin.site.register(producto)
admin.site.register(paquete)
admin.site.register(servicio)
admin.site.register(asociacion)
admin.site.register(consumo)
admin.site.register(inclucion)
admin.site.register(afiliacion)