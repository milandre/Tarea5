# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from ServiSoft.apps.mocel.models import producto
from ServiSoft.apps.mocel.models import cliente 
from ServiSoft.apps.mocel.models import afiliacion
from ServiSoft.apps.mocel.models import inclucion
from ServiSoft.apps.mocel.models import paquete
from ServiSoft.apps.mocel.models import servicio
from ServiSoft.apps.mocel.models import asociacion
from ServiSoft.apps.mocel.models import consumo
from ServiSoft.apps.mocel.models import administradorMocel
from ServiSoft.apps.home.forms import ContactForm, LoginForm, LoginCliente, addClienteForm, ProductoCliente
from django.core.mail import EmailMultiAlternatives	# Enviamos HTML
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, HttpResponse
# Paginacion en django
from django.core.paginator import Paginator, EmptyPage, InvalidPage
import logging
import datetime

def index_view(request):
	mensaje = " :) "
	# Contexto
	ctx = {'msg':mensaje}
	return render_to_response('home/index.html', ctx, context_instance=RequestContext(request))

def about_view(request):
	mensaje = " :) "
	# Contexto
	ctx = {'msg':mensaje}
	return render_to_response('home/about.html', ctx, context_instance=RequestContext(request))

def productos_view(request, pagina):
	lista_prod = producto.objects.filter(status=True) # Select * from ventas_productos where status = True;
	paginator = Paginator(lista_prod, 3) # Cuantos productos por pagina
	try:
		page = int(pagina)
	except:
		page = 1
	try:
		productos = paginator.page(page)
	except (EmptyPage, InvalidPage):
		productos = paginator.page(paginator.num_pages)
	ctx = {'productos':productos}
	return render_to_response('home/productos.html', ctx, context_instance=RequestContext(request))

def singleProducto_view(request, id_prod):
	prod = producto.objects.get(id=id_prod)
	ctx = {'producto':prod}
	return render_to_response('home/singleProducto.html', ctx, context_instance=RequestContext(request))

def contacto_view(request):
	info_enviado = False # Definir si se envio la informacion o no
	email = ""
	titulo = ""
	texto = ""
	if request.method == "POST":
		formulario = ContactForm(request.POST)
		if formulario.is_valid():
			info_enviado = True
			email = formulario.cleaned_data['Email']
			titulo = formulario.cleaned_data['Titulo']
			texto = formulario.cleaned_data['Texto']

			# Configuracion enviando mensaje via GMAIL
			to_admin = "servicios.servisoft@gmail.com"
			html_content =	"Informacion recibida de [%s]<br><br><br>****Mensaje****<br><br>%s"%(email, texto)
			msg = EmailMultiAlternatives('Correo de Contacto', html_content, 'from@server.com', [to_admin])
			msg.attach_alternative(html_content, 'text/html') # Definimos el contenido como HTML
			msg.send() # Enviamos en correo
	else:
		formulario = ContactForm()
	ctx = {'form':formulario, 'email':email, 'titulo':titulo, 'texto':texto, 'info_enviado':info_enviado}
	return render_to_response('home/contacto.html', ctx, context_instance=RequestContext(request))


def login_view(request):
	mensaje = ""
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		if request.method == "POST":
			form = LoginForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				usuario = authenticate(username=username, password=password)
				if usuario is not None and usuario.is_active:
					login(request, usuario)
					return HttpResponseRedirect('/')
				else:
					mensaje = "usuario y/o password incorrecto"
		form = LoginForm()
		ctx = {'form':form, 'mensaje':mensaje}
		return render_to_response('home/login.html', ctx, context_instance=RequestContext(request))

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

def loginCliente_view(request):


	if request.method == "POST":
		formulario = LoginCliente(request.POST)
		if formulario.is_valid():
			identificador = formulario.cleaned_data['identificador']
			ide = cliente.objects.filter(ident = identificador)
			if not ide:
				info = "Cliente no registrado. Intente de nuevo."
				form = LoginCliente()
				ctx = {'form':form, 'informacion': info}
				return render_to_response('home/vista_clientes.html', ctx, context_instance=RequestContext(request))
			else:
				form = ProductoCliente()
				lista_prodClientes = afiliacion.objects.filter(identCliente = ide)
				ctx = {'form':form, 'lista_prodClientes':lista_prodClientes}
				print session_set(request, identificador)
				return render_to_response('home/cuentaCliente.html', ctx, context_instance=RequestContext(request))

	form = LoginCliente()
	ctx = {'form':form}
	return render_to_response('home/vista_clientes.html', ctx, context_instance=RequestContext(request))

def nuevoCliente_view(request):
	
	if request.method == "POST":
		form = addClienteForm(request.POST)
		info = "Inicializando..."
		if form.is_valid():
			identificador = form.cleaned_data['identificador']
			nombre = form.cleaned_data['nombre']
			direccion = form.cleaned_data['direccion']
			email = form.cleaned_data['email']
			
			num = cliente.objects.filter(ident=identificador).count()
						
			if num == 0:
				c = cliente()
				c.ident = identificador
				c.nombre = nombre
				c.direccion = direccion
				c.status = True
				c.save() 	# Guarda la informacion
				info = "Se guardo satisfactoriamente. Ahora debe afiliarle un producto."
				ctx = {'form':form, 'informacion':info, 'numero': num}
				
				return render_to_response('home/addCliente.html', ctx, context_instance=RequestContext(request))
					
			else:
				info = "El cliente ya se encuentra registrado. Ingrese solo clientes nuevos"
				form = addClienteForm()
				ctx = {'form':form, 'informacion':info, 'numero':num}
				return render_to_response('home/addCliente.html', ctx, context_instance=RequestContext(request))
		else:
			info = "Informacion con datos incorrectos"
			form = addClienteForm()
			ctx = {'form':form, 'informacion':info}
			return render_to_response('home/addCliente.html', ctx, context_instance=RequestContext(request))

	else: # GET
		form = addClienteForm()
				
	ctx = {'form':form}
	return render_to_response('home/addCliente.html', ctx, context_instance=RequestContext(request))
	
def ingresarAdmin_view(request):
	if request.method == "POST":
		formulario = LoginForm(request.POST)
		if formulario.is_valid():
			us = request.POST['username'] #us = formulario.cleaned_data['username']
			contra = request.POST['password'] #contra = formulario.cleaned_data['password']
	
			admin = administradorMocel.objects.filter(usuario=us,contrasena=contra, status=True)
						
			if not admin:
				mensaje = "Usuario o contrasena invalido"
				ctx = {'form':formulario,'mensaje':mensaje}
				return render_to_response('home/admin.html', ctx, context_instance=RequestContext(request))
 				#return HttpResponseRedirect('/adminMocel')
 			
 			ctx = {'username': us}
 			return render_to_response('home/AdminMocel.html', ctx, context_instance=RequestContext(request))	
	else:		
		form = LoginForm()
		ctx = {'form':form}
		return render_to_response('home/admin.html', ctx, context_instance=RequestContext(request))	
 	
def afiliaciones_view(request):
	return render_to_response('home/afiliaciones.html', context_instance=RequestContext(request))	
 	
def factura_view(request):
	return render_to_response('home/factura.html', context_instance=RequestContext(request))	
 	
def facturasAct_view(request):
	return render_to_response('home/facturasAct.html', context_instance=RequestContext(request))	

def clientePrepago_view(request):
	identi = request.session['ide']
	formulario = ProductoCliente(request.POST)
	if formulario.is_valid():
		num = formulario.cleaned_data['num']
		print num, identi
		prodCliente = afiliacion.objects.filter(identCliente = identi, numero = num)
	today = datetime.datetime.now()
	dateFormat = today.strftime("%d-%m-%Y")
	timeFormat = today.strftime("%H:%M")
	ctx = {'identif':identi,'fecha':dateFormat, 'hora':timeFormat, 'num':num}
	return render_to_response('home/vista_clientePrepago.html', ctx, context_instance=RequestContext(request))

def clientePostpago_view(request, identi):
	# FECHA
	today = datetime.datetime.now()
	dateFormat = today.strftime("%d-%m-%Y")
	timeFormat = today.strftime("%H:%M")
	# CI O RIF
	identi = request.session['ide']
	formulario = ProductoCliente(request.POST)
	if formulario.is_valid():
		# NUMERO DE CELULAR
		num = formulario.cleaned_data['num']
		# DATOS CLIENTE
		c = cliente.objects.get(ident = identi)
		print c, num
		# AFILIACION CLIENTE-PRODUCTO
		#afil = afiliacion.objects.get(identCliente = c, numero = num)
		# ASOCIACION PRODUCTO-PAQUETE
# 		asoc = asociacion.objects.get(afiliacion = afil)
# 		listaInclusiones = []
# 		listaConsumos = []
		#for a in asoc:
		#	incl = inclucion.objects.get(paquete = a.paquete)
		#	for i in range(len(listaInclusiones)):
		#		if listaInclusiones[i][0] == incl.servicio.nombre:
		#			listaInclusiones[i][1] = listaInclusiones[i][0] + incl.cantIncluida
		#		else:
		#			listaInclusiones.append([incl.servicio.nombre, incl.cantIncluida])
		#cons = consumo.objects.get(afiliacion = afil)
		#for c in cons:
		#	listaConsumos.append([c.servicio.nombre, c.cantConsumida])
		#print listaInclusiones
		#print listaConsumos

		ctx = {'fecha':dateFormat, 'hora':timeFormat, 'identif':identi, 'cliente':c, 'num':num}
		return render_to_response('home/vista_clientePostpago.html', ctx, context_instance=RequestContext(request))
				

def session_set(request, ident):
	if 'ide' in request.session:
		return request.session['ide']
	else:
		request.session['ide'] = ident
		request.session.set_expiry(20)
		return True

