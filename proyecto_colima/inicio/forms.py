#! -*- coding:utf-8 -*-

from django import forms
from inicio.models import ( Proyectos,
							Clientes,
							Facturas,
							AnexosTecnicos,
							Contratos,
							Convenios,
							Propuestas,
							Personal,
							Entidades,
							Entregables,
							DocumentosGenerales,
							EntidadProyecto,
							)

import datetime

class AuthForm(forms.Form):
    username = forms.CharField(required=True, max_length = 10, label=u'Usuario', widget = forms.TextInput(attrs = {'class': "form-control", 'id':"inputEmail3", 'placeholder':"Usuario", 'name': "username"}))  
    password = forms.CharField(required=True,label=u'Contraseña',widget=forms.PasswordInput(attrs = {'type':"password", 'class':"form-control", 'id':"inputPassword3", 'placeholder':"Contraseña", 'name':"password"}))

class RegistrarProyectoForm(forms.Form):
	nombre 			= forms.CharField(required=True, max_length=150, help_text=u"Nombre del proyecto", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	siglas 			= forms.CharField(required=True, max_length=45, help_text=u"Siglas del proyecto", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	responsable		= forms.ModelMultipleChoiceField(required=True,help_text='Personal a cargo', widget=forms.SelectMultiple(attrs={'class':"form-control", 'size':3}), queryset=Personal.objects.all())

	fecha_inicio 	= forms.DateField(required=True,help_text='Fecha de inicio del proyecto', input_formats=['%d-%m-%Y', '%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d'], widget=forms.TextInput(attrs={'type': "date", 'class': "form-control"}) )
	fecha_fin 		= forms.DateField(required=False,help_text='Fecha de termino del proyecto', input_formats=['%d-%m-%Y', '%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d'], widget=forms.TextInput(attrs={'type': "date", 'class': "form-control"}) )
	avance 			= forms.CharField(required=False,help_text='Porcentaje de avance del proyecto', max_length=45, widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))

	comentario 		= forms.CharField(required=False,help_text='Comentarios acerca del proyecto', max_length=500, widget=forms.Textarea(attrs={'class':"form-control", 'rows': 5, 'cols': 50}))
	cliente			= forms.ModelChoiceField(required=True,help_text='Cliente del proyecto' ,queryset=Clientes.objects.all(), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))

class RegistrarFacturaForm(forms.Form):
	
	contrato 			= forms.ModelChoiceField(required=True, queryset=Contratos.objects.all(), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	responsable 		= forms.ModelChoiceField(required=True, queryset=Personal.objects.all(), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))

	tipo 				= forms.ChoiceField(required=True, widget=forms.Select(attrs={'type': "select", 'class': "form-control"}), choices=Facturas.TIPOS)
	nombre 				= forms.CharField(required=True, max_length=150, widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	siglas 				= forms.CharField(required=True, max_length=150, widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))

	numero_factura 		= forms.IntegerField(required=True, widget=forms.TextInput(attrs={'type': "number", 'class': "form-control"}))
	fecha_factura 		= forms.DateField(required=True, input_formats=['%d-%m-%Y', '%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d'], widget=forms.TextInput(attrs={'type': "date", 'class': "form-control"}) )
	folio_venta 		= forms.CharField(required=True, max_length=150, help_text="Folio de la factura", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))

	rfc 				= forms.CharField(required=True, max_length=150, help_text="RFC persona fisica/moral", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	direccion 			= forms.CharField(required=True, max_length=150, help_text=u"dirección persona fisica/moral", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))

	subtotal 			= forms.IntegerField(required=True, widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	iva 				= forms.IntegerField(required=True, widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	total_con_numero 	= forms.IntegerField(required=True, widget=forms.TextInput(attrs={'type': "number", 'class': "form-control"}))
	total_con_letra 	= forms.CharField(required=True, max_length=150, widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	pagada 				= forms.BooleanField(widget=forms.CheckboxInput(attrs={'type': "checkbox"}))	
	archivo_xml 		= forms.FileField(required=False, widget=forms.FileInput(attrs={"type":"file", "id": "exampleInputFile"})) #Archivo en XML
	archivo_fisico 		= forms.FileField(required=False, widget=forms.FileInput(attrs={"type":"file", "id": "exampleInputFile"})) #Archivo fisico de la factura

class RegistrarAnexotecnicoForm(forms.Form):
	numero_oficio 	= forms.IntegerField(required=True, widget=forms.TextInput(attrs={'type': "number", 'class': "form-control"}))	
	proyecto 		= forms.ModelChoiceField(required=True, queryset=Proyectos.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	
	nombre 			= forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	siglas 			= forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))

	status 			= forms.ChoiceField(required=True, widget=forms.Select(attrs={'type': "select", 'class': "form-control"}), choices=AnexosTecnicos.STATUS)
	archivo         = forms.FileField(required=False, widget=forms.FileInput(attrs={"type":"file", "id": "exampleInputFile"}))

class RegistrarContratoForm(forms.Form):
	numero_oficio 	= forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'type': "number", 'class': "form-control"}))
	proyecto        = forms.ModelChoiceField(required=True, queryset=Proyectos.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	encargado 		= forms.ModelChoiceField(required=True, queryset=Personal.objects.all(), widget=forms.Select(attrs={'type': "select", 'class': "form-control"})) #Responsable
	archivo 		= forms.FileField(required=False, widget=forms.FileInput(attrs={"type":"file", "id": "exampleInputFile"})) # Deprecated no entiendo por que eeste quedo en des uso nesesitamos hablarlo

class RegistrarConvenioForm(forms.Form):
	numero 			= forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'type': "number", 'class': "form-control"}))
	proyecto 		= forms.ModelChoiceField(required=True, queryset=Proyectos.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	encargado 		= forms.ModelChoiceField(required=True, queryset=Personal.objects.filter(), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	archivo 		= forms.FileField(required=False, widget=forms.FileInput(attrs={"type":"file", "id": "exampleInputFile"}))

class RegistrarConvenioForm(forms.Form):
	numero 				= forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'type': "number", 'class': "form-control"}))
	proyecto 			= forms.ModelChoiceField(required=True, queryset=Proyectos.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	encargado 			= forms.ModelChoiceField(required=True, queryset=Personal.objects.filter(), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	archivo 			= forms.FileField(required=False, widget=forms.FileInput(attrs={"type":"file", "id": "exampleInputFile"}))

class RegistrarPropuestaForm(forms.Form):
	numero_oficio 	= forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'type': "number", 'class': "form-control"}))
	proyecto 		= forms.ModelChoiceField(required=True, queryset=Proyectos.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	responsable 	= forms.ModelChoiceField(required=True, queryset=Personal.objects.filter(), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))

class RegistrarPersonalForm(forms.Form):
	rfc 						= forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	credencial_elector 			= forms.FileField(required=False, widget=forms.FileInput(attrs={"type":"file", "id": "exampleInputFile"}))
	nombre 						= forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	apellido_paterno 			= forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	apellido_materno 			= forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	siglas_nombre 				= forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	genero 						= forms.ChoiceField(required=True, widget=forms.Select(attrs={'type': "select", 'class': "form-control"}), choices=Personal.SEXO_OPCIONES)
	direccion 					= forms.CharField(max_length=60, required=True, widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	telefono 					= forms.IntegerField(required=True, widget=forms.TextInput(attrs={'type': "number", 'class': "form-control"}))
	no_seguro 					= forms.IntegerField(required=True, widget=forms.TextInput(attrs={'type': "number", 'class': "form-control"}))
	fecha_ingreso 				= forms.DateField(initial=datetime.datetime.now().date(), required=True, input_formats=['%d-%m-%Y', '%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d'], widget=forms.TextInput(attrs={'type': "date", 'class': "form-control"}))
	puesto 						= forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	turno 						= forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	tipo_plaza 					= forms.ChoiceField(required=True, widget=forms.Select(attrs={'type': "select", 'class': "form-control"}), choices=Personal.TIPO_PLAZA)
	especificacion 				= forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))#En caso de que se seleccione Otro, abrir campo de especificacion
	tipo_pago 					= forms.ChoiceField(required=True, widget=forms.Select(attrs={'type': "select", 'class': "form-control"}), choices=Personal.TIPO_PAGO)
	monto 						= forms.IntegerField(required=True, widget=forms.TextInput(attrs={'type': "number", 'class': "form-control"}))	
	dias_trabajo_al_mes 		= forms.IntegerField(required=True, widget=forms.TextInput(attrs={'type': "number", 'class': "form-control"}))
	fecha_vencimiento_contrato 	= forms.DateField(required=True, input_formats=['%d-%m-%Y', '%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d'], widget=forms.TextInput(attrs={'type': "date", 'class': "form-control"}))
	fecha_baja 					= forms.DateField(required=True, input_formats=['%d-%m-%Y', '%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d'], widget=forms.TextInput(attrs={'type': "date", 'class': "form-control"}) )
	motivo_baja 				= forms.CharField(max_length=150, required=True, widget=forms.Textarea(attrs={'class':"form-control", 'rows': 5, 'cols': 50}))

class RegistrarClienteForm(forms.Form):
	nombre 	= forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	siglas	= forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))

class RegistrarEntidadForm(forms.Form):
	nombre 	= forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	siglas 	= forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))#cuastiona la necesidad del a existencia de todos los campos de siglas pero temporalmetne que se queden
	tipo 	= forms.ChoiceField(required=True, widget=forms.Select(attrs={'type': "select", 'class': "form-control"}), choices=Entidades.TIPOS)

class RegistrarEntregableForm(forms.Form):
	proyecto 		= forms.ModelChoiceField(required=True, queryset=Proyectos.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	responsable 	= forms.ModelChoiceField(required=True, queryset=Personal.objects.filter(), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	total 			= forms.IntegerField(required=True, widget=forms.TextInput(attrs={'type': "number", 'class': "form-control"}))

class RegistrarDocGeneralForm(forms.Form):
	proyecto 		= forms.ModelChoiceField(required=True, queryset=Proyectos.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	clave 			= forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))

class RegistrarDetalleDocGeneralForm(forms.Form):
	documentos_generales 	= forms.ModelChoiceField(required=True, queryset=DocumentosGenerales.objects.all(), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	responsable 			= forms.ModelChoiceField(required=True, queryset=Personal.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	numero 					= forms.IntegerField(required=True, widget=forms.TextInput(attrs={'type': "number", 'class': "form-control"}))
	nombre 					= forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	siglas 					= forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	archivo 				= forms.FileField(required=False, widget=forms.FileInput(attrs={"type":"file", "id": "exampleInputFile"}))

class RegistrarDetalleDocResponsivaForm(forms.Form):
	personal 						= forms.ModelChoiceField(required=True, queryset=Personal.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	archivo_documento_responsiva 	= forms.FileField(required=False, widget=forms.FileInput(attrs={"type":"file", "id": "exampleInputFile"}))

class RegistrarPagoEmpleadoForm(forms.Form):
	personal 					= forms.ModelChoiceField(required=True, queryset=Personal.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	responsable 				= forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	archivo_documento_de_pago 	= forms.FileField(required=False, widget=forms.FileInput(attrs={"type":"file", "id": "exampleInputFile"}))

class RegistrarDetalleEntregableForm(forms.Form):
	entregable 		= forms.ModelChoiceField(required=True, queryset=Entregables.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	responsable 	= forms.ModelChoiceField(required=True, queryset=Personal.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	numero 			= forms.IntegerField(required=True, widget=forms.TextInput(attrs={'type': "number", 'class': "form-control"}))
	nombre 			= forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	siglas 			= forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	archivo 		= forms.FileField(required=False, widget=forms.FileInput(attrs={"type":"file", "id": "exampleInputFile"}))

class RegistrarDetalleFacturaForm(forms.Form):
	factura 		= forms.ModelChoiceField(required=True, queryset=Facturas.objects.all(), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	descripcion 	= forms.CharField(required=False,help_text='Comentarios acerca del proyecto', max_length=200, widget=forms.Textarea(attrs={'class':"form-control", 'rows': 5, 'cols': 50}))
	cantidad 		= forms.IntegerField(required=True, widget=forms.TextInput(attrs={'type': "number", 'class': "form-control"}))

class RegistrarEntidadProyectoForm(forms.Form):
	entidad 	= forms.ModelChoiceField(required=True, queryset=Entidades.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	proyecto 	= forms.ModelChoiceField(required=True, queryset=Proyectos.objects.filter(habilitado=True).order_by('fecha_inicio'), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	porcentaje  = forms.ChoiceField(required=True, widget=forms.Select(attrs={'type': "select", 'class': "form-control"}), choices=EntidadProyecto.TIPOS) 