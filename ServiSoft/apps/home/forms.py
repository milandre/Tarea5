from django import forms

class ContactForm(forms.Form):
	Email	= forms.EmailField(widget=forms.TextInput())
	Titulo	= forms.CharField(widget=forms.TextInput())
	Texto	= forms.CharField(widget=forms.Textarea())

class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput())
	password = forms.CharField(widget=forms.PasswordInput(render_value=False))

class LoginCliente(forms.Form):
	identificador = forms.CharField(widget=forms.TextInput())

class addClienteForm(forms.Form):
	identificador = forms.CharField(widget=forms.TextInput())
	nombre		= forms.CharField(widget=forms.TextInput())
	direccion	= forms.CharField(widget=forms.TextInput())
	email		= forms.EmailField()

class afiliacionForm(forms.Form):
	cliente = forms.CharField(widget=forms.TextInput())
	producto = forms.CharField(widget=forms.TextInput()) 
	numero	= forms.CharField(widget=forms.TextInput())
	fechaAfiliacion = forms.DateField()
	tipoPlan = forms.MultipleChoiceField()
	
class ProductoCliente(forms.Form):
	num = forms.CharField(widget=forms.HiddenInput())
	