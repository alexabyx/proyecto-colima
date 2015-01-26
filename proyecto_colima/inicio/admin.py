from django.contrib import admin
from inicio.models import AreaAdministrativa

# Register your models here.


class AreaAdministrativaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    list_filter = ['nombre']
    search_fields = ['nombre', 'usuario']




admin.site.register(AreaAdministrativa, AreaAdministrativaAdmin)

 