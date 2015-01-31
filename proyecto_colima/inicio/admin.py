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


class DetallesEntregablesAdminInline(admin.TabularInline):
	model = DetallesEntregables
	extra = 2

class EntregablesAdmin(admin.ModelAdmin):
	list_display = ('contrato', 'proyecto', 'responsable')
	list_filter = ('fecha_creacion',)

	inlines = [DetallesEntregablesAdminInline]

class EmpresasAdmin(admin.ModelAdmin):
	list_display = ('nombre',)

class DetallesFacturasAdminInline(admin.TabularInline):
	model = DetallesFacturas
	extra = 2

class FacturasAdmin(admin.ModelAdmin):
	list_display = ('contrato', 'responsable', 'tipo', 'nombre', 'siglas')
	list_filter = ('tipo',)

	inlines = [DetallesFacturasAdminInline]

class PropuestasAdmin(admin.ModelAdmin):
	list_display = ('proyecto', 'responsable', 'tipo', 'nombre', 'siglas')
	list_filter = ('fecha_creacion', 'tipo',)

class DetallesDocumentosGeneralesAdminInline(admin.TabularInline):
	model = DetallesDocumentosGenerales
	extra = 2

class DocumentosGeneralesAdmin(admin.ModelAdmin):
	list_display = ('tipo', 'proyecto', 'responsable', 'clave')
	list_filter = ('fecha_creacion',)

	inlines = [DetallesDocumentosGeneralesAdminInline]


admin.site.register(Personal, PersonalAdmin)
admin.site.register(DetallePagoEmpleado,DetallePagoEmpleadoAdmin)
admin.site.register(DetalleDocumentoResponsiva, DetalleDocumentoResponsivaAdmin)
admin.site.register(Proyectos, ProyectosAdmin)
admin.site.register(AnexosTecnicos, AnexosTecnicosAdmin)
admin.site.register(Convenios, ConveniosAdmin)
admin.site.register(Contratos, ContratosAdmin)
admin.site.register(Entregables, EntregablesAdmin)
admin.site.register(Empresas, EmpresasAdmin)
admin.site.register(Facturas, FacturasAdmin)
admin.site.register(Propuestas, PropuestasAdmin)
admin.site.register(DocumentosGenerales, DocumentosGeneralesAdmin)


# class PersonalAdmin(admin.ModelAdmin):
# 	list_display=('rfc','credencial_elector','nombre','apellido_paterno','apellido_materno','siglas_nombre','genero','direccion','telefono','no_seguro','fecha_ingreso','puesto','turno','tipo_plaza','tipo_pago','monto','numero_oficio_contrato','dias_trabajo_al_mes','fecha_vencimiento_contrato','fecha_baja','motivo_baja','responsable',)

# class ConveniosAdmin (admin.ModelAdmin):
# 	list_display=('numero','proyecto','numero_universidad','siglas_universidad','archivo','fecha_creacion','encargado',)

# class ContratosAdmin(admin.ModelAdmin):
# 	list_display=('numero_oficio','proyecto','fecha_creacion','encargado','cliente','archivo',)


# class ProyectoAdmin(admin.ModelAdmin):
# 	list_display=('mombre','siglas','fecha_inicio','status','avance',)



# class AnexosTecnicosAdmin(admin.ModelAdmin):
# 	list_display=('numero_oficio','proyecto','tipo','nombre','siglas','porcentaje','fecha_creacion','archivo',)


# class EntregablesAdmin(admin.ModelAdmin):
# 	list_display=('contrato','proyecto','responsable','nombre','fecha_creacion','archivo',)


# class DetallesEntregablesAdmin(admin.ModelAdmin):
# 	list_display=('entregable','responsable','numero','nombre','siglas','fecha_creacion','archivo',)


# admin.site.register(AnexosTecnicos, AnexosTecnicosAdmin)
# admin.site.register(Proyectos, ProyectoAdmin)
# admin.site.register(Convenios, ConveniosAdmin)
# admin.site.register(Contratos, ContratosAdmin)
# admin.site.register(DetallesEntregables, DetallesEntregablesAdmin)
# admin.site.register(Entregables, EntregablesAdmin)
# #admin.site.register(proyecto_has_personal, proyecto_has_personalAdmin)
# admin.site.register(Personal, PersonalAdmin)

