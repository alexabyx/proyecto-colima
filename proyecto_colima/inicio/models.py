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
	responsable = models.ManyToManyField(max_length=45)
	fecha_inicio = models.DateField(default=datetime.datetime.now())
	status = models.CharField(max_length=45)
	avance = models.CharField(max_length=45)
	personal = models.ManyToManyField(Personal)

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
	fecha=models.DateField()
	responsable=models.CharField(max_length=45)
	telefono=models.CharField(max_length=45)


class Contratos(models.Model):
	numero_oficio_contrato=models.CharField(max_length=45)
	nombre_dependencia=models.CharField(max_length=45)
	archivo=models.FileField(upload_to=get_upload_path, blank=True)
	fecha_creacion=models.DateField()
	responsable=models.CharField(max_length=45)
	telefono=models.CharField(max_length=45)
	siglas_responsable=models.CharField(max_length=45)
	proyectos=models.ForeignKey(Proyectos)

class Entregables(models.Model):
	nombre_entregable=models.CharField(max_length=45)
	archivo=models.FileField(upload_to=get_upload_path, blank=True)
	fecha_creacion=models.DateField()
	responsable=models.CharField(max_length=45)
	telefono=models.CharField(max_length=45)
	total=models.IntegerField()
	proyecto=models.ForeignKey(Proyectos)

class Detalle_entregable(models.Model):
	entregable = models.ForeignKey(Entregables)
	numero_entregable=models.IntegerField()
	siglas_entregables=models.CharField(max_length=45)
	nombre_entregable=models.CharField(max_length=45)
	nombre_responsable=models.CharField(max_length=45)
	siglas_responsable=models.CharField(max_length=45)
	archivo=models.FileField(upload_to=get_upload_path, blank=True)
	fecha_creacion=models.DateField()
	telefono=models.CharField(max_length=45)

class Documentos_Generales(models.Model):
	clave_identificacion=models.CharField(max_length=45)
	nombre_empresa=models.CharField(max_length=45)
	nombre_universidad=models.CharField(max_length=45)
	siglas_universidad=models.CharField(max_length=45)
	fecha=models.DateField()
	telefono=models.CharField(max_length=45)
	responsable=models.CharField(max_length=45)
	siglas_responsable=models.CharField(max_length=45)
	proyectos=models.ForeignKey(Proyectos)

class Empresa(models.Model):
	empresacol=models.CharField(max_length=45)

class Facturas(models.Model):
	numero_oficio_contrato=models.CharField(max_length=45)
	nombre_dependencia=models.CharField(max_length=45)
	siglas_dependencia=models.CharField(max_length=45)
	nombre_empresa=models.CharField(max_length=45)
	siglas_empresa=models.CharField(max_length=45)
	nombre_universidad=models.CharField(max_length=45)
	nombre_responsable=models.CharField(max_length=45)
	siglas_responsable=models.CharField(max_length=45)
	numero_factura=models.IntegerField()
	fecha_factura=models.DateField()
	folio_venta=models.CharField(max_length=45)
	rfc=models.CharField(max_length=45)
	direccion=models.CharField(max_length=45)
	descripcion_producto=models.CharField(max_length=45)
	cantidad_producto=models.IntegerField()
	subtotal=models.IntegerField()
	iva=models.IntegerField()
	total=models.IntegerField()
	total_con_letra=models.CharField(max_length=45)
	pagada=models.BooleanField(default=False)
	archivo_factura=models.FileField(upload_to=get_upload_path, blank=True)
	responsable=models.CharField(max_length=45)
	telefono=models.CharField(max_length=45)
	siglas_responsable=models.CharField(max_length=45)
	proyectos=models.ForeignKey(Proyectos)

class Propuesta(models.Model):
	Nombre_Dependencia=models.CharField(max_length=45)
	Siglas_Dependencia=models.CharField(max_length=45)
	Nombre_Universidad=models.CharField(max_length=45)
	fecha_creacion=models.DateField()
	Telefono=models.IntegerField(max_length=12)
	siglas_responsable=models.CharField(max_length=45)
	proyectos =models.ForeignKey(Proyectos)

class Detalles_documentos_generales(models.Model):
	total=models.CharField(max_length=45)
	numero_documento=models.IntegerField()
	nombre_documento=models.CharField(max_length=45)
	siglas_documento=models.CharField(max_length=45)
	nombre_responsable=models.CharField(max_length=45)
	siglas_responsable=models.CharField(max_length=45)
	archivo=models.CharField(max_length=45)
	fecha=models.DateField()
	Telefono=models.IntegerField(max_length=12)
	documentos_generales =models.ForeignKey(Documentos_Generales)