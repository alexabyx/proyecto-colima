from django.contrib import admin
from inicio.models import *

#<=======================PERSONAL=======================>
class DetallePagoEmpleadoAdminInline(admin.TabularInline):
	model = DetallePagoEmpleado
	extra = 1

class DetalleDocumentoResponsivaAdminInline(admin.TabularInline):
	model = DetalleDocumentoResponsiva
	extra = 1

class PersonalAdmin(admin.ModelAdmin):
	list_display = ('rfc',)
	list_filter = ['turno', 'genero', 'tipo_pago']
	search_fields = ['rfc', 'nombre', 'apellido_paterno', 'apellido_materno']
	inlines = [DetallePagoEmpleadoAdminInline, DetalleDocumentoResponsivaAdminInline]

#<=======================PROYECTOS=======================>
class AnexosTecnicosAdminInline(admin.TabularInline):
	model = AnexosTecnicos
	extra = 1

class ProyectosAdmin(admin.ModelAdmin):
	list_display = ('siglas', 'fecha_inicio', 'avance')
	list_filter = ('responsable',)

	inlines = [AnexosTecnicosAdminInline]

#<=======================CONVENIOS=======================>
class ConveniosAdmin(admin.ModelAdmin):
	list_display = ('numero', 'proyecto', 'encargado')
	list_filter = ('fecha_creacion',)

#<=======================CONTRATOS=======================>
class ContratosAdmin(admin.ModelAdmin):
	list_display = ('numero_oficio', 'proyecto', 'encargado')

#<=======================ENTREGABLES=======================>
class DetallesEntregablesAdminInline(admin.TabularInline):
	model = DetallesEntregables
	extra = 1

class EntregablesAdmin(admin.ModelAdmin):
	list_display = ( 'proyecto', 'responsable')
	list_filter = ('total',)

	inlines = [DetallesEntregablesAdminInline]

#<=======================FACTURAS=======================>
class DetallesFacturasAdminInline(admin.TabularInline):
	model = DetallesFacturas
	extra = 1

class FacturasAdmin(admin.ModelAdmin):
	list_display = ('contrato', 'responsable')
	inlines = [DetallesFacturasAdminInline]

#<=======================PROPUESTAS=======================>
class PropuestasAdmin(admin.ModelAdmin):
	list_display = ('proyecto', 'responsable')
	list_filter = ('fecha_creacion', 'numero_oficio',)

#<=======================DOCS. GENERALES=======================>
class DetallesDocumentosGeneralesAdminInline(admin.TabularInline):
	model = DetallesDocumentosGenerales
	extra = 1

class DocumentosGeneralesAdmin(admin.ModelAdmin):
	list_display = ( 'entidad', 'clave')
	list_filter = ('fecha_creacion',)

	inlines = [DetallesDocumentosGeneralesAdminInline]

#<=======================ENTIDADES=======================>
class EntidadProyectoAdminInline(admin.TabularInline):
	model = EntidadProyecto
	extra = 1

class EntidadesAdmin(admin.ModelAdmin):
	list_display = ('nombre',)

#<=======================PAGOS=======================>
class DetallePagosAdminInline(admin.TabularInline):
	model = DetallePagos
	extra = 1 

class PagosAdmin(admin.ModelAdmin):
	list_display = ('proyecto', 'monto_total', 'fecha_pago')
	list_filter = ('proyecto',)

	inlines = [DetallePagosAdminInline]



admin.site.register(Personal, PersonalAdmin)
admin.site.register(DetallePagoEmpleado)
admin.site.register(DetalleDocumentoResponsiva)

admin.site.register(Clientes)
admin.site.register(Proyectos, ProyectosAdmin)
admin.site.register(AnexosTecnicos)


admin.site.register(Convenios, ConveniosAdmin)
admin.site.register(Contratos, ContratosAdmin)

admin.site.register(Entregables, EntregablesAdmin)
admin.site.register(DetallesEntregables)

admin.site.register(Facturas, FacturasAdmin)
admin.site.register(DetallesFacturas)

admin.site.register(Propuestas, PropuestasAdmin)

admin.site.register(DocumentosGenerales, DocumentosGeneralesAdmin)
admin.site.register(DetallesDocumentosGenerales)

admin.site.register(Entidades, EntidadesAdmin)
admin.site.register(EntidadProyecto)

admin.site.register(Pagos, PagosAdmin)
admin.site.register(DetallePagos)

admin.site.register(Alarmas)
admin.site.register(HomologacionDeDocs)