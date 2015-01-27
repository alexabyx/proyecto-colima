from django.contrib import admin
from inicio.models import *
 
class PersonalAdmin(admin.ModelAdmin):
	list_display = ('rfc',)
	list_filter = ['turno', 'genero', 'tipo_pago']
	search_fields = ['rfc', 'nombre', 'apellido_paterno', 'apellido_materno']


class DetallePagoEmpleadoAdmin(admin.ModelAdmin):
	list_display = ('personal',)

class DetalleDocumentoResponsivaAdmin(admin.ModelAdmin):
	list_display = ('personal', )


class ProyectosAdmin(admin.ModelAdmin):
	list_display = ('siglas', 'fecha_inicio', 'avance')
	list_filter = ('responsable', 'status')

class AnexosTecnicosAdmin(admin.ModelAdmin):
	list_display = ('tipo', 'nombre', 'siglas')
	list_filter = ('tipo',)


class ConveniosAdmin(admin.ModelAdmin):
	list_display = ('numero', 'proyecto', 'encargado')
	list_filter = ('fecha_creacion',)


class ContratosAdmin(admin.ModelAdmin):
	list_display = ('numero_oficio', 'proyecto', 'encargado')


class EntregablesAdmin(admin.ModelAdmin):
	list_display = ('contrato', 'proyecto', 'responsable')
	list_filter = ('fecha_creacion',)

class DetallesEntregablesAdmin(admin.ModelAdmin):
	list_display = ('entregable', 'responsable','numero')
	list_filter = ('fecha_creacion',)

class EmpresasAdmin(admin.ModelAdmin):
	list_display = ('nombre',)

class FacturasAdmin(admin.ModelAdmin):
	list_display = ('contrato', 'responsable', 'tipo', 'nombre', 'siglas')
	list_filter = ('tipo',)

class DetallesFacturasAdmin(admin.ModelAdmin):
	list_display = ('factura', 'descripcion', 'cantidad')

class PropuestasAdmin(admin.ModelAdmin):
	list_display = ('proyecto', 'responsable', 'tipo', 'nombre', 'siglas')
	list_filter = ('fecha_creacion', 'tipo',)


class DocumentosGeneralesAdmin(admin.ModelAdmin):
	list_display = ('tipo', 'proyecto', 'responsable', 'clave')
	list_filter = ('fecha_creacion',)


class DetallesDocumentosGeneralesAdmin(admin.ModelAdmin):
	list_display= ('documentos_generales', 'responsable', 'numero', 'nombre')
	list_filter=('fecha_creacion',)

admin.site.register(Personal, PersonalAdmin)
admin.site.register(DetallePagoEmpleado,DetallePagoEmpleadoAdmin)
admin.site.register(DetalleDocumentoResponsiva, DetalleDocumentoResponsivaAdmin)
admin.site.register(Proyectos, ProyectosAdmin)
admin.site.register(AnexosTecnicos, AnexosTecnicosAdmin)
admin.site.register(Convenios, ConveniosAdmin)
admin.site.register(Contratos, ContratosAdmin)
admin.site.register(Entregables, EntregablesAdmin)
admin.site.register(DetallesEntregables, DetallesEntregablesAdmin)
admin.site.register(Empresas, EmpresasAdmin)
admin.site.register(Facturas, FacturasAdmin)
admin.site.register(DetallesFacturas, DetallesFacturasAdmin)
admin.site.register(Propuestas, PropuestasAdmin)
admin.site.register(DocumentosGenerales, DocumentosGeneralesAdmin)
admin.site.register(DetallesDocumentosGenerales, DetallesDocumentosGeneralesAdmin)