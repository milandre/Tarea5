
from django.conf.urls import patterns, url

urlpatterns = patterns('ServiSoft.apps.mocel.views',
	url(r'^add/producto/$', 'add_product_view', name="vista_agregar_producto"),
)
