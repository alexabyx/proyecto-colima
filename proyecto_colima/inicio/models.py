#-*- coding:utf-8 -*-

from django.contrib.auth.models import User
from django.conf import settings
from django.db import models

from inicio.helpers import get_upload_path

import datetime

#esta clase se encarga de representar en el sistema los atributos de la clase PERSONAL 
class Personal(models.Model):
	REPOSITORIO 	= settings.PERSONAL

	TIPO_PAGO 		= (('S', 'Semanal'), ('Q', 'Quincenal'), ('M', 'Mensual'),)
	TIPO_PLAZA 		= (('B', 'Becario'), ('H','Honorarios'), ('E', 'Efectivo'), ('O', 'Otro'),)
	SEXO_OPCIONES 	= (('M', 'Masculino'), ('F', 'Femenino'),)

	rfc 						= models.CharField(max_length=150)
	credencial_elector 			= models.FileField(upload_to = get_upload_path, blank=True)
	nombre 						= models.CharField(max_length=150)
	apellido_paterno 			= models.CharField(max_length=150)
	apellido_materno 			= models.CharField(max_length=150)
	siglas_nombre 				= models.CharField(max_length=150, null=True)
	genero 						= models.CharField(max_length=2, choices=SEXO_OPCIONES)
	direccion 					= models.CharField(max_length=60)
	telefono 					= models.IntegerField(max_length=20)
	no_seguro 					= models.IntegerField(max_length=150)
	fecha_ingreso 				= models.DateField(default=datetime.datetime.now().date())
	puesto 						= models.CharField(max_length=150)
	turno 						= models.CharField(max_length=150)
	tipo_plaza 					= models.CharField(max_length=3, choices = TIPO_PLAZA)
	especificacion 				= models.CharField(max_length=150, null=True, blank=True)#En caso de que se seleccione Otro, abrir campo de especificacion
	tipo_pago 					= models.CharField(max_length=1, choices=TIPO_PAGO)
	monto 						= models.IntegerField()	
	dias_trabajo_al_mes 		= models.IntegerField()
	fecha_vencimiento_contrato 	= models.DateField()
	fecha_baja 					= models.DateField()
	motivo_baja 				= models.CharField(max_length=150)
	habilitado 					= models.BooleanField(default=True)

	def __unicode__(self):
		return "%s-%s" % (self.rfc, self.nombre)
	
	@property
	def genero_genero(self):
		return dict(self.SEXO_OPCIONES).get(self.genero, '---')

	def plaza_plaza(self):
		return dict(self.TIPO_PLAZA).get(self.tipo_plaza, '---')

	def pago_pago(self):
		return dict(self.TIPO_PAGO).get(self.tipo_pago, '---')

# Aqui se modelan los atributos multivaluados de la clase PAGOEMPLEADO (de uno a muchos)
class DetallePagoEmpleado(models.Model):
	REPOSITORIO 				= settings.DETALLES_PAGO_EMPLEADO

	personal 					= models.ForeignKey(Personal)
	responsable 				= models.CharField(max_length=150)
	archivo_documento_de_pago 	= models.FileField(upload_to = get_upload_path, blank=True)	

# Aqui se modelan los atributos multivaluados de la clase DOCUMENTORESPONSIVA (de uno a muchos)
class DetalleDocumentoResponsiva(models.Model):
	REPOSITORIO						= settings.DETALLES_DOCUMENTO_RESPONSIVA

	personal 						= models.ForeignKey(Personal)
	archivo_documento_responsiva 	= models.FileField(upload_to = get_upload_path, blank=True)

class Clientes(models.Model):
	REPOSITORIO 			= settings.DETALLE_DOCUMENTOS_GENERALES

	nombre 					= models.CharField(max_length=150)
	siglas					= models.CharField(max_length=150)
	fecha_creacion 			= models.DateField(default=datetime.datetime.now().date())
	habilitado 				= models.BooleanField(default=True)

	def __unicode__(self):
		return "%s" % (self.nombre)

#esta clase se encarga de representar en el sistema los atributos de la clase PROYECTOS
class Proyectos(models.Model):

	nombre 			= models.CharField(max_length=150, null=False)
	siglas 			= models.CharField(max_length=150, null=False)
	responsable 	= models.ManyToManyField(Personal, null=False)
	fecha_inicio 	= models.DateField(default=datetime.datetime.now().date(), null=False)
	fecha_fin 		= models.DateField(default=datetime.datetime.now().date(), null=True)
	
	avance 			= models.CharField(max_length=150, null=True)
	comentario 		= models.CharField(max_length=500, null=True)
	fecha_cambio 	= models.DateField(auto_now=True)
	cliente			= models.ForeignKey(Clientes, null=False)
	habilitado 		= models.BooleanField(default=True)
	#
	# Relacion uno a muchas Empresas(49, 46) 
	#

	def __unicode__(self):
		return "%s-%s" % (self.nombre, self.siglas)

#esta clase se encarga de representar en el sistema los atributos de la clase Anexostecnicos
class AnexosTecnicos(models.Model):
	REPOSITORIO 	= settings.ANEXOS_TECNICOS

	
	STATUS 			= (('EP','En proceso'),('ER', 'En revision'), ('A', 'Aceptado'))

	numero_oficio 	= models.IntegerField(blank=False)	
	proyecto 		= models.ForeignKey(Proyectos)
	
	nombre 			= models.CharField(max_length=150)
	siglas 			= models.CharField(max_length=150)
	
	status 			= models.CharField(max_length=3, choices=STATUS)
	fecha_creacion  = models.DateField(default=datetime.datetime.now().date())
	archivo         = models.FileField(upload_to=get_upload_path, blank=True)
	habilitado 		= models.BooleanField(default=True)
	#Responsable distinto del proyeto
	#
	#		
	#status = En proceso/en revision/aceptado
	
	def __unicode__(self):
		return "%s-%s" % (self.numero_oficio, self.nombre)

	@property
	def status_status(self):
		return dict(self.STATUS).get(self.status, '---')

#esta clase se encarga de representar en el sistema los atributos de la clase CONVENIOS
class Convenios (models.Model):
	REPOSITORIO 		= settings.CONVENIOS
	
	#Convenio Universidad Empresa 46/49
	numero 				= models.CharField(max_length=150)
	proyecto 			= models.ForeignKey(Proyectos)

	archivo 			= models.FileField(upload_to=get_upload_path, blank=True)
	fecha_creacion 		= models.DateField(default=datetime.datetime.now().date())

	encargado 			= models.ForeignKey(Personal)
	habilitado 			= models.BooleanField(default=True)

	def __unicode__(self):
		return "%s" % (self.numero)


#esta clase se encarga de representar en el sistema los atributos de la clase CONTRATOS
class Contratos(models.Model):
	REPOSITORIO 	= settings.CONTRATOS

	numero_oficio 	= models.CharField(max_length=150)
	proyecto        = models.ForeignKey(Proyectos)
	fecha_creacion  = models.DateField(default=datetime.datetime.now().date())
	encargado 		= models.ForeignKey(Personal) #Responsable
	
	archivo 		= models.FileField(upload_to=get_upload_path, blank=True) # Deprecated no entiendo por que eeste quedo en des uso nesesitamos hablarlo
	habilitado 		= models.BooleanField(default=True)
	#Contrato Dependencia universidad
	

	def __unicode__(self):
		return "%s-%s" % (self.numero_oficio, self.proyecto)

#esta clase se encarga de representar en el sistema los atributos de la clase ENTREGABLES

class Entregables(models.Model):
	REPOSITORIO 	= settings.ENTREGABLES

	proyecto 		= models.ForeignKey(Proyectos)
	responsable 	= models.ForeignKey(Personal)
	habilitado 		= models.BooleanField(default=True)
	total 			= models.IntegerField()
	
	#Total de entregables ---UNO/N----

# Aqui se modelan los atributos multivaluados de la clase ENTREGABLES (de uno a muchos)
class DetallesEntregables(models.Model):
	REPOSITORIO 	= settings.DETALLES_ENTREGABLES

	entregable 		= models.ForeignKey(Entregables)
	responsable 	= models.ForeignKey(Personal)
	numero 			= models.IntegerField()
	nombre 			= models.CharField(max_length=150)
	siglas 			= models.CharField(max_length=150)
	fecha_creacion 	= models.DateField(default=datetime.datetime.now())
	archivo 		= models.FileField(upload_to=get_upload_path, blank=True)

#esta clase se encarga de representar en el sistema los atributos de la clase FACTURAS
class Facturas(models.Model):
	REPOSITORIO 		= settings.FACTURAS

	TIPOS 				= (('E1', 'Empresa 46%'), ('E2', 'Empresa 49%'), ('U1', 'Universidad'))
	
	contrato 			= models.ForeignKey(Contratos)
	responsable 		= models.ForeignKey(Personal)

	tipo 				= models.CharField(max_length=3, choices=TIPOS)
	nombre 				= models.CharField(max_length=150)
	siglas 				= models.CharField(max_length=150)

	numero_factura 		= models.IntegerField(unique=True)
	fecha_factura 		= models.DateField(default=datetime.datetime.now())
	folio_venta 		= models.CharField(max_length=150, blank=True, help_text="Folio de la factura")

	rfc 				= models.CharField(max_length=150, help_text="RFC persona fisica/moral")
	direccion 			= models.CharField(max_length=150, help_text=u"dirección persona fisica/moral")

	subtotal 			= models.IntegerField()
	iva 				= models.IntegerField()
	total_con_numero 	= models.IntegerField()
	total_con_letra 	= models.CharField(max_length=150)
	pagada 				= models.BooleanField(default=False)
	archivo_xml 		= models.FileField(upload_to=get_upload_path, blank=True) #Archivo en XML
	archivo_fisico 		= models.FileField(upload_to=get_upload_path, blank=True) #Archivo fisico de la factura

	def __unicode__(self):
		return "%s-%s" % (self.nombre, self.folio_venta)

	@property
	def tipo_tipo(self):
		return  dict(self.TIPOS).get(self.tipo, '---')

#Aqui se modelan los atributos multivaluados de la clase FACTURA (de uno a muchos)
class DetallesFacturas(models.Model):
	factura 		= models.ForeignKey(Facturas) 
	descripcion 	= models.CharField(max_length=200)
	cantidad 		= models.IntegerField()

#esta clase se encarga de representar en el sistema los atributos de la clase PROPUESTAS
class Propuestas(models.Model):
	numero_oficio 	= models.CharField(max_length=150)
	proyecto 		= models.ForeignKey(Proyectos)
	responsable 	= models.ForeignKey(Personal)
	fecha_creacion 	= models.DateField(default=datetime.datetime.now().date())
	habilitado 		= models.BooleanField(default=True)

#esta clase se encarga de representar en el sistema los atributos de la claseDOCUMENTOS GENERALES
class DocumentosGenerales(models.Model):
	TIPOS 			= (('D1', 'Dependencia'), ('E', 'Empresa'), ('U1', 'Universidad'))

	proyecto 		= models.ForeignKey(Proyectos)
	clave 			= models.CharField(max_length=150)
	fecha_creacion 	= models.DateField(default=datetime.datetime.now().date())

#Aqui se modelan los atributos multivaluados de la clase Documentos Generales (de uno a muchos)
class DetallesDocumentosGenerales(models.Model):
	REPOSITORIO 			= settings.DETALLE_DOCUMENTOS_GENERALES

	documentos_generales 	= models.ForeignKey(DocumentosGenerales)
	responsable 			= models.ForeignKey(Personal)
	numero 					= models.IntegerField()
	nombre 					= models.CharField(max_length=150)
	siglas 					= models.CharField(max_length=150)
	archivo 				= models.FileField(upload_to=get_upload_path, blank=True)
	fecha_creacion 			= models.DateField(default=datetime.datetime.now().date())

#esta clase se encarga de representar en el sistema los atributos de la clase EMPRESAS
class Entidades(models.Model):
	TIPOS 				= (('E', 'Empresa'), ('U', 'Universidad'))

	nombre 				= models.CharField(max_length=150)
	siglas 				= models.CharField(max_length=150)#cuastiona la necesidad del a existencia de todos los campos de siglas pero temporalmetne que se queden
	tipo 				= models.CharField(max_length=3, choices=TIPOS)
	fecha_creacion 		= models.DateField(default=datetime.datetime.now().date())
	habilitado 			= models.BooleanField(default=True)

	def __unicode__(self):
		return "%s | %s" % (self.nombre, self.tipo)
		
	@property
	def tipo_tipo(self):
		return dict(self.TIPOS).get(self.tipo, '---')

class EntidadProyecto(models.Model):
	TIPOS 		= ( (46, '46%'), (49, '49%'))

	entidad 	= models.ForeignKey(Entidades)
	proyecto 	= models.ForeignKey(Proyectos)
	porcentaje  = models.IntegerField(choices=TIPOS)

	def porcentaje_porcenataje(self):
		return dict(self.TIPOS).get(self.porcentaje, '0%')