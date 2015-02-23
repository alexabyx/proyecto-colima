from django.conf.urls import patterns, include, url
from inicio.views import *
from inicio.views_login import *
from inicio.views_modal import *

urlpatterns = patterns('proyecto_colima.inicio',

    #URL LOGOUT Y ADMINISTRACION
    url(r'^$', administracion, name="index"),
    url(r'^logout/$', logout_web, name="logout-web"),

    #MODALES
    url(r'^modal_ok/$', modal_ok, name="modal-ok"),
    url(r'^modal_aviso/$', modal_aviso, name="modal-aviso"),
    url(r'^modal_error/$', modal_error, name="modal-error"),
    
    #PERSONAL
    url(r'^personal/$', personal, name="personal"),
    url(r'^detalle_personal/(?P<pk>\d+)/$', PersonalDetailView.as_view(), name="detalle-personal"),
    url(r'^editar_personal/(?P<pk>\d+)/$', editar_personal, name="editar-personal"),
    url(r'^eliminar_personal/$', eliminar_personal, name='eliminar-personal'),
    url(r'^crear_personal/$', crear_personal, name="crear-personal"),

    #PROYECTOS
    url(r'^proyectos/$', proyectos, name="proyectos"),
    url(r'^detalle_proyecto/(?P<pk>\d+)/$', ProyectoDetailView.as_view(), name="detalle-proyecto"),
    url(r'^editar_proyecto/(?P<pk>\d+)/$', editar_proyecto, name="editar-proyecto"),
    url(r'^editar_proyecto_1/(?P<pk>\d+)/$', editar_proyecto_1, name="editar-proyecto-1"),
    url(r'^eliminar_proyecto/$', eliminar_proyecto, name='eliminar-proyecto'),
    url(r'^crear_proyecto/$', crear_proyecto, name="crear-proyecto"),


    #ENTREGABLES
    url(r'^entregables/$', entregables, name="entregables"),
    url(r'^detalle_entregable/(?P<pk>\d+)/$', EntregableDetailView.as_view(), name="detalle-proyecto"),
    url(r'^editar_entregable/(?P<pk>\d+)/$', editar_entregable, name="editar-entregable"),
    url(r'^editar_entregable_1/(?P<pk>\d+)/$', editar_entregable_1, name="editar-entregable-1"),
    url(r'^eliminar_entregable/$', eliminar_entregable, name='eliminar-entregable'),
    url(r'^crear_entregable/$', crear_entregable, name="crear-entregable"),
    
    #DETALLES ENTREGABLES
    url(r'^detalle_entregables/$', detalle_entregables, name="detalle-entregables"),
    url(r'^detalle_detalle_entregable/(?P<pk>\d+)/$', DetalleEntregableDetailView.as_view(), name="detalle-detalle-proyecto"),
    url(r'^editar_detalle_entregable/(?P<pk>\d+)/$', editar_detalle_entregable, name="editar-detalle-entregable"),
    url(r'^editar_detalle_entregable_1/(?P<pk>\d+)/$', editar_detalle_entregable_1, name="editar-detalle-entregable-1"),
    url(r'^crear_detalle_entregable/$', crear_detalle_entregable, name="crear-detalle-entregable"),

    #FACTURAS
    url(r'^facturas/$', facturas, name="facturas"),
    url(r'^detalle_factura/(?P<pk>\d+)/$', FacturaDetailView.as_view(), name="detalle-factura"),
    url(r'^editar_factura/(?P<pk>\d+)/$', editar_factura, name="editar-factura"),
    url(r'^editar_factura_1/(?P<pk>\d+)/$', editar_factura_1, name="editar-factura-1"),
    url(r'^crear_factura/$', crear_factura, name="crear-factura"),

    #DETALLES DE FACTURAS
    url(r'^detalle_facturas/$', detalle_facturas, name="detalle-facturas"),
    url(r'^detalle_detalle_factura/(?P<pk>\d+)/$', DetalleFacturaDetailView.as_view(), name="detalle-detalle-factura"),
    url(r'^editar_detalle_factura/(?P<pk>\d+)/$', editar_detalle_factura, name="editar-detalle-factura"),
    url(r'^editar_detalle_factura_1/(?P<pk>\d+)/$', editar_detalle_factura_1, name="editar-detalle-factura-1"),
    url(r'^crear_detalle_factura/$', crear_detalle_factura, name="crear-detalle-factura"),

    #ANEXOS TECNICOS
    url(r'^anexostecnicos/$', anexostecnicos, name = "anexostecnicos"),
    url(r'^detalle_anexotecnico/(?P<pk>\d+)/$', AnexotecnicoDetailView.as_view(), name="detalle-anexotecnico"),
    url(r'^editar_anexotecnico/(?P<pk>\d+)/$', editar_anexotecnico, name="editar-anexotecnico"),
    url(r'^editar_anexotecnico_1/(?P<pk>\d+)/$', editar_anexotecnico_1, name="editar-anexotecnico-1"),
    url(r'^eliminar_anexotecnico/$', eliminar_anexotecnico, name='eliminar-anexotecnico'),
    url(r'^crear_anexotecnico/$', crear_anexotecnico, name="crear-anexotecnico"),

    #CONTRATOS
    url(r'^contratos/$', contratos, name="contratos"),
    url(r'^detalle_contrato/(?P<pk>\d+)/$', ContratoDetailView.as_view(), name="detalle-contrato"),
    url(r'^editar_contrato/(?P<pk>\d+)/$', editar_contrato, name="editar-contrato"),
    url(r'^editar_contrato_1/(?P<pk>\d+)/$', editar_contrato_1, name="editar-contrato-1"),
    url(r'^eliminar_contrato/$', eliminar_contrato, name='eliminar-contrato'),
    url(r'^crear_contrato/$', crear_contrato, name="crear-contrato"),

    #CONVENIOS
    url(r'^convenios/$', convenios, name="convenios"),
    url(r'^detalle_convenio/(?P<pk>\d+)/$', ConvenioDetailView.as_view(), name="detalle-convenio"),
    url(r'^editar_convenio/(?P<pk>\d+)/$', editar_convenio, name="editar-convenio"),
    url(r'^editar_convenio_1/(?P<pk>\d+)/$', editar_convenio_1, name="editar-convenio-1"),
    url(r'^eliminar_convenio/$', eliminar_convenio, name='eliminar-convenio'),
    url(r'^crear_convenio/$', crear_convenio, name="crear-convenio"),

    #PROPUESTAS
    url(r'^propuestas/$', propuestas, name = "propuestas"),
    url(r'^detalle_propuesta/(?P<pk>\d+)/$', PropuestaDetailView.as_view(), name="detalle-propuesta"),
    url(r'^editar_propuesta/(?P<pk>\d+)/$', editar_propuesta, name="editar-propuesta"),
    url(r'^editar_propuesta_1/(?P<pk>\d+)/$', editar_propuesta_1, name="editar-propuesta-1"),
    url(r'^eliminar_propuesta/$', eliminar_propuesta, name='eliminar-propuesta'),
    url(r'^crear_propuesta/$', crear_propuesta, name="crear-propuesta"),

    #CLIENTES
    url(r'^clientes/$', clientes, name="clientes"),
    url(r'^detalle_cliente/(?P<pk>\d+)/$', ClienteDetailView.as_view(), name="detalle-cliente"),
    url(r'^editar_cliente/(?P<pk>\d+)/$', editar_cliente, name="editar-cliente"),
    url(r'^eliminar_cliente/$', eliminar_cliente, name='eliminar-cliente'),
    url(r'^crear_cliente/$', crear_cliente, name="crear-cliente"),

    #ENTIDADES
    url(r'^entidades/$', entidades, name="entidades"),
    url(r'^detalle_entidad/(?P<pk>\d+)/$', EntidadDetailView.as_view(), name="detalle-entidad"),
    url(r'^editar_entidad/(?P<pk>\d+)/$', editar_entidad, name="editar-entidad"),
    url(r'^eliminar_entidad/$', eliminar_entidad, name='eliminar-entidad'),
    url(r'^crear_entidad/$', crear_entidad, name="crear-entidad"),

    #ENTIDAD PROYECTO
    url(r'^entidades_proyecto/$', entidades_proyecto, name="entidades-proyecto"),
    url(r'^detalle_entidad_proyecto/(?P<pk>\d+)/$', EntidadProyectoDetailView.as_view(), name="detalle-entidad-proyecto"),
    url(r'^editar_entidad_proyecto/(?P<pk>\d+)/$', editar_entidad_proyecto, name="editar-entidad-proyecto"),
    url(r'^editar_entidad_proyecto_1/(?P<pk>\d+)/$', editar_entidad_proyecto_1, name="editar-entidad-proyecto-1"),
    url(r'^crear_entidad_proyecto/$', crear_entidad_proyecto, name="crear-entidad-proyecto"),

    #DOCUMENTOS GENERALES
    url(r'^doc_generales/$', docs_generales, name="doc-generales"),
    url(r'^detalle_doc_general/(?P<pk>\d+)/$', DocsGeneralesDetailView.as_view(), name="detalle-doc-general"),
    url(r'^editar_doc_general/(?P<pk>\d+)/$', editar_doc_general, name="editar-doc-general"),
    url(r'^editar_doc_general_1/(?P<pk>\d+)/$', editar_doc_general_1, name="editar-doc-general-1"),
    url(r'^crear_doc_general/$', crear_doc_general, name="crear-doc-general"),

    #DETALLES DOCUMENTOS GENERALES
    url(r'^detalle_docs_generales/$', detalle_docs_generales, name="detalle-doc-generales"),
    url(r'^detalle_detalle_doc_general/(?P<pk>\d+)/$', DetalleDocsGeneralesDetailView.as_view(), name="detalle-detalle-doc-general"),
    url(r'^editar_detalle_doc_general/(?P<pk>\d+)/$', editar_detalle_doc_general, name="editar-detalle-doc-general"),
    url(r'^editar_detalle_doc_general_1/(?P<pk>\d+)/$', editar_detalle_doc_general_1, name="editar-detalle-doc-general-1"),
    url(r'^crear_detalle_doc_general/$', crear_detalle_doc_general, name="crear-detalle-doc-general"),

    #DETALLES DOCUMENTOS RESPONSIVA
    url(r'^detalles_doc_responsiva/$', detalle_doc_responsiva, name="detalles-doc-responsiva"),
    url(r'^detalle_detalle_doc_responsiva/(?P<pk>\d+)/$', DetalleDocsResponsivaDetailView.as_view(), name="detalle-detalle-doc-responsiva"),
    url(r'^editar_detalle_doc_responsiva/(?P<pk>\d+)/$', editar_detalle_doc_responsiva, name="editar-detalle-doc-responsiva"),
    url(r'^editar_detalle_doc_responsiva_1/(?P<pk>\d+)/$', editar_detalle_doc_responsiva_1, name="editar-detalle-doc-responsiva-1"),
    url(r'^crear_detalle_doc_responsiva/$', crear_detalle_doc_responsiva, name="crear-detalle-doc-responsiva"),

    #DETALLES PAGO EMPLEADO
    url(r'^detalles_pago_empleado/$', detalles_pago_empleado, name="detalles-pago-empleado"),
    url(r'^detalle_detalle_pago_empleado/(?P<pk>\d+)/$', DetallePagoEmpleadoDetailView.as_view(), name="detalle-detalle-pago-empleado"),
    url(r'^editar_detalle_pago_empleado/(?P<pk>\d+)/$', editar_detalle_pago_empleado, name="editar-detalle-pago-empleado"),
    url(r'^editar_detalle_pago_empleado_1/(?P<pk>\d+)/$', editar_detalle_pago_empleado_1, name="editar-detalle-pago-empleado-1"),
    url(r'^crear_detalle_pago_empleado/$', crear_detalle_pago_empleado, name="crear-detalle-pago-empleado"),
    )