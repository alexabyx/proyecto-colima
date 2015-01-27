from django.contrib import admin
 
from inicio.models import *
# Register your models here.

class PersonalAdmin(admin.ModelAdmin):
	list_display=('rfc','credencial_elector','nombre','apellido_paterno','apellido_materno','siglas_nombre','genero','direccion','telefono','no_seguro','fecha_ingreso','puesto','turno','tipo_plaza','tipo_pago','monto','numero_oficio_contrato','dias_trabajo_al_mes','fecha_vencimiento_contrato','fecha_baja','motivo_baja','responsable',)

class ConveniosAdmin (admin.ModelAdmin):
	list_display=('numero','proyecto','numero_universidad','siglas_universidad','archivo','fecha_creacion','encargado',)

class ContratosAdmin(admin.ModelAdmin):
	list_display=('numero_oficio','proyecto','fecha_creacion','encargado','cliente','archivo',)


class ProyectoAdmin(admin.ModelAdmin):
	list_display=('mombre','siglas','fecha_inicio','status','avance',)



class AnexosTecnicosAdmin(admin.ModelAdmin):
	list_display=('numero_oficio','proyecto','tipo','nombre','siglas','porcentaje','fecha_creacion','archivo',)


class EntregablesAdmin(admin.ModelAdmin):
	list_display=('contrato','proyecto','responsable','nombre','fecha_creacion','archivo',)


class DetallesEntregablesAdmin(admin.ModelAdmin):
	list_display=('entregable','responsable','numero','nombre','siglas','fecha_creacion','archivo',)


admin.site.register(AnexosTecnicos, AnexosTecnicosAdmin)
admin.site.register(Proyectos, ProyectoAdmin)
admin.site.register(Convenios, ConveniosAdmin)
admin.site.register(Contratos, ContratosAdmin)
admin.site.register(DetallesEntregables, DetallesEntregablesAdmin)
admin.site.register(Entregables, EntregablesAdmin)
#admin.site.register(proyecto_has_personal, proyecto_has_personalAdmin)
admin.site.register(Personal, PersonalAdmin)