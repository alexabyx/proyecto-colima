from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'inicio.views_login.login_web', name="login_web"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^administracion/', include('inicio.urls', namespace="administracion")),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    )
