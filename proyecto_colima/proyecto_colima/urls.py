from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'inicio.views_login.login_web', name="login_web"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^administracion/', include('inicio.urls', namespace="administracion")),
    )
