# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from ServiSoft.apps.mocel.forms import addProductForm
from ServiSoft.apps.mocel.models import producto
from django.http import HttpResponseRedirect

def add_product_view(request):
	if request.user.is_authenticated():
		if request.method == "POST":
			form = addProductForm(request.POST)
			info = "Inicializando..."
			if form.is_valid():
				nombre = form.cleaned_data['nombre']
				descripcion = form.cleaned_data['descripcion']
				p = producto()
				p.nombre = nombre
				p.descripcion = descripcion
				p.status = True
				p.save() 	# Guarda la informacion
				info = "Se guardo satisfactoriamente..."
			else:
				info = "Informacion con datos incorrectos"
			form = addProductForm()
			ctx = {'form':form, 'informacion':info}
			return render_to_response('mocel/addProducto.html', ctx, context_instance=RequestContext(request))
		else: # GET
			form = addProductForm()
			ctx = {'form':form}
			return render_to_response('mocel/addProducto.html', ctx, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')