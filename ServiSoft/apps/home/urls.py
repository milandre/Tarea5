
from django.conf.urls import patterns, url

urlpatterns = patterns('ServiSoft.apps.home.views',
	url(r'^$', 'index_view', name='vista_principal'),
	url(r'^about/$', 'about_view', name='vista_about'),
	url(r'^productos/page/(?P<pagina>.*)/$', 'productos_view', name='vista_productos'),
	url(r'^producto/(?P<id_prod>.*)/$', 'singleProducto_view', name='vista_single_producto'),
	url(r'^contacto/$', 'contacto_view', name='vista_contacto'),
	url(r'^login/$', 'login_view', name='vista_login'),
	url(r'^logout/$', 'logout_view', name='vista_logout'),
	url(r'loginCliente/$','loginCliente_view', name= 'vista_loginCliente'),
	url(r'^adminMocel/$','ingresarAdmin_view', name= 'vista_adminMocel'),
	#url(r'^registrarAdmin/$','nuevoAdmin_view', name= 'vista_registrarAdmin'),
	url(r'^AdminMocel/$','ingresarAdmin_view', name= 'vista_AdminMocel'),
	url(r'^registrarCliente/$','nuevoCliente_view', name= 'vista_registrarCliente'),
	url(r'^afiliaciones/$','afiliaciones_view', name= 'vista_afiliaciones'),
	url(r'^factura/$','factura_view', name= 'vista_factura'),
	url(r'^facturasActuales/$','facturasAct_view', name= 'vista_facturasAct'),
	url(r'^loginCliente/productoPostCliente/$', 'clientePostpago_view', name= 'vista_clientePostpago'),
	url(r'^loginCliente/productoPreCliente/$', 'clientePrepago_view', name= 'vista_clientePrepago'),
)
