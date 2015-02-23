from django.contrib import admin
from inicio.models import *

class DetallePagoEmpleadoAdminInline(admin.TabularInline):
	model = DetallePagoEmpleado
	extra = 2
 
class PersonalAdmin(admin.ModelAdmin):
	list_display = ('rfc',)
	list_filter = ['turno', 'genero', 'tipo_pago']
	search_fields = ['rfc', 'nombre', 'apellido_paterno', 'apellido_materno']
	inlines = [DetallePagoEmpleadoAdminInline]



class DetalleDocumentoResponsivaAdmin(admin.ModelAdmin):
	list_display = ('personal', )


class ProyectosAdmin(admin.ModelAdmin):
	list_display = ('siglas', 'fecha_inicio', 'avance')
	list_filter = ('responsable',)

class AnexosTecnicosAdmin(admin.ModelAdmin):
	list_display = ( 'nombre', 'siglas','numero_oficio')
	list_filter = ('nombre','numero_oficio',)


class ConveniosAdmin(admin.ModelAdmin):
	list_display = ('numero', 'proyecto', 'encargado')
	list_filter = ('fecha_creacion',)


class ContratosAdmin(admin.ModelAdmin):
	list_display = ('numero_oficio', 'proyecto', 'encargado')


class DetallesEntregablesAdminInline(admin.TabularInline):
	model = DetallesEntregables
	extra = 2

class EntregablesAdmin(admin.ModelAdmin):
	list_display = ( 'proyecto', 'responsable')
	list_filter = ('total',)

	inlines = [DetallesEntregablesAdminInline]

class EntidadesAdmin(admin.ModelAdmin):
	list_display = ('nombre',)

class DetallesFacturasAdminInline(admin.TabularInline):
	model = DetallesFacturas
	extra = 2

class FacturasAdmin(admin.ModelAdmin):
	list_display = ('contrato', 'responsable', 'tipo', 'nombre', 'siglas')
	list_filter = ('tipo',)

	inlines = [DetallesFacturasAdminInline]

class PropuestasAdmin(admin.ModelAdmin):
	list_display = ('proyecto', 'responsable')
	list_filter = ('fecha_creacion', 'numero_oficio',)

class DetallesDocumentosGeneralesAdminInline(admin.TabularInline):
	model = DetallesDocumentosGenerales
	extra = 2

class DocumentosGeneralesAdmin(admin.ModelAdmin):
	list_display = ( 'proyecto', 'clave')
	list_filter = ('fecha_creacion',)

	inlines = [DetallesDocumentosGeneralesAdminInline]


admin.site.register(Personal, PersonalAdmin)
admin.site.register(Clientes)
#admin.site.register(DetallePagoEmpleado,DetallePagoEmpleadoAdmin)
admin.site.register(DetalleDocumentoResponsiva, DetalleDocumentoResponsivaAdmin)
admin.site.register(Proyectos, ProyectosAdmin)
admin.site.register(AnexosTecnicos, AnexosTecnicosAdmin)
admin.site.register(Convenios, ConveniosAdmin)
admin.site.register(Contratos, ContratosAdmin)
admin.site.register(Entregables, EntregablesAdmin)
admin.site.register(Entidades, EntidadesAdmin)
admin.site.register(Facturas, FacturasAdmin)
admin.site.register(Propuestas, PropuestasAdmin)
admin.site.register(DocumentosGenerales, DocumentosGeneralesAdmin)

