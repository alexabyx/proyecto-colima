#-*- coding:utf-8 -*-

from django.contrib.auth.models import User
from django.conf import settings
from django.db import models

from inicio.helpers import get_upload_path

import datetime

#esta clase se encarga de representar en el sistema los atributos de la clase PERSONAL 
class Personal(models.Model):
	class Meta:
		verbose_name_plural = 'Personal'

	REPOSITORIO 	= settings.PERSONAL
	HISTORICO 		= settings.PERSONAL_HIST

	TIPO_TURNO 		= (('M', 'Matutino'), ('V', 'Vespertino'), ('N', 'Nocturno'),)
	TIPO_PAGO 		= (('S', 'Semanal'), ('Q', 'Quincenal'), ('M', 'Mensual'),)
	TIPO_PLAZA 		= (('B', 'Becario'), ('H','Honorarios'), ('E', 'Efectivo'), ('O', 'Otro'),)
	SEXO_OPCIONES 	= (('M', 'Masculino'), ('F', 'Femenino'),)

	rfc 						= models.CharField(max_length=150)
	credencial_elector 			= models.FileField(upload_to = get_upload_path, null=True)
	nombre 						= models.CharField(max_length=150, verbose_name = "Nombre(s)")
	apellido_paterno 			= models.CharField(max_length=150)
	apellido_materno 			= models.CharField(max_length=150)
	siglas_nombre 				= models.CharField(max_length=150)
	genero 						= models.CharField(max_length=2, choices=SEXO_OPCIONES)
	direccion 					= models.CharField(max_length=150, blank=True)
	no_seguro 					= models.CharField(max_length=150, null=True)
	telefono 					= models.CharField(max_length=150, null=True)
	fecha_ingreso 				= models.DateField(default=datetime.datetime.now().date())
	puesto 						= models.CharField(max_length=150)
	fecha_vencimiento_contrato 	= models.DateField(null=True)
	fecha_baja 					= models.DateField(null=True)
	motivo_baja 				= models.CharField(max_length=500, blank=True)	
	dias_trabajo_al_mes 		= models.FloatField()
	turno 						= models.CharField(max_length=3, choices=TIPO_TURNO)
	tipo_plaza 					= models.CharField(max_length=3, choices=TIPO_PLAZA)
	especificacion 				= models.CharField(max_length=150, blank=True)#En caso de que se seleccione Otro, abrir campo de especificacion
	monto 						= models.FloatField()	
	tipo_pago 					= models.CharField(max_length=3, choices=TIPO_PAGO)
	habilitado 					= models.BooleanField(default=True)
	historico 					= models.IntegerField(max_length=5, default=1)

	def __unicode__(self):
		return "%s-%s" % (self.rfc, self.nombre)
	
	def genero_genero(self):
		return dict(self.SEXO_OPCIONES).get(self.genero, '---')

	def plaza_plaza(self):
		return dict(self.TIPO_PLAZA).get(self.tipo_plaza, '---')

	def pago_pago(self):
		return dict(self.TIPO_PAGO).get(self.tipo_pago, '---')

	def turno_turno(self):
		return dict(self.TIPO_TURNO).get(self.turno, '---')

	def credencial_liga(self):
		try:
			return self.credencial_elector.url
		except ValueError:
			return self.credencial_elector

	def en_historico(self):
		return self.historico in (2, 3) 


# Aqui se modelan los atributos multivaluados de la clase PAGOEMPLEADO (de uno a muchos)
class DetallePagoEmpleado(models.Model):
	class Meta:
		verbose_name_plural = 'Detalle Pago Empleado'

	REPOSITORIO 				= settings.DETALLES_PAGO_EMPLEADO
	HISTORICO 					= settings.DETALLES_PAGO_EMPLEADO_HIST

	personal 					= models.ForeignKey(Personal)
	responsable 				= models.CharField(max_length=150)
	archivo_documento_de_pago 	= models.FileField(upload_to = get_upload_path, null=True)
	historico 					= models.IntegerField(max_length=5, default=1)

	def archivo_documento_de_pago_liga(self):
		try:
			return self.archivo_documento_de_pago.url
		except ValueError:
			return self.archivo_documento_de_pago

	def en_historico(self):
		return self.historico in (2, 3) 


# Aqui se modelan los atributos multivaluados de la clase DOCUMENTORESPONSIVA (de uno a muchos)
class DetalleDocumentoResponsiva(models.Model):
	class Meta:
		verbose_name_plural = 'Detalle Documentos Responsiva'

	REPOSITORIO						= settings.DETALLES_DOCUMENTO_RESPONSIVA
	HISTORICO 						= settings.DETALLES_DOCUMENTO_RESPONSIVA_HIST

	personal 						= models.ForeignKey(Personal)
	archivo_documento_responsiva 	= models.FileField(upload_to = get_upload_path, null=True)
	historico 						= models.IntegerField(max_length=5, default=1)

	def archivo_documento_responsiva_liga(self):
		try:
			return self.archivo_documento_responsiva.url
		except ValueError:
			return self.archivo_documento_responsiva

	def en_historico(self):
		return self.historico in (2, 3) 

class Clientes(models.Model):
	class Meta:
		verbose_name_plural = 'Clientes'

	nombre 					= models.CharField(max_length=150)
	siglas					= models.CharField(max_length=150)
	fecha_creacion 			= models.DateField(default=datetime.datetime.now().date())
	habilitado 				= models.BooleanField(default=True)
	historico				= models.IntegerField(max_length=5, default=1)

	def __unicode__(self):
		return "%s" % (self.nombre)

	def en_historico(self):
		return self.historico in (2, 3) 


#esta clase se encarga de representar en el sistema los atributos de la clase PROYECTOS
class Proyectos(models.Model):
	class Meta:
		verbose_name_plural = 'Proyectos'

	nombre 			= models.CharField(max_length=150, blank=False)
	siglas 			= models.CharField(max_length=150, blank=False)
	cliente			= models.ForeignKey(Clientes)
	responsable 	= models.ManyToManyField(Personal)
	fecha_inicio 	= models.DateField(default=datetime.datetime.now().date(), null=False)
	fecha_fin 		= models.DateField(default=datetime.datetime.now().date(), null=True)
	avance 			= models.IntegerField(max_length=5, null=True)
	comentario 		= models.CharField(max_length=500, blank=True)
	fecha_cambio 	= models.DateField(auto_now=True)
	habilitado 		= models.BooleanField(default=True)
	historico 		= models.IntegerField(max_length=5, default=1)

	
	#
	# Relacion uno a muchas Empresas(49, 46) 
	#

	def __unicode__(self):
		return "%s-%s" % (self.nombre, self.siglas)

	def en_historico(self):
		return self.historico in (2, 3) 

#esta clase se encarga de representar en el sistema los atributos de la clase Anexostecnicos
class AnexosTecnicos(models.Model):
	class Meta:
		verbose_name_plural = 'Anexos Tecnicos'

	REPOSITORIO 	= settings.ANEXOS_TECNICOS
	HISTORICO 		= settings.ANEXOS_TECNICOS_HIST

	STATUS 			= (('EP','En proceso'),('ER', 'En revision'), ('A', 'Aceptado'))

	numero_oficio 	= models.IntegerField()	
	proyecto 		= models.ForeignKey(Proyectos)
	nombre 			= models.CharField(max_length=150)
	siglas 			= models.CharField(max_length=150)
	status 			= models.CharField(max_length=3, choices=STATUS)
	fecha_creacion  = models.DateField(default=datetime.datetime.now().date())
	archivo         = models.FileField(upload_to=get_upload_path, null=True)
	habilitado 		= models.BooleanField(default=True)
	historico 		= models.IntegerField(max_length=5, default=1)
	#Responsable distinto del proyeto
	#
	#		
	#status = En proceso/en revision/aceptado
	
	def __unicode__(self):
		return "%s-%s" % (self.numero_oficio, self.nombre)

	def status_status(self):
		return dict(self.STATUS).get(self.status, '---')

	def archivo_liga(self):
		try:
			return self.archivo.url
		except ValueError:
			return self.archivo

	def en_historico(self):
		return self.historico in (2, 3)

#esta clase se encarga de representar en el sistema los atributos de la clase CONVENIOS
class Convenios (models.Model):
	class Meta:
		verbose_name_plural = 'Convenios'

	REPOSITORIO 		= settings.CONVENIOS
	HISTORICO 			= settings.CONVENIOS_HIST
	
	#Convenio Universidad Empresa 46/49
	numero 				= models.CharField(max_length=150)
	proyecto 			= models.ForeignKey(Proyectos)
	encargado 			= models.ForeignKey(Personal)
	archivo 			= models.FileField(upload_to=get_upload_path, null=True)
	fecha_creacion 		= models.DateField(default=datetime.datetime.now().date())
	habilitado 			= models.BooleanField(default=True)
	historico 			= models.IntegerField(max_length=5, default=1)

	def __unicode__(self):
		return "%s" % (self.numero)

	def archivo_liga(self):
		try:
			return self.archivo.url
		except ValueError:
			return self.archivo

	def en_historico(self):
		return self.historico in (2, 3)

#esta clase se encarga de representar en el sistema los atributos de la clase CONTRATOS
class Contratos(models.Model):
	class Meta:
		verbose_name_plural = 'Contratos'

	REPOSITORIO 	= settings.CONTRATOS
	HISTORICO 		= settings.CONTRATOS_HIST

	numero_oficio 	= models.CharField(max_length=150) # Esto qué?!
	proyecto        = models.ForeignKey(Proyectos)
	encargado 		= models.ForeignKey(Personal) #Responsable
	archivo 		= models.FileField(upload_to=get_upload_path, null=True) # Deprecated no entiendo por que eeste quedo en des uso nesesitamos hablarlo
	fecha_creacion  = models.DateField(default=datetime.datetime.now().date())
	habilitado 		= models.BooleanField(default=True)
	historico 		= models.IntegerField(max_length=5, default=1)
	#Contrato Dependencia universidad
	
	def __unicode__(self):
		return "%s-%s" % (self.numero_oficio, self.proyecto)

	def archivo_liga(self):
		try:
			return self.archivo.url
		except ValueError:
			return self.archivo

	def en_historico(self):
		return self.historico in (2, 3)


#esta clase se encarga de representar en el sistema los atributos de la clase ENTREGABLES

class Entregables(models.Model):
	class Meta:
		verbose_name_plural = 'Entregables'

	proyecto 		= models.ForeignKey(Proyectos)
	responsable 	= models.ForeignKey(Personal)
	total 			= models.IntegerField()
	habilitado 		= models.BooleanField(default=True)
	historico 		= models.IntegerField(max_length=5, default=1)

	def __unicode__(self):
		return "%s | %s" % (self.proyecto, self.responsable)

	def en_historico(self):
		return self.historico in (2, 3)
	#Total de entregables ---UNO/N----

# Aqui se modelan los atributos multivaluados de la clase ENTREGABLES (de uno a muchos)
class DetallesEntregables(models.Model):
	class Meta:
		verbose_name_plural = 'Detalle de entregables'

	REPOSITORIO 	= settings.DETALLES_ENTREGABLES
	HISTORICO 		= settings.DETALLES_ENTREGABLES_HIST
	STATUS 			= (('EP','En proceso'),('ER', 'En revision'), ('A', 'Aceptado'))

	entregable 		= models.ForeignKey(Entregables)
	responsable 	= models.ForeignKey(Personal)
	numero 			= models.IntegerField()
	nombre 			= models.CharField(max_length=150)
	siglas 			= models.CharField(max_length=150)
	status 			= models.CharField(max_length=3, choices=STATUS)
	fecha_creacion 	= models.DateField(default=datetime.datetime.now().date())
	archivo 		= models.FileField(upload_to=get_upload_path, null=True)
	historico 		= models.IntegerField(max_length=5, default=1)

	def __unicode__(self):
		return "%s - %s" % (self.entregable, self.numero)

	def status_status(self):
		return dict(self.STATUS).get(self.status, '---')
	
	def archivo_liga(self):
		try:
			return self.archivo.url
		except ValueError:
			return self.archivo

	def en_historico(self):
		return self.historico in (2, 3)

#esta clase se encarga de representar en el sistema los atributos de la clase FACTURAS
class Facturas(models.Model):
	class Meta:
		verbose_name_plural = 'Facturas'

	REPOSITORIO 		= settings.FACTURAS
	HISTORICO 			= settings.FACTURAS_HIST
	STATUS 				= (('EP','En proceso'),('ER', 'En revision'), ('A', 'Aceptado'))

	contrato 			= models.ForeignKey(Contratos)
	responsable 		= models.ForeignKey(Personal)
	numero_factura 		= models.IntegerField(unique=True)
	fecha_emision 		= models.DateField(default=datetime.datetime.now())
	fecha_entrega 		= models.DateField()
	folio_venta 		= models.CharField(max_length=150, help_text="Folio de venta")
	rfc 				= models.CharField(max_length=150, help_text="RFC persona fisica/moral")
	direccion 			= models.CharField(max_length=150, help_text=u"dirección persona fisica/moral")
	subtotal 			= models.FloatField()
	iva 				= models.FloatField()
	total_con_numero 	= models.FloatField()
	total_con_letra 	= models.CharField(max_length=150)
	status 				= models.CharField(max_length=3, choices=STATUS)
	pagada 				= models.BooleanField(default=False)
	archivo_xml 		= models.FileField(upload_to=get_upload_path, null=True) #Archivo en XML
	archivo_fisico 		= models.FileField(upload_to=get_upload_path, null=True) #Archivo fisico de la factura
	historico 			= models.IntegerField(max_length=5, default=1)

	def __unicode__(self):
		return "%s-%s" % (self.numero_factura, self.folio_venta)

	def status_status(self):
		return dict(self.STATUS).get(self.status, '---')

	def archivo_xml_liga(self):
		try:
			return self.archivo_xml.url
		except ValueError:
			return self.archivo_xml

	def archivo_fisico_liga(self):
		try:
			return self.archivo_fisico.url
		except ValueError:
			return self.archivo_fisico

	def en_historico(self):
		return self.historico in (2, 3)

#Aqui se modelan los atributos multivaluados de la clase FACTURA (de uno a muchos)
class DetallesFacturas(models.Model):
	class Meta:
		verbose_name_plural = 'Detalle de facturas'

	factura 		= models.ForeignKey(Facturas) 
	descripcion 	= models.CharField(max_length=500, blank=True)
	cantidad 		= models.IntegerField()
	historico 		= models.IntegerField(max_length=5, default=1)

	def en_historico(self):
		return self.historico in (2, 3)

#esta clase se encarga de representar en el sistema los atributos de la clase PROPUESTAS
class Propuestas(models.Model):
	class Meta:
		verbose_name_plural = 'Propuestas'

	REPOSITORIO 	= settings.PROPUESTAS
	HISTORICO 		= settings.PROPUESTAS_HIST

	STATUS 			= (('EP','En proceso'),('ER', 'En revision'), ('A', 'Aceptado'))

	numero_oficio 	= models.CharField(max_length=150)
	proyecto 		= models.ForeignKey(Proyectos)
	responsable 	= models.ForeignKey(Personal)
	status 			= models.CharField(max_length=3, choices=STATUS)
	archivo 		= models.FileField(upload_to=get_upload_path, null=True)
	fecha_creacion 	= models.DateField(default=datetime.datetime.now().date())
	habilitado 		= models.BooleanField(default=True)
	historico 		= models.IntegerField(max_length=5, default=1)

	def archivo_liga(self):
		try:
			return self.archivo.url
		except ValueError:
			return self.archivo

	def status_status(self):
		return dict(self.STATUS).get(self.status, '---')

	def en_historico(self):
		return self.historico in (2, 3)

#esta clase se encarga de representar en el sistema los atributos de la clase EMPRESAS
class Entidades(models.Model):
	class Meta:
		verbose_name_plural = 'Entidades (empresas)'

	TIPOS 				= (('E', 'Empresa'), ('U', 'Universidad'))

	nombre 				= models.CharField(max_length=150)
	siglas 				= models.CharField(max_length=150)#cuestiona la necesidad del a existencia de todos los campos de siglas pero temporalmetne que se queden
	tipo 				= models.CharField(max_length=3, choices=TIPOS)
	fecha_creacion 		= models.DateField(default=datetime.datetime.now().date())
	habilitado 			= models.BooleanField(default=True)
	historico 			= models.IntegerField(max_length=5, default=1)

	def __unicode__(self):
		return "%s | %s" % (self.nombre, self.tipo)

	def tipo_tipo(self):
		return dict(self.TIPOS).get(self.tipo, '---')

	def en_historico(self):
		return self.historico in (2, 3)

class EntidadProyecto(models.Model):
	class Meta:
		verbose_name_plural = 'Entidad-Proyecto'

	PORCENTAJES = ( (46, '46%'), (49, '49%'))

	entidad 	= models.ForeignKey(Entidades)
	proyecto 	= models.ForeignKey(Proyectos)
	porcentaje  = models.IntegerField(choices=PORCENTAJES)
	historico 	= models.IntegerField(max_length=5, default=1)

	def porcentaje_porcentaje(self):
		return dict(self.PORCENTAJES).get(self.porcentaje, '0%')

	def en_historico(self):
		return self.historico in (2, 3)

#esta clase se encarga de representar en el sistema los atributos de la clase DOCUMENTOS GENERALES
class DocumentosGenerales(models.Model):
	class Meta:
		verbose_name_plural = 'Documentos Generales'

	TIPOS 			= (('D1', 'Dependencia'), ('E', 'Empresa'), ('U1', 'Universidad'))

	#proyecto 		= models.ForeignKey(Proyectos)
	entidad 		= models.ForeignKey(Entidades)
	clave 			= models.CharField(max_length=150)
	fecha_creacion 	= models.DateField(default=datetime.datetime.now().date())
	historico 		= models.IntegerField(max_length=5, default=1)

	def __unicode__(self):
		return "%s" % (self.clave)

	def en_historico(self):
		return self.historico in (2, 3)

#Aqui se modelan los atributos multivaluados de la clase Documentos Generales (de uno a muchos)
class DetallesDocumentosGenerales(models.Model):
	class Meta:
		verbose_name_plural = 'Detalle de documentos generales'

	REPOSITORIO 			= settings.DETALLE_DOCUMENTOS_GENERALES
	HISTORICO 				= settings.DETALLE_DOCUMENTOS_GENERALES_HIST
	STATUS 					= (('C', 'Completos'), ('I', 'Incompletos'),)

	documentos_generales 	= models.ForeignKey(DocumentosGenerales)
	responsable 			= models.ForeignKey(Personal)
	nombre 					= models.CharField(max_length=150)
	#tipo?
	status  				= models.CharField(max_length=3, choices=STATUS)
	archivo 				= models.FileField(upload_to=get_upload_path, null=True)
	fecha_creacion 			= models.DateField(default=datetime.datetime.now().date())
	historico 				= models.IntegerField(max_length=5, default=1)
	#siglas 					= models.CharField(max_length=150) #Deprecated o que chow
	#numero 					= models.IntegerField() #Deprecated o que chow

	def archivo_liga(self):
		try:
			return self.archivo.url
		except ValueError:
			return self.archivo

	def status_status(self):
		return dict(self.STATUS).get(self.status, '---')

	def en_historico(self):
		return self.historico in (2, 3)

class Pagos (models.Model):
	class Meta:
		verbose_name_plural = 'Pagos'

	proyecto 				= models.ForeignKey(Proyectos)
	monto_total 			= models.FloatField(null=True)
	fecha_pago				= models.DateField(null=True)
	historico 				= models.IntegerField(max_length=5, default=1)

	def __unicode__(self):
		return "%s - %s" % (self.proyecto, self.monto_total)

	def en_historico(self):
		return self.historico in (2, 3)

class DetallePagos (models.Model):
	class Meta:
		verbose_name_plural = 'Detalle de pagos'

	REPOSITORIO 		= settings.DETALLE_PAGOS
	HISTORICO 			= settings.DETALLE_PAGOS_HIST
	TIPOS_DE_PAGO 		= (('DB', 'Deposito Bancario'), ('DE', 'Deposito Electronico'),('PE','Pago en Efectivo'))

	entregable 			= models.ForeignKey(DetallesEntregables)
	pago 				= models.ForeignKey(Pagos, null=True)
	detalle_pago 		= models.IntegerField(null=True)
	nombre_pago_origen 	= models.CharField(max_length=150, blank=True)
	siglas_pago_origen	= models.CharField(max_length=150, blank=True)
	nombre_pago_destino	= models.CharField(max_length=150, blank=True)
	siglas_pago_destino	= models.CharField(max_length=150, blank=True)
	fecha_pago			= models.DateField()
	monto 				= models.FloatField()
	porcentaje_de_pago	= models.FloatField()
	tipo_de_pago		= models.CharField(max_length=2, choices=TIPOS_DE_PAGO)
	documento_deposito	= models.FileField(upload_to=get_upload_path, null=True)
	responsable 		= models.ForeignKey(Personal)
	pagado 				= models.BooleanField(default=False)
	historico 			= models.IntegerField(max_length=5, default=1)

	def __unicode__(self):
		return "%s | %s" % (self.entregable, self.pago)
		
	def documento_deposito_liga(self):
		try:
			return self.documento_deposito.url
		except ValueError:
			return self.documento_deposito

	def tipo_pago_tipo(self):
		return dict(self.TIPOS_DE_PAGO).get(self.tipo_de_pago, '---')

	def en_historico(self):
		return self.historico in (2, 3)

class Alarmas (models.Model):
	class Meta:
		verbose_name_plural = 'Alarmas'

	STATUS 				= (('R','Revisado'), ('P','Pendiente'))

	emisor				= models.ForeignKey(User, related_name="emisor")
	receptor 			= models.ForeignKey(User, related_name="receptor") 
	fecha_creacion		= models.DateField(default=datetime.datetime.now().date())
	fecha_vencimiento	= models.DateField()
	mensaje				= models.CharField(max_length=150)
	status 				= models.CharField(max_length=3, default='P')
	habilitado 			= models.BooleanField(default=True)
	
	def class_alert(self):
		hoy = datetime.datetime.today().date()
		diff = (self.fecha_vencimiento-hoy).days

		if diff >= 7: 
			return "list-group-item-success"
		elif diff < 7 and diff >= 4:
			return "list-group-item-warning"
		elif diff < 4:
			return "list-group-item-danger"
		else:
			return "list-group-item-info"

	def status_status(self):
		return dict(self.STATUS).get(self.status, '---')


class HomologacionDeDocs(models.Model):

	REPOSITORIO = settings.HOMOLOG_DOCS 

	class Meta:
		verbose_name_plural = 'Homologación de Docs.'

	nombre  = models.CharField(max_length=150, blank=False)
	archivo = models.FileField(upload_to=get_upload_path, null=False)
	fecha 	= models.DateField(default=datetime.datetime.now().date())

	def archivo_liga(self):
		try:
			return self.archivo.url
		except ValueError:
			return self.archivo