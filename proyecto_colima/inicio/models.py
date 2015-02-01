#-*- coding:utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

def get_upload_path(instance, filename):
    return os.path.join(filename)

#PERSONAL DE DESARROLLO
class Personal(models.Model):
	SEXO_OPCIONES = (('H', 'Hombre'), ('M', 'Mujer'), )
	TIPO_PAGO = (('S', 'Semanal'), ('Q', 'Quincenal'), ('M', 'Mensual'),)

	rfc = models.CharField(max_length=45)
	credencial_elector = models.FileField(upload_to = get_upload_path, blank=True)
	nombre = models.CharField(max_length=45)
	apellido_paterno = models.CharField(max_length=45)
	apellido_materno = models.CharField(max_length=45)
	siglas_nombre = models.CharField(max_length=45, null=True)
	genero = models.CharField(max_length=1, choices=SEXO_OPCIONES)
	direccion = models.CharField(max_length=45)
	telefono = models.CharField(max_length=45)
	no_seguro = models.CharField(max_length=45)
	fecha_ingreso = models.DateField(default=datetime.datetime.now())
	puesto = models.CharField(max_length=45)
	turno = models.CharField(max_length=45)
	tipo_plaza = models.CharField(max_length=45)
	tipo_pago = models.CharField(max_length=1, choices=TIPO_PAGO)
	monto = models.IntegerField()	
	numero_oficio_contrato = models.CharField(max_length=45)
	dias_trabajo_al_mes = models.IntegerField()
	
	fecha_vencimiento_contrato = models.DateField()
	fecha_baja = models.DateField()
	motivo_baja = models.CharField(max_length=45)

	responsable = models.CharField(max_length=45)

class DetallePagoEmpleado(models.Model):
	personal = models.ForeignKey(Personal)
	archivo_documento_de_pago = models.FileField(upload_to = get_upload_path, blank=True)	

class DetalleDocumentoResponsiva(models.Model):
	personal = models.ForeignKey(Personal)
	archivo_documento_responsiva = models.FileField(upload_to = get_upload_path, blank=True)

class Proyectos(models.Model):
	mombre = models.CharField(max_length=45, null=False)
	siglas = models.CharField(max_length=45)
	responsable = models.ManyToManyField(Personal)
	fecha_inicio = models.DateField(default=datetime.datetime.now())
	status = models.CharField(max_length=45)
	avance = models.CharField(max_length=45)

class AnexosTecnicos(models.Model):
	TIPOS = (('D', 'Dependencia'), ('E', 'Empresa'), ('U', 'Universidad'))

	numero_oficio = models.IntegerField(blank=False)	
	proyecto = models.ForeignKey(Proyectos)

	tipo = models.CharField(max_length=1, choices=TIPOS)
	nombre = models.CharField(max_length=45)
	siglas = models.CharField(max_length=45)
	porcentaje = models.IntegerField()
	fecha_creacion=models.DateField(default=datetime.datetime.now())
	archivo=models.FileField(upload_to = get_upload_path, blank=True)

class Convenios (models.Model):
	numero=models.CharField(max_length=45)
	proyecto=models.ForeignKey(Proyectos)

	numero_universidad=models.CharField(max_length=45)
	siglas_universidad=models.CharField(max_length=45)

	archivo=models.FileField(upload_to=get_upload_path, blank=True)
	fecha_creacion=models.DateField(default=datetime.datetime.now())

	encargado = models.ForeignKey(Personal)


class Contratos(models.Model):
	numero_oficio =models.CharField(max_length=45)
	proyecto=models.ForeignKey(Proyectos)
	fecha_creacion=models.DateField(default=datetime.datetime.now())
	encargado=models.ForeignKey(Personal)
	cliente=models.CharField(max_length=45, help_text = "Nombre de la dependencia")
	archivo=models.FileField(upload_to=get_upload_path, blank=True)

class Entregables(models.Model):
	contrato = models.ForeignKey(Contratos)
	proyecto = models.ForeignKey(Proyectos)
	responsable = models.ForeignKey(Personal)

	nombre = models.CharField(max_length=45)
	fecha_creacion=models.DateField(default=datetime.datetime.now())
	archivo = models.FileField(upload_to=get_upload_path, blank=True)
	
	# @property
	# def total(self):
	# 	return len(Detalle_entregable.objects.filter(entregable=self))

class DetallesEntregables(models.Model):
	entregable = models.ForeignKey(Entregables)
	responsable = models.ForeignKey(Personal)
	numero = models.IntegerField()
	nombre =models.CharField(max_length=45)
	siglas = models.CharField(max_length=45)
	fecha_creacion=models.DateField(default=datetime.datetime.now())
	archivo=models.FileField(upload_to=get_upload_path, blank=True)

class Empresas(models.Model):
	nombre=models.CharField(max_length=45)

class Facturas(models.Model):
	TIPOS = (('D', 'Dependencia'), ('E', 'Empresa'), ('U', 'Universidad'))
	
	contrato = models.ForeignKey(Contratos)
	responsable = models.ForeignKey(Personal)

	tipo = models.CharField(max_length=1, choices=TIPOS)
	nombre=models.CharField(max_length=45)
	siglas=models.CharField(max_length=45)

	numero_factura=models.IntegerField(unique=True)
	fecha_factura = models.DateField(default=datetime.datetime.now())
	folio_venta=models.CharField(max_length=45)

	rfc=models.CharField(max_length=45, help_text="RFC persona fisica/moral")
	direccion=models.CharField(max_length=45, help_text=u"dirección persona fisica/moral")

	subtotal=models.IntegerField()
	iva=models.IntegerField()
	total_con_numero = models.IntegerField()
	total_con_letra = models.CharField(max_length=45)
	pagada=models.BooleanField(default=False)
	archivo=models.FileField(upload_to=get_upload_path, blank=False)

class DetallesFacturas(models.Model):
	factura = models.ForeignKey(Facturas) 
	descripcion = models.CharField(max_length=45)
	cantidad = models.IntegerField()

class Propuestas(models.Model):
	TIPOS = (('E1', 'Empresa 46%'), ('E2', 'Empresa 49%'), ('U1', 'Universidad'))

	numero_oficio = models.CharField(max_length=45)
	proyecto = models.ForeignKey(Proyectos)
	responsable = models.ForeignKey(Personal)

	nombre_dependencia=models.CharField(max_length=45)
	siglas_dependencia=models.CharField(max_length=45)

	tipo = models.CharField(max_length=2, choices=TIPOS)
	nombre =models.CharField(max_length=45)
	siglas=models.CharField(max_length=45)

	fecha_creacion=models.DateField(default=datetime.datetime.now())

class DocumentosGenerales(models.Model):
	TIPOS = (('D', 'Dependencia'), ('E', 'Empresa'), ('U', 'Universidad'))
	proyecto=models.ForeignKey(Proyectos)
	responsable=models.ForeignKey(Personal)
	clave =models.CharField(max_length=45)
	tipo = models.CharField(max_length=1, choices=TIPOS)
	nombre =models.CharField(max_length=45)
	siglas=models.CharField(max_length=45)
	fecha_creacion=models.DateField(default=datetime.datetime.now())

class DetallesDocumentosGenerales(models.Model):
	documentos_generales =models.ForeignKey(DocumentosGenerales)
	responsable=models.ForeignKey(Personal)
	numero =models.IntegerField()
	nombre =models.CharField(max_length=45)
	siglas =models.CharField(max_length=45)
	archivo=models.CharField(max_length=45)
	fecha_creacion=models.DateField(default=datetime.datetime.now())
