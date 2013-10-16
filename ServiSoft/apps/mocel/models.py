from django.db import models

# Create your models here.

class cliente(models.Model):
	ident		= models.CharField(max_length=10, unique=True)
	nombre		= models.CharField(max_length=100)
	direccion	= models.CharField(max_length=300)
	email		= models.EmailField()
	status		= models.BooleanField(default=True)

	def __unicode__(self):
		visionCliente = "%s, %s" %(self.ident, self.nombre)
		return visionCliente

class producto(models.Model):
	nombre		= models.CharField(max_length=100)
	descripcion	= models.TextField(max_length=300)
	#foto		= models.ImageField(............)
	status		= models.BooleanField(default=True)

	def __unicode__(self):
		return self.nombre

TIPO_PLAN_CHOICES = (
	('prepago', 'prepago'),
	('postpago', 'postpago'),
)

class afiliacion(models.Model):
	numero		= models.CharField(max_length=7)
	fechaAfil	= models.DateField()
	tipoPlan 	= models.CharField(max_length=10, choices=TIPO_PLAN_CHOICES)
	identCliente	= models.ForeignKey(cliente)
	identProducto	= models.ForeignKey(producto)
	status		= models.BooleanField(default=True)

	def __unicode__(self):
		visionAfil = "propietario: %s, producto: %s, numero: %s" %(self.identCliente, self.identProducto, self.numero)
		return visionAfil

TIPO_PLAN_2_CHOICES = (
	('ambos','ambos'),
	('prepago', 'prepago'),
	('postpago', 'postpago'),
)

class paquete(models.Model):
	nombre		= models.CharField(max_length=100)
	descripcion	= models.TextField(max_length=300)
	costo		= models.DecimalField(max_digits=14, decimal_places=4)
	tipoPlan    = models.CharField(max_length=10, choices=TIPO_PLAN_2_CHOICES)
	status		= models.BooleanField(default=True)

	def __unicode__(self):
		return self.nombre

class servicio(models.Model):
	nombre		= models.CharField(max_length=100)
	descripcion	= models.TextField(max_length=300)
	tarifaBasica= models.DecimalField(max_digits=10, decimal_places=4)
	status		= models.BooleanField(default=True)

	def __unicode__(self):
		return self.nombre

class asociacion(models.Model):
	afiliacion 	= models.ForeignKey(afiliacion)
	paquete 	= models.ForeignKey(paquete)
	status		= models.BooleanField(default=True)

	def __unicode__(self):
		vistaAsocia = "%s, %s" %(self.afiliacion, self.paquete)
		return vistaAsocia

class consumo(models.Model):
	afiliacion	= models.ForeignKey(afiliacion)
	servicio	= models.ForeignKey(servicio)
	cantConsumida	= models.IntegerField()
	status		= models.BooleanField(default=True)

	def __unicode__(self):
		vistaConsume = "%s, %s: %s" %(self.afiliacion, self.servicio, self.cantConsumida)
		return vistaConsume

class inclucion(models.Model):
	paquete		= models.ForeignKey(paquete)
	servicio	= models.ForeignKey(servicio)
	cantIncluida	= models.IntegerField()
	status		= models.BooleanField(default=True)

	def __unicode__(self):
		vistaIncluye = "%s, %s: %s" %(self.paquete, self.servicio, self.cantIncluida)
		return vistaIncluye

