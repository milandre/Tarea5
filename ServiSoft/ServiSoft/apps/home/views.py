# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from ServiSoft.apps.mocel.models import producto
from ServiSoft.apps.mocel.models import cliente 
from ServiSoft.apps.home.forms import ContactForm, LoginForm, LoginCliente
from django.core.mail import EmailMultiAlternatives	# Enviamos HTML
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
# Paginacion en django
from django.core.paginator import Paginator, EmptyPage, InvalidPage

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
			info_enviado = True
			cedula = formulario.cleaned_data['Identificador']
	
	form = LoginCliente()
	ctx = {'form':form}
	return render_to_response('home/vista_clientes.html', ctx, context_instance=RequestContext(request))

