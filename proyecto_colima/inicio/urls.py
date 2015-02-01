from django.conf.urls import patterns, include, url
from inicio.views import *


urlpatterns = patterns('proyecto_colima.inicio',
    # Examples:
    # url(r'^$', 'proyecto_colima.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', inicio, name="login"),
    url(r'^administrar_usuarios/$', administrar_usuarios, name="administrar-usuarios"),

    url(r'^registrar_proyecto/$', registrar_proyecto, name="registrar-proyecto"),
    url(r'^registrar_factura/$', registrar_factura, name="registrar-factura"),
    url(r'^registrar_anexostecnicos/$', registrar_anexostecnicos, name = "registrar-anexostecnicos"),
    url(r'^registrar_contratos/$', registrar_contratos, name="registrar-contratos"),
    url(r'^registrar_convenios/$', registrar_convenios, name="registrar-convenios"),
    url(r'^registrar_propuestas/$', registrar_propuestas, name="registrar-propuestas"),
    url(r'^registrar_empresa/$', registrar_empresa, name="registrar-empresa"),
    url(r'^registrar_entregable/$', registrar_entregable, name="registrar-entregable"),
    url(r'^registrar_personal/$', registrar_personal, name="registrar-personal")
    )