from django.db import models

# Create your models here.

class cliente(models.Model):
	nombre		= models.CharField(max_length=100)
	apellido	= models.CharField(max_length=100)
	status		= models.BooleanField(default=True)

	def __unicode__(self):
		nombreCompleto = "%s %s" %(self.nombre, self.apellido)
		return nombreCompleto

class producto(models.Model):

	nombre		= models.CharField(max_length=100)
	descripcion	= models.TextField(max_length=300)
	status		= models.BooleanField(default=True)
	#precio		= models.DecimalField(max_digits=6, decimal_places=2)
	#stock		= models.IntegerField()

	def __unicode__(self):
		return self.nombre
