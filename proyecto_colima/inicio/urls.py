from django.conf.urls import patterns, include, url
from inicio.views import *


urlpatterns = patterns('proyecto_colima.inicio',
    # Examples:
    # url(r'^$', 'proyecto_colima.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', inicio, name="login"),
    url(r'^administrar_usuarios/$', administrar_usuarios, name="administrar-usuarios"),

    )

