#! -*- coding:utf-8 -*-
from django.contrib.auth.models import User
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
							Pagos,
							DetallePagos,
							DetallesEntregables,
							DetallesDocumentosGenerales,
							Alarmas,
							)



import datetime

class AuthForm(forms.Form):
    username = forms.CharField(required=True, max_length = 10, label=u'Usuario', help_text="", widget = forms.TextInput(attrs = {'class': "form-control", 'id':"inputEmail3", 'placeholder':"Usuario", 'name': "username"}))  
    password = forms.CharField(required=True, label=u'Contraseña', help_text="", widget=forms.PasswordInput(attrs = {'type':"password", 'class':"form-control", 'id':"inputPassword3", 'placeholder':"Contraseña", 'name':"password"}))

class RegistrarPersonalForm(forms.Form):
	rfc 						= forms.CharField(max_length=150, required=True, label="RFC", help_text="Proporcione el rfc del empleado", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	credencial_elector 			= forms.FileField(required=False, label="Identificación oficial (PDF)", help_text="Proporcione un documento como identificación oficial", widget=forms.FileInput(attrs={"type":"file", "id": "exampleInputFile"}))
	nombre 						= forms.CharField(max_length=150, required=True, label="Nombre(s)", help_text="", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	apellido_paterno 			= forms.CharField(max_length=150, required=True, label="Apellido paterno", help_text="", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	apellido_materno 			= forms.CharField(max_length=150, required=True, label="Apellido materno", help_text="", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	siglas_nombre 				= forms.CharField(max_length=150, required=True, label="Siglas", help_text="Siglas del nombre completo", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	genero 						= forms.ChoiceField(required=True, label="Genero", widget=forms.Select(attrs={'type': "select", 'class': "form-control"}), choices=Personal.SEXO_OPCIONES)
	direccion 					= forms.CharField(max_length=150, required=False, label="Dirección", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	telefono 					= forms.CharField(required=False, label="Teléfono", help_text="", widget=forms.TextInput(attrs={'type': "number", 'class': "form-control"}))
	no_seguro 					= forms.CharField(required=False, label="Número de seguro", help_text="Seguro médico IMSS o ISSSTE", widget=forms.TextInput(attrs={'type': "number", 'class': "form-control"}))
	fecha_ingreso 				= forms.DateField(required=True, label="Fecha de Ingreso", input_formats=['%d-%m-%Y', '%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d'], initial=datetime.datetime.now().date(), widget=forms.TextInput(attrs={'type': "date", 'class': "form-control"}))
	puesto 						= forms.CharField(max_length=150, required=True, label="Puesto", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	fecha_vencimiento_contrato 	= forms.DateField(required=False, label="Fecha de vencimiento de contrato", input_formats=['%d-%m-%Y', '%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d'], widget=forms.TextInput(attrs={'type': "date", 'class': "form-control"}))
	fecha_baja 					= forms.DateField(required=False, label="Fecha de baja", input_formats=['%d-%m-%Y', '%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d'], widget=forms.TextInput(attrs={'type': "date", 'class': "form-control"}) )
	motivo_baja 				= forms.CharField(max_length=150, required=False, label="Motivo de baja", widget=forms.Textarea(attrs={'class':"form-control", 'rows': 5, 'cols': 50}))
	dias_trabajo_al_mes 		= forms.FloatField(required=True, label="Días trabajados al mes", widget=forms.TextInput(attrs={'type': "number", "step": "any", 'class': "form-control"}))
	turno 						= forms.ChoiceField(required=True, label="Turno", widget=forms.Select(attrs={'type': "select", 'class': "form-control"}), choices=Personal.TIPO_TURNO)
	tipo_plaza 					= forms.ChoiceField(required=True, label="Tipo de plaza", widget=forms.Select(attrs={'type': "select", 'class': "form-control"}), choices=Personal.TIPO_PLAZA)
	especificacion 				= forms.CharField(max_length=150, required=False, label="Especifique el tipo de plaza", help_text="", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))#En caso de que se seleccione Otro, abrir campo de especificacion
	monto 						= forms.FloatField(required=True, label="Monto total mensual", widget=forms.TextInput(attrs={'type': "number", 'step':"any",'class': "form-control"}))	
	tipo_pago 					= forms.ChoiceField(required=True, label="El pago es", widget=forms.Select(attrs={'type': "select", 'class': "form-control"}), choices=Personal.TIPO_PAGO)

	def clean_credencial_elector(self):
		archivo = self.cleaned_data['credencial_elector']

		if archivo and not str(archivo.name).endswith(('.pdf', '.PDF')):
			raise forms.ValidationError('Archivo Invalido')

		return archivo


class RegistrarPagoEmpleadoForm(forms.Form):
	personal 					= forms.ModelChoiceField(required=True, label="Personal", help_text="", queryset=Personal.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	responsable 				= forms.CharField(max_length=150, required=True, label="Responsable", help_text="Responsable de pagar al empleado", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	archivo_documento_de_pago 	= forms.FileField(required=False, label="Documento de pago", help_text="", widget=forms.FileInput(attrs={"type":"file", "id": "exampleInputFile"}))

	def clean_archivo_documento_de_pago(self):
		archivo = self.cleaned_data['archivo_documento_de_pago']

		if archivo and not str(archivo.name).endswith(('.pdf', '.PDF')):
			raise forms.ValidationError('Archivo Invalido')

		return archivo	

class RegistrarDetalleDocResponsivaForm(forms.Form):
	personal 						= forms.ModelChoiceField(required=True, label="Personal", help_text="", queryset=Personal.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	archivo_documento_responsiva 	= forms.FileField(required=False, label="Documento de responsiva", help_text="", widget=forms.FileInput(attrs={"type":"file", "id": "exampleInputFile"}))

	def clean_archivo_documento_responsiva(self):
		archivo = self.cleaned_data['archivo_documento_responsiva']

		if archivo and not str(archivo.name).endswith(('.pdf', '.PDF')):
			raise forms.ValidationError('Archivo Invalido')

		return archivo

class RegistrarClienteForm(forms.Form):
	nombre 	= forms.CharField(max_length=150, required=True, label="Nombre", help_text="Nombre completo del cliente", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	siglas	= forms.CharField(max_length=150, required=True, label="Siglas", help_text="Siglas del nombre", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))

class RegistrarProyectoForm(forms.Form):
	nombre 			= forms.CharField(required=True, max_length=150, label="Nombre del proyecto", help_text=u"Nombre del proyecto", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	siglas 			= forms.CharField(required=True, max_length=45, label="Siglas del proyecto", help_text=u"Siglas del proyecto", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	cliente			= forms.ModelChoiceField(required=True, label="Cliente del proyecto", help_text='Cliente del proyecto' ,queryset=Clientes.objects.all(), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	responsable		= forms.ModelMultipleChoiceField(required=True, label="Responsble(s) del proyecto", help_text='Personal a cargo', widget=forms.SelectMultiple(attrs={'class':"form-control", 'size':3}), queryset=Personal.objects.filter(habilitado=True))
	fecha_inicio 	= forms.DateField(required=True, label="Fecha de inicio", help_text='Fecha de inicio del proyecto', input_formats=['%d-%m-%Y', '%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d'], widget=forms.TextInput(attrs={'type': "date", 'class': "form-control"}) )
	fecha_fin 		= forms.DateField(required=False, label="Fecha de termino", help_text='Fecha de termino del proyecto', input_formats=['%d-%m-%Y', '%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d'], widget=forms.TextInput(attrs={'type': "date", 'class': "form-control"}) )
	avance 			= forms.IntegerField(required=False, label="Avance", help_text='Porcentaje de avance del proyecto', widget=forms.TextInput(attrs={'type': "number", 'class': "form-control"}))
	comentario 		= forms.CharField(required=False,label="Comentario", help_text='Comentarios acerca del proyecto', max_length=500, widget=forms.Textarea(attrs={'class':"form-control", 'rows': 5, 'cols': 50}))

class RegistrarAnexotecnicoForm(forms.Form):
	numero_oficio 	= forms.IntegerField(required=True, label="Número de oficio de invitación", help_text="Invitación DEPENDENCIA-UCOL", widget=forms.TextInput(attrs={'type': "number", 'class': "form-control"}))	
	proyecto 		= forms.ModelChoiceField(required=True, label="Proyecto", queryset=Proyectos.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	nombre 			= forms.CharField(max_length=150, required=True, label="Nombre de la dependencia", help_text="Se refiere a la dependencia dueña del Proyecto", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	siglas 			= forms.CharField(max_length=150, required=True, label="Siglas de la dependencia", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	status 			= forms.ChoiceField(required=True, label="Estatus", help_text="Estado que guarda el documento", widget=forms.Select(attrs={'type': "select", 'class': "form-control"}), choices=AnexosTecnicos.STATUS)
	archivo         = forms.FileField(required=False, label="Subir archivo", help_text="Archivo en formato PDF", widget=forms.FileInput(attrs={"type":"file", "id": "exampleInputFile"}))
	
	def clean_archivo(self):
		_archivo = self.cleaned_data['archivo']

		if _archivo and not str(_archivo.name).endswith(('.pdf', '.PDF')):
			raise forms.ValidationError('Archivo Invalido')

		return _archivo

class RegistrarConvenioForm(forms.Form):
	numero 			= forms.CharField(max_length=150, required=True, label="Número de oficio de invitación", help_text="Invitación DEPENDENCIA-UCOL", widget=forms.TextInput(attrs={'type': "number", 'class': "form-control"}))
	proyecto 		= forms.ModelChoiceField(required=True, label="Proyecto", queryset=Proyectos.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	encargado 		= forms.ModelChoiceField(required=True, label="Encargado", help_text="Líder del proyecto",queryset=Personal.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	archivo 		= forms.FileField(required=False, label="Subir archivo", help_text="Archivo en formato PDF", widget=forms.FileInput(attrs={"type":"file", "id": "exampleInputFile"}))

	def clean_archivo(self):
		_archivo = self.cleaned_data['archivo']

		if _archivo and not str(_archivo.name).endswith(('.pdf', '.PDF')):
			raise forms.ValidationError('Archivo Invalido')

		return _archivo


class RegistrarContratoForm(forms.Form):
	numero_oficio 	= forms.CharField(max_length=150, required=True, label="Número de contrato", help_text="Número de oficion de contrato", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	proyecto        = forms.ModelChoiceField(required=True, label="Proyecto",help_text="", queryset=Proyectos.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	encargado 		= forms.ModelChoiceField(required=True, label="Encargado",help_text="Personal a cargo", queryset=Personal.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"})) #Responsable
	archivo 		= forms.FileField(required=False, label="Subir archivo",help_text="Archivo en formato PDF", widget=forms.FileInput(attrs={"type":"file", "id": "exampleInputFile"})) # Deprecated no entiendo por que eeste quedo en des uso nesesitamos hablarlo

	def clean_archivo(self):
		_archivo = self.cleaned_data['archivo']

		if _archivo and not str(_archivo.name).endswith(('.pdf', '.PDF')):
			raise forms.ValidationError('Archivo Invalido')

		return _archivo

class RegistrarEntregableForm(forms.Form):
	proyecto 		= forms.ModelChoiceField(required=True, label="Proyecto", help_text="", queryset=Proyectos.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	responsable 	= forms.ModelChoiceField(required=True, label="Responsable", help_text="Personal a cargo del entregable", queryset=Personal.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	total 			= forms.IntegerField(required=True, label="Total de entregables", help_text="Número total de entregables del proyecto", widget=forms.TextInput(attrs={'type': "number", 'class': "form-control"}))

class RegistrarDetalleEntregableForm(forms.Form):
	entregable 		= forms.ModelChoiceField(required=True, label="Entregable", help_text="", queryset=Entregables.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	responsable 	= forms.ModelChoiceField(required=True, label="Responsable", help_text="Responsable del entregable", queryset=Personal.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	numero 			= forms.IntegerField(required=True, label="Número de entregable", help_text="", widget=forms.TextInput(attrs={'type': "number", 'class': "form-control"}))
	nombre 			= forms.CharField(max_length=150, required=True, label="Nombre del entregable", help_text="", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	siglas 			= forms.CharField(max_length=150, required=True, label="Siglas del entregable", help_text="", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	status 			= forms.ChoiceField(required=True, label="Estatus", help_text="Estado que guarda el entregable", widget=forms.Select(attrs={'type': "select", 'class': "form-control"}), choices=DetallesEntregables.STATUS)
	archivo 		= forms.FileField(required=False, label="Subir archivo", help_text="Archivo en formato PDF", widget=forms.FileInput(attrs={"type":"file", "id": "exampleInputFile"}))
	
	def clean_archivo(self):
		_archivo = self.cleaned_data['archivo']

		if _archivo and not str(_archivo.name).endswith(('.pdf', '.PDF')):
			raise forms.ValidationError('Archivo Invalido')

		return _archivo

class RegistrarFacturaForm(forms.Form):
	contrato 			= forms.ModelChoiceField(required=True, label="Contrato", help_text="", queryset=Contratos.objects.all(), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	responsable 		= forms.ModelChoiceField(required=True, label="Responsable", help_text="", queryset=Personal.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	numero_factura 		= forms.IntegerField(required=True, label="Número de factura", help_text="Debe ser único", widget=forms.TextInput(attrs={'type': "number", 'class': "form-control"}))
	fecha_entrega 		= forms.DateField(required=True, label="Fecha de entrega", help_text="", input_formats=['%d-%m-%Y', '%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d'], widget=forms.TextInput(attrs={'type': "date", 'class': "form-control"}) )
	folio_venta 		= forms.CharField(required=True, max_length=150, label="Folio de venta", help_text="Folio de la factura", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	rfc 				= forms.CharField(required=True, max_length=150, label="RFC", help_text="RFC persona fisica/moral", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	direccion 			= forms.CharField(required=True, max_length=150, label="Dirección", help_text=u"dirección persona fisica/moral", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	subtotal 			= forms.FloatField(required=True, label="Subtotal", help_text="", widget=forms.TextInput(attrs={'type': "number", 'step':"any", 'class': "form-control"}))
	iva 				= forms.FloatField(required=True, label="Iva", help_text="", widget=forms.TextInput(attrs={'type': "number", 'step':"any", 'class': "form-control"}))
	total_con_numero 	= forms.FloatField(required=True, label="Total (numérico)", help_text="Total con número", widget=forms.TextInput(attrs={'type': "number", 'step':"any", 'class': "form-control"}))
	total_con_letra 	= forms.CharField(required=True, label="Total (letra)", help_text="Total econ letra", max_length=150, widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	status 				= forms.ChoiceField(required=True, label="Estatus", help_text="Estado que guarda la factura", widget=forms.Select(attrs={'type': "select", 'class': "form-control"}), choices=Facturas.STATUS)
	pagada 				= forms.BooleanField(initial=False, label="Pagada", help_text="", widget=forms.CheckboxInput(attrs={'type': "checkbox"}))	
	archivo_xml 		= forms.FileField(required=False, label="Subir archivo (XML)", help_text="Archivo en formato XML", widget=forms.FileInput(attrs={"type":"file", "id": "exampleInputFile"})) #Archivo en XML
	archivo_fisico 		= forms.FileField(required=False, label="Subir archivo (PDF)", help_text="Archivo en formato PDF", widget=forms.FileInput(attrs={"type":"file", "id": "exampleInputFile"})) #Archivo fisico de la factura

	def clean_archivo_xml(self):
		_archivo_xml = self.cleaned_data['archivo_xml']

		if _archivo_xml and not str(_archivo_xml.name).endswith(('.xml', '.XML')):
			raise forms.ValidationError('Archivo Invalido')

		return _archivo_xml

	def clean_archivo_fisico(self):
		_archivo_fisico = self.cleaned_data['archivo_fisico']

		if _archivo_fisico and not str(_archivo_fisico.name).endswith(('.pdf', '.PDF')):
			raise forms.ValidationError('Archivo Invalido')

		return _archivo_fisico


class RegistrarDetalleFacturaForm(forms.Form):
	factura 		= forms.ModelChoiceField(required=True, label="Factura", help_text="", queryset=Facturas.objects.all(), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	descripcion 	= forms.CharField(required=False, label="Descripción", help_text='Comentarios acerca de la fatura', max_length=200, widget=forms.Textarea(attrs={'class':"form-control", 'rows': 5, 'cols': 50}))
	cantidad 		= forms.IntegerField(required=True, label="Cantidad", help_text="", widget=forms.TextInput(attrs={'type': "number", 'class': "form-control"}))

class RegistrarPropuestaForm(forms.Form):
	numero_oficio 	= forms.CharField(max_length=150, required=True, label="Número de oficio", help_text="Invitación DEPENDENCIA-UCOL", widget=forms.TextInput(attrs={'type': "number", 'class': "form-control"}))
	proyecto 		= forms.ModelChoiceField(required=True, label="Proyecto", help_text="proyecto al que se hace la propuesta", queryset=Proyectos.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	responsable 	= forms.ModelChoiceField(required=True, label="Responsable", help_text="Líder del proyecto", queryset=Personal.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	status 			= forms.ChoiceField(required=True, label="Estatus", help_text="Estado que guarda la propuesta", widget=forms.Select(attrs={'type': "select", 'class': "form-control"}), choices=Propuestas.STATUS)
	archivo 		= forms.FileField(required=False, label="Subir archivo (PDF)", help_text="Archivo en formato PDF", widget=forms.FileInput(attrs={"type":"file", "id": "exampleInputFile"})) #Archivo fisico de la factura

	def clean_archivo(self):
		_archivo = self.cleaned_data['archivo']

		if _archivo and not str(_archivo.name).endswith(('.pdf', '.PDF')):
			raise forms.ValidationError('Archivo Invalido')

		return _archivo

class RegistrarDocGeneralForm(forms.Form):
	entidad 		= forms.ModelChoiceField(required=True, label="Entidad", help_text="Entidad a la que pertenece el documento", queryset=Entidades.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	clave 			= forms.CharField(max_length=150, required=True, label="Clave del documento", help_text="Ingresa una clave de relación", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))

class RegistrarDetalleDocGeneralForm(forms.Form):
	documentos_generales 	= forms.ModelChoiceField(required=True, label="Documento General", help_text="", queryset=DocumentosGenerales.objects.all(), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	responsable 			= forms.ModelChoiceField(required=True, label="Responsable", help_text="Responsable del documento",queryset=Personal.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	nombre 					= forms.CharField(max_length=150, required=True, label="Nombre del documento", help_text="", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	#tipo 					=
	status 					= forms.ChoiceField(required=True, label="Estatus", help_text="Estado que guarda el detalle", widget=forms.Select(attrs={'type': "select", 'class': 'form-control'}), choices=DetallesDocumentosGenerales.STATUS)
	archivo 				= forms.FileField(required=False, label="Subir archivo", help_text="Archivo en formato PDF", widget=forms.FileInput(attrs={"type":"file", "id": "exampleInputFile"}))
	#numero 					= forms.IntegerField(required=True, widget=forms.TextInput(attrs={'type': "number", 'class': "form-control"}))
	#siglas 					= forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	def clean_archivo(self):
		_archivo = self.cleaned_data['archivo']

		if _archivo and not str(_archivo.name).endswith(('.pdf', '.PDF')):
			raise forms.ValidationError('Archivo Invalido')
			
		return _archivo
		
class RegistrarEntidadForm(forms.Form):
	nombre 	= forms.CharField(max_length=150, required=True, label="Nombre de la Entidad", help_text="Se refiere al nombre de la empresa", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	siglas 	= forms.CharField(max_length=150, required=True, label="Siglas", help_text="Siglas del nombre de la entidad", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))#cuastiona la necesidad del a existencia de todos los campos de siglas pero temporalmetne que se queden
	tipo 	= forms.ChoiceField(required=True, label="Tipo", help_text="Tipo de organización", widget=forms.Select(attrs={'type': "select", 'class': "form-control"}), choices=Entidades.TIPOS)

class RegistrarEntidadProyectoForm(forms.Form):
	entidad 	= forms.ModelChoiceField(required=True, label="Entidad", help_text="Empresa a la que hace relación", queryset=Entidades.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	proyecto 	= forms.ModelChoiceField(required=True, label="Proyecto", help_text="Proyecto al que se hace relacion", queryset=Proyectos.objects.filter(habilitado=True).order_by('-fecha_inicio'), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	porcentaje  = forms.ChoiceField(required=True, label="Procentaje", help_text="Porcentaje con el cual se relacionan", widget=forms.Select(attrs={'type': "select", 'class': "form-control"}), choices=EntidadProyecto.PORCENTAJES) 

class RegistrarPagoForm(forms.Form):
	proyecto 				= forms.ModelChoiceField(required=True, label="Proyecto", help_text="Proyecto", queryset=Proyectos.objects.filter(habilitado=True).order_by('-fecha_inicio'), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	monto_total 			= forms.FloatField(required=False, label="Monto Total", help_text="Monto total", widget=forms.TextInput(attrs={'type': "number", 'step':"any",'class': "form-control"}))
	fecha_pago				= forms.DateField(required=False, label="Fecha de pago", help_text="Día que se realizó el pago", input_formats=['%d-%m-%Y', '%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d'], widget=forms.TextInput(attrs={'type': "date", 'class': "form-control"}), initial=datetime.datetime.now().date())

DETALLE_PAGOS = ((detalle.id, '%s' % detalle) for detalle in DetallePagos.objects.all())
class RegistrarDetallePagoForm(forms.Form):
	entregable 			= forms.ModelChoiceField(required=True, label="Detalle de Entregable", help_text="", queryset=DetallesEntregables.objects.order_by('-fecha_creacion'), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	pago 				= forms.ModelChoiceField(required=False, label="Pago", help_text="" ,queryset=Pagos.objects.all(), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	detalle_pago 		= forms.ChoiceField(required=False, label="Detalle de pago", help_text="" ,choices=DETALLE_PAGOS, widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	nombre_pago_origen 	= forms.CharField(max_length=150, required=False, label="Nombre de pago origen", help_text="", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	siglas_pago_origen	= forms.CharField(max_length=150, required=False, label="Siglas de pago origen", help_text="", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	nombre_pago_destino	= forms.CharField(max_length=150, required=False, label="Nombre de pago destino", help_text="", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	siglas_pago_destino	= forms.CharField(max_length=150, required=False, label="Siglas de pago destino", help_text="", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	fecha_pago			= forms.DateField(required=True, initial=datetime.datetime.now().date(), label="Fecha de pago", help_text="Día que se realizo el pago", input_formats=['%d-%m-%Y', '%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d'], widget=forms.TextInput(attrs={'type': "date", 'class': "form-control"}))
	monto 				= forms.FloatField(required=True, label="Monto", help_text="", widget=forms.TextInput(attrs={'type': "number", 'step':"any",'class': "form-control"}))
	porcentaje_de_pago	= forms.FloatField(required=True, label="Porcentaje del pago", help_text="", widget=forms.TextInput(attrs={'type': "number", 'step':"any",'class': "form-control"}))
	tipo_de_pago		= forms.ChoiceField(required=True, label="Tipo de pago", help_text="", widget=forms.Select(attrs={'type': "select", 'class': "form-control"}), choices=DetallePagos.TIPOS_DE_PAGO)
	documento_deposito	= forms.FileField(required=False, 	label="Documento de deposito", help_text="", widget=forms.FileInput(attrs={"type":"file", "id": "exampleInputFile"}))
	responsable 		= forms.ModelChoiceField(required=True, label="Responsable", help_text="", queryset=Personal.objects.filter(habilitado=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	pagado 				= forms.BooleanField(required=False, 	label="Pagado", help_text="", initial=False, widget=forms.CheckboxInput(attrs={'type': "checkbox"}))

	def clean_documento_deposito(self):
		_documento_deposito = self.cleaned_data['documento_deposito']

		if _documento_deposito and not str(_documento_deposito.name).endswith(('.pdf', '.PDF')):
			raise forms.ValidationError('Archivo Invalido')
			
		return _documento_deposito

class RegistrarHomologacionForm(forms.Form):
	nombre  = forms.CharField(max_length=150, required=True, label="Nombre de documento", help_text="", widget=forms.TextInput(attrs={'type': "text", 'class': "form-control"}))
	archivo = forms.FileField(required=False, label="Documento", help_text="", widget=forms.FileInput(attrs={"type":"file", "id": "exampleInputFile"}))

class RegistrarAlarmaForm(forms.Form):
	receptor 			= forms.ModelChoiceField(required=True, label="Destinatario", help_text="A quién va dirijida la alarma", queryset=User.objects.filter(is_active=True), widget=forms.Select(attrs={'type': "select", 'class': "form-control"}))
	fecha_vencimiento	= forms.DateField(required=True, initial=datetime.datetime.now().date(), label="Fecha de vencimiento", help_text="Día que vence la alarma", input_formats=['%d-%m-%Y', '%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d'], widget=forms.TextInput(attrs={'type': "date", 'class': "form-control"}))
	mensaje				= forms.CharField(max_length=150, required=True, label="Mensaje", widget=forms.Textarea(attrs={'class':"form-control", 'rows': 5, 'cols': 50}))