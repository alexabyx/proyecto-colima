#! -*- coding:utf-8 -*-
# Create your views here.

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView

from inicio.models import ( Proyectos,
							Personal,
							Clientes,
							AnexosTecnicos,
							Contratos,
							Facturas,
							Convenios,
							Propuestas,
							Entidades,
							Entregables,
							DocumentosGenerales,
							DetallesDocumentosGenerales,
							DetalleDocumentoResponsiva,
							DetallePagoEmpleado,
							DetallesEntregables,
							DetallesFacturas,
							EntidadProyecto,
							Pagos,
							DetallePagos,
							HomologacionDeDocs,
							Alarmas,
						  )

from inicio.forms import (	RegistrarProyectoForm,
							RegistrarFacturaForm, 
							RegistrarAnexotecnicoForm,
							RegistrarContratoForm,
							RegistrarConvenioForm,
							RegistrarPropuestaForm,
							RegistrarPersonalForm,
							RegistrarClienteForm,
							RegistrarEntidadForm,
							RegistrarEntregableForm,
							RegistrarDocGeneralForm,
							RegistrarDetalleDocGeneralForm,
							RegistrarDetalleDocResponsivaForm,
							RegistrarPagoEmpleadoForm,
							RegistrarDetalleEntregableForm,
							RegistrarDetalleFacturaForm,
							RegistrarEntidadProyectoForm,
							RegistrarPagoForm,
							RegistrarDetallePagoForm,
							RegistrarHomologacionForm,
							RegistrarAlarmaForm,
						  )

from inicio.helpers import move_document

import os

#
#==================OPERACIONES DE PERSONAL========================
#
@login_required(login_url='/')
def personal(request):
	_historico = request.GET.get('historico', None)
	historico = [2,3] if _historico else [1]

	personal_list = Personal.objects.filter(habilitado=True, historico__in=historico).order_by('-fecha_ingreso')

	paginator = Paginator(personal_list, 9)
	page = request.GET.get('page', 1)

	try:
		personal = paginator.page(page)
	except PageNotAnInteger:
		personal = paginator.page(1)
	except EmptyPage:
		personal = paginator.page(paginator.num_pages)

	return render(request, 'inicio/personal.html', {'personal':personal, 'historico':_historico}, context_instance=RequestContext(request))

class PersonalDetailView(DetailView):
	
	template_name = "inicio/personal_detail.html"
	model = Personal

	def get_object(self):
		object = super(PersonalDetailView, self).get_object()
		return object

@login_required(login_url='/')
def crear_personal(request):
	if request.method=="POST":
		form = RegistrarPersonalForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				personal = Personal.objects.create(	
													rfc 						= form.cleaned_data['rfc'],
													nombre 						= form.cleaned_data['nombre'],
													apellido_paterno 			= form.cleaned_data['apellido_paterno'],
													apellido_materno 			= form.cleaned_data['apellido_materno'],
													siglas_nombre 				= form.cleaned_data['siglas_nombre'],
													genero 						= form.cleaned_data['genero'],
													direccion 					= form.cleaned_data['direccion'],
													telefono 					= form.cleaned_data['telefono'],
													no_seguro 					= form.cleaned_data['no_seguro'],
													fecha_ingreso 				= form.cleaned_data['fecha_ingreso'],
													puesto 						= form.cleaned_data['puesto'],
													turno 						= form.cleaned_data['turno'],
													tipo_plaza 					= form.cleaned_data['tipo_plaza'],
													especificacion 				= form.cleaned_data['especificacion'],
													tipo_pago 					= form.cleaned_data['tipo_pago'],
													monto 						= form.cleaned_data['monto'],
													dias_trabajo_al_mes 		= form.cleaned_data['dias_trabajo_al_mes'],
													fecha_vencimiento_contrato 	= form.cleaned_data['fecha_vencimiento_contrato'],
													fecha_baja 					= form.cleaned_data['fecha_baja'],
													motivo_baja 				= form.cleaned_data['motivo_baja'],
													)

				credencial_elector = form.cleaned_data['credencial_elector']
				if credencial_elector:
					personal.credencial_elector = credencial_elector
					personal.save()

			except Exception as e:
				mensaje = "Algo fallo al guardar el registro, favor de reportarlo al area de sistemas."
			else:
				mensaje = "El empleado ha sido creado exitosamente."
				return HttpResponseRedirect('/administracion/editar_personal/'+str(personal.id)+'/')
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarPersonalForm()
	return render(request, 'inicio/personal_create.html', {'form': form, 'mensaje': mensaje})

@login_required(login_url='/')
def editar_personal(request, pk):
	personal = Personal.objects.get(id=int(pk))

	if request.method=="POST":
		print request.FILES
		form = RegistrarPersonalForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				Personal.objects.filter(id=int(pk)).update(
															rfc 						= form.cleaned_data['rfc'],
															nombre 						= form.cleaned_data['nombre'],
															apellido_paterno 			= form.cleaned_data['apellido_paterno'],
															apellido_materno 			= form.cleaned_data['apellido_materno'],
															siglas_nombre 				= form.cleaned_data['siglas_nombre'],
															genero 						= form.cleaned_data['genero'],
															direccion 					= form.cleaned_data['direccion'],
															telefono 					= form.cleaned_data['telefono'],
															no_seguro 					= form.cleaned_data['no_seguro'],
															fecha_ingreso 				= form.cleaned_data['fecha_ingreso'],
															puesto 						= form.cleaned_data['puesto'],
															turno 						= form.cleaned_data['turno'],
															tipo_plaza 					= form.cleaned_data['tipo_plaza'],
															especificacion 				= form.cleaned_data['especificacion'],
															tipo_pago 					= form.cleaned_data['tipo_pago'],
															monto 						= form.cleaned_data['monto'],
															dias_trabajo_al_mes 		= form.cleaned_data['dias_trabajo_al_mes'],
															fecha_vencimiento_contrato 	= form.cleaned_data['fecha_vencimiento_contrato'],
															fecha_baja 					= form.cleaned_data['fecha_baja'],
															motivo_baja 				= form.cleaned_data['motivo_baja'],
															)
				
				credencial_elector = request.FILES.get('credencial_elector', None)
				if credencial_elector:
					if personal.credencial_elector and os.path.isfile(personal.credencial_elector.path):
						os.remove(personal.credencial_elector.path)
					personal.credencial_elector = credencial_elector
					personal.save()
			except Exception, e:				
				print "Error: ", e
				mensaje = "Los datos no pudieron ser actualizados"
			else:
				mensaje = "Datos actualizados correctamente"
		else:
			mensaje = "Proporcione los datos correctos"
	else:
		mensaje = ""
		data = model_to_dict(personal)
		form=RegistrarPersonalForm(data)

	convenios = Convenios.objects.filter(encargado=personal, habilitado=True).order_by('-fecha_creacion')
	contratos = Contratos.objects.filter(encargado=personal, habilitado=True).order_by('-fecha_creacion')
	entregables = Entregables.objects.filter(responsable=personal, habilitado=True).order_by('total')
	propuestas = Propuestas.objects.filter(responsable=personal, habilitado=True).order_by('-fecha_creacion')
	detalles_doc_generales = DetallesDocumentosGenerales.objects.filter(responsable=personal).order_by('-fecha_creacion')
	detalles_doc_responsiva = DetalleDocumentoResponsiva.objects.filter(personal=personal)
	detalles_pago_empleado = DetallePagoEmpleado.objects.filter(personal=personal)
	facturas = Facturas.objects.filter(responsable=personal).order_by('-fecha_emision')
	return render(request, 'inicio/personal_edit.html', {'mensaje':mensaje,
														 'personal': personal,
														 'form': form,
														 'entregables': entregables, 
														 'convenios': convenios,
														 'contratos': contratos,
														 'propuestas': propuestas,
														 'detalles_doc_generales':detalles_doc_generales,
														 'detalles_doc_responsiva':detalles_doc_responsiva,
														 'detalles_pago_empleado':detalles_pago_empleado,
														 'facturas': facturas})
	

@login_required(login_url='/')
def eliminar_personal(request):
	import json

	if not request.is_ajax():
		raise Http404

	pk = request.POST.get('pk')

	try:
		personal = Personal.objects.filter(id=pk).update(habilitado=False)
	except Exception, e:
		print "Error: ", e
		mensaje = {'mensaje': "Fallo la operación", 'error': True}
	else:
		mensaje = {'mensaje': "Operación exitosa", 'error': False}

	content = json.dumps(mensaje)
	http_response = HttpResponse(content, content_type="application/json")

	return http_response

#
#==================OPERACIONES DE DETALLE DE PAGO EMPLEADO========================
#
@login_required(login_url='/')
def detalles_pago_empleado(request):
	_historico = request.GET.get('historico', None)
	historico = [2,3] if _historico else [1]
	
	detalles_pago_empleado_list = DetallePagoEmpleado.objects.filter(historico__in=historico)

	paginator = Paginator(detalles_pago_empleado_list, 9)
	page = request.GET.get('page', 1)

	try:
		detalles_pago_empleado = paginator.page(page)
	except PageNotAnInteger:
		detalles_pago_empleado = paginator.page(1)
	except EmptyPage:
		detalles_pago_empleado = paginator.page(paginator.num_pages)

	return render(request, 'inicio/detalles_pago_empleado.html', {'detalles_pago_empleado':detalles_pago_empleado, 'historico':_historico}, context_instance=RequestContext(request))

class DetallePagoEmpleadoDetailView(DetailView):
	
	template_name = "inicio/detalle_pago_empleado_detail.html"
	model = DetallePagoEmpleado

	def get_object(self):
		object = super(DetallePagoEmpleadoDetailView, self).get_object()
		return object

@login_required(login_url='/')
def crear_detalle_pago_empleado(request):
	if request.method=="POST":
		form = RegistrarPagoEmpleadoForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				detalle_pago_empleado = DetallePagoEmpleado.objects.create(
																		personal 	= form.cleaned_data['personal'],
																		responsable = form.cleaned_data['responsable'],
																		)

				archivo_documento_de_pago = form.cleaned_data['archivo_documento_de_pago']

				if archivo_documento_de_pago:
					detalle_pago_empleado.archivo_documento_de_pago = archivo_documento_de_pago
					detalle_pago_empleado.save()

			except Exception, e:
				print "Error: ", e
				mensaje = "Algo fallo al guardar el registro, favor de reportarlo al area de sistemas."
			else:
				mensaje = "El detalle ha sido creado exitosamente"
				return HttpResponseRedirect('/administracion/editar_detalle_pago_empleado/'+str(detalle_pago_empleado.id)+'/')
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarPagoEmpleadoForm()
	return render(request, 'inicio/detalle_pago_empleado_create.html', {'form': form, 'mensaje':mensaje})

@login_required(login_url='/')
def editar_detalle_pago_empleado(request, pk):
	detalle_pago_empleado = DetallePagoEmpleado.objects.get(id=int(pk))
	
	if request.method=="POST":
		form = RegistrarPagoEmpleadoForm(request.POST, request.FILES)

		if form.is_valid():
			try:
				DetallePagoEmpleado.objects.filter(id=int(pk)).update(
																	personal 					= form.cleaned_data['personal'],
																	responsable 				= form.cleaned_data['responsable'],
																	)

				archivo_documento_de_pago = form.cleaned_data['archivo_documento_de_pago']
				if archivo_documento_de_pago:
					if detalle_pago_empleado.archivo_documento_de_pago and os.path.isfile(detalle_pago_empleado.archivo_documento_de_pago.path):
						os.remove(detalle_pago_empleado.archivo_documento_de_pago.path)
					detalle_pago_empleado.archivo_documento_de_pago = archivo_documento_de_pago
					detalle_pago_empleado.save()

			except Exception, e:				
				print "Error: ", e
				mensaje = "Los datos no pudieron ser actualizados"
			else:
				mensaje = "Datos actualizados correctamente"
		else:
			mensaje = "Por favor, proporcione los datos correctos"
	else:
		mensaje = ""
		form=RegistrarPagoEmpleadoForm(model_to_dict(detalle_pago_empleado))

	return render(request, 'inicio/detalle_pago_empleado_edit.html', {'form': form, 'detalle_pago_empleado': detalle_pago_empleado, 'mensaje':mensaje})

@login_required(login_url='/')
def editar_detalle_pago_empleado_1(request, pk):
	detalle_pago_empleado = DetallePagoEmpleado.objects.get(id=int(pk))
	if request.method=="POST":
		form = RegistrarPagoEmpleadoForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				DetallePagoEmpleado.objects.filter(id=int(pk)).update(
																	personal 					= form.cleaned_data['personal'],
																	responsable 				= form.cleaned_data['responsable'],
																	archivo_documento_de_pago 	= form.cleaned_data['archivo_documento_de_pago'],
																	)
				return render(request, "inicio/modal_ok.html", {'cabecera':"Operación exitosa", 'mensaje':"Los campos fueron actualizados correctamente"})
			except Exception, e:				
				print "Error: ", e
				mensaje = "El detalle no pudo ser actualizado"
		else:
			mensaje = "Los datos son invalidos"
	else:
		mensaje = ""
		form=RegistrarPagoEmpleadoForm(model_to_dict(detalle_pago_empleado))
	return render(request, 'inicio/detalle_pago_empleado_edit_1.html', {'form': form, 'id': detalle_pago_empleado.id, 'mensaje': mensaje})

#
#==================OPERACIONES DE DETALLES DE DOCUMENTOS RESPONSIVA========================
#

@login_required(login_url='/')
def detalle_doc_responsiva(request):
	_historico = request.GET.get('historico', None)
	historico = [2,3] if _historico else [1]

	detalle_doc_responsiva_list = DetalleDocumentoResponsiva.objects.filter(historico__in=historico)

	paginator = Paginator(detalle_doc_responsiva_list, 9)
	page = request.GET.get('page', 1)

	try:
		detalles_doc_responsiva = paginator.page(page)
	except PageNotAnInteger:
		detalles_doc_responsiva = paginator.page(1)
	except EmptyPage:
		detalles_doc_responsiva = paginator.page(paginator.num_pages)

	return render(request, 'inicio/detalles_doc_responsiva.html', {'detalles_doc_responsiva':detalles_doc_responsiva, 'historico': _historico}, context_instance=RequestContext(request))

class DetalleDocsResponsivaDetailView(DetailView):
	
	template_name = "inicio/detalle_doc_responsiva_detail.html"
	model = DetalleDocumentoResponsiva

	def get_object(self):
		object = super(DetalleDocsResponsivaDetailView, self).get_object()
		return object

@login_required(login_url='/')
def crear_detalle_doc_responsiva(request):
	if request.method=="POST":
		form = RegistrarDetalleDocResponsivaForm(request.POST, request.FILES)
		#import ipdb; ipdb.set_trace()
		if form.is_valid():
			try:
				detalle_doc_responsiva = DetalleDocumentoResponsiva.objects.create(
																				personal = form.cleaned_data['personal'],
																				)

				archivo_documento_responsiva = form.cleaned_data['archivo_documento_responsiva']
				if archivo_documento_responsiva:
					detalle_doc_responsiva.archivo_documento_responsiva = archivo_documento_responsiva
					detalle_doc_responsiva.save()

			except Exception as e:
				print "Error: ", e
				mensaje = "Algo fallo al guardar el registro, favor de reportarlo al area de sistemas."
			else:
				mensaje = "El registro fue creado exitosamente."
				return HttpResponseRedirect('/administracion/editar_detalle_doc_responsiva/'+str(detalle_doc_responsiva.id)+'/')
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje=""
		form=RegistrarDetalleDocResponsivaForm()
	return render(request, 'inicio/detalle_doc_responsiva_create.html', {'form': form, 'mensaje':mensaje})

@login_required(login_url='/')
def editar_detalle_doc_responsiva(request, pk):
	detalle_doc_responsiva = DetalleDocumentoResponsiva.objects.get(id=int(pk))
	if request.method=="POST":
		form = RegistrarDetalleDocResponsivaForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				DetalleDocumentoResponsiva.objects.filter(id=int(pk)).update(
																			personal = form.cleaned_data['personal'],
																			)

				archivo_documento_responsiva = form.cleaned_data['archivo_documento_responsiva']

				if archivo_documento_responsiva:
					if detalle_doc_responsiva.archivo_documento_responsiva and os.path.isfile(detalle_doc_responsiva.archivo_documento_responsiva.path):
						os.remove(detalle_doc_responsiva.archivo_documento_responsiva.path)
					detalle_doc_responsiva.archivo_documento_responsiva = archivo_documento_responsiva
					detalle_doc_responsiva.save()

			except Exception, e:				
				print "Error: ", e
				mensaje = "Los datos no pudieron ser actualizados."
			else:
				mensaje = "Datos actualizados correctamente."
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarDetalleDocResponsivaForm(model_to_dict(detalle_doc_responsiva))
	return render(request, 'inicio/detalle_doc_responsiva_edit.html', {'form': form, 'detalle_doc_responsiva': detalle_doc_responsiva, 'mensaje':mensaje})

@login_required(login_url='/')
def editar_detalle_doc_responsiva_1(request, pk):
	detalle_doc_responsiva = DetalleDocumentoResponsiva.objects.get(id=int(pk))
	if request.method=="POST":
		form = RegistrarDetalleDocResponsivaForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				DetalleDocumentoResponsiva.objects.filter(id=int(pk)).update(
																			personal 						= form.cleaned_data['personal'],
																			archivo_documento_responsiva 	= form.cleaned_data['archivo_documento_responsiva'],
																			)
				return render(request, "inicio/modal_ok.html", {'cabecera':"Operación exitosa", 'mensaje':"Los campos fueron actualizados correctamente"})
			except Exception, e:				
				print "Error: ", e
				mensaje = "El detalle no pudo ser actualizado"
		else:
			mensaje = "Los datos son invalidos"
	else:
		mensaje = ""
		form=RegistrarDetalleDocResponsivaForm(model_to_dict(detalle_doc_responsiva))
	return render(request, 'inicio/detalle_doc_responsiva_edit_1.html', {'form': form, 'id': detalle_doc_responsiva.id, 'mensaje': mensaje})

#
#==================OPERACIONES DE CLIENTES========================
#

@login_required(login_url='/')
def clientes(request):
	_historico = request.GET.get('historico', None)
	historico = [2,3] if _historico else [1]

	clientes_list = Clientes.objects.filter(habilitado=True, historico__in=historico).order_by('-fecha_creacion')

	paginator = Paginator(clientes_list, 9)
	page = request.GET.get('page', 1)

	try:
		clientes = paginator.page(page)
	except PageNotAnInteger:
		clientes = paginator.page(1)
	except EmptyPage:
		clientes = paginator.page(paginator.num_pages)

	return render(request, 'inicio/clientes.html', {'clientes':clientes, 'historico':_historico}, context_instance=RequestContext(request))

class ClienteDetailView(DetailView):
	
	template_name = "inicio/cliente_detail.html"
	model = Clientes

	def get_object(self):
		object = super(ClienteDetailView, self).get_object()
		return object

@login_required(login_url='/')
def crear_cliente(request):
	if request.method=="POST":
		form = RegistrarClienteForm(request.POST)
		if form.is_valid():
			try:
				cliente = Clientes.objects.create(
													nombre 	= form.cleaned_data['nombre'],
													siglas	= form.cleaned_data['siglas'],
													)
			except Exception, e:				
				print "Error: ", e
				mensaje = "El cliente no pudo ser creado."
			else:
				mensaje = "El registro fue creado exitosamente."
				return HttpResponseRedirect('/administracion/editar_cliente/'+str(cliente.id)+'/')
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarClienteForm()
	return render(request, 'inicio/cliente_create.html', {'form': form, 'mensaje': mensaje})

@login_required(login_url='/')
def editar_cliente(request, pk):
	cliente = Clientes.objects.get(id=int(pk))
	if request.method=="POST":
		form = RegistrarClienteForm(request.POST)
		if form.is_valid():
			try:
				Clientes.objects.filter(id=int(pk)).update(
															nombre 	= form.cleaned_data['nombre'],
															siglas	= form.cleaned_data['siglas'],
															)

			except Exception, e:				
				print "Error: ", e
				mensaje = "Los datos no puedieron ser actualizados."
			else:
				mensaje = "Los datos fueron actualizados correctamente."
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarClienteForm(model_to_dict(cliente))
	proyectos = Proyectos.objects.filter(cliente=cliente, habilitado=True).order_by('-fecha_inicio')

	return render(request, 'inicio/cliente_edit.html', {'mensaje': mensaje,
														'form': form,
														'proyectos': proyectos})	

@login_required(login_url='/')
def eliminar_cliente(request):
	import json

	if not request.is_ajax():
		raise Http404

	pk = request.POST.get('pk')

	try:
		cliente = Clientes.objects.filter(id=pk).update(habilitado=False)
	except Exception, e:
		print "Error: ", e
		mensaje = {'mensaje': "Fallo la operación", 'error': True}
	else:
		mensaje = {'mensaje': "Operación exitosa", 'error': False}

	content = json.dumps(mensaje)
	http_response = HttpResponse(content, content_type="application/json")

	return http_response

#
#==================OPERACIONES DE PROYECTOS========================
#

@login_required(login_url='/')
def proyectos(request):
	_historico = request.GET.get('historico', None)
	historico = [2,3] if _historico else [1]

	proyectos_list = Proyectos.objects.filter(habilitado=True, historico__in=historico)

	paginator = Paginator(proyectos_list, 9)
	page = request.GET.get('page', 1)

	try:
		proyectos = paginator.page(page)
	except PageNotAnInteger:
		proyectos = paginator.page(1)
	except EmptyPage:
		proyectos = paginator.page(paginator.num_pages)

	return render(request, 'inicio/proyectos.html', {'proyectos': proyectos, 'historico': _historico}, context_instance=RequestContext(request))

class ProyectoDetailView(DetailView):
	
	template_name = "inicio/proyecto_detail.html"
	model = Proyectos

	def get_object(self):
		object = super(ProyectoDetailView, self).get_object()
		return object

@login_required(login_url='/')
def crear_proyecto(request):
	if request.method=="POST":
		form = RegistrarProyectoForm(request.POST)
		if form.is_valid():
			try:
				proyecto = Proyectos.objects.create(
													nombre = form.cleaned_data['nombre'],
													siglas = form.cleaned_data['siglas'],
													cliente = form.cleaned_data['cliente'],
													fecha_inicio = form.cleaned_data['fecha_inicio'],
													fecha_fin = form.cleaned_data['fecha_fin'],
													avance = form.cleaned_data['avance'],
													comentario = form.cleaned_data['comentario'],
													)

				for responsable in form.cleaned_data['responsable']:
					proyecto.responsable.add(responsable)
				proyecto.save()

			except Exception, e:				
				print "Error: ", e
				mensaje = "El proyecto no pudo ser creado."
			else:
				mensaje = "El registro se creo correctamente."
				return HttpResponseRedirect('/administracion/editar_proyecto/'+str(proyecto.id)+'/')
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarProyectoForm()
	return render(request, 'inicio/proyecto_create.html', {'form': form, 'mensaje':mensaje})

@login_required(login_url='/')
def editar_proyecto(request, pk):
	proyecto = Proyectos.objects.get(id=int(pk))
	if request.method=="POST":
		form = RegistrarProyectoForm(request.POST)
		if form.is_valid():
			try:
				Proyectos.objects.filter(id=int(pk)).update( 
															nombre = form.cleaned_data['nombre'],
															siglas = form.cleaned_data['siglas'],																														
															cliente = form.cleaned_data['cliente'],								
															fecha_inicio = form.cleaned_data['fecha_inicio'],
															fecha_fin = form.cleaned_data['fecha_fin'],
															avance = form.cleaned_data['avance'],
															comentario = form.cleaned_data['comentario'],
															)
				proyecto.responsable.clear()			
				for responsable in form.cleaned_data['responsable']:
					proyecto.responsable.add(responsable)
				proyecto.save()
			except Exception, e:					
				print "Error: ", e
				mensaje = "Ocurrió un error a actualizar el proyecto."
			else:
				mensaje = "Los datos fueron actualizado correctamente."
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarProyectoForm(model_to_dict(proyecto))

	entregables 	= Entregables.objects.filter(proyecto = proyecto, habilitado=True).order_by('total')
	anexostecnicos 	= AnexosTecnicos.objects.filter(proyecto=proyecto, habilitado=True).order_by('-fecha_creacion')
	convenios 		= Convenios.objects.filter(proyecto=proyecto, habilitado=True).order_by('-fecha_creacion')
	contratos 		= Contratos.objects.filter(proyecto=proyecto, habilitado=True).order_by('-fecha_creacion')
	propuestas 		= Propuestas.objects.filter(proyecto=proyecto, habilitado=True).order_by('-fecha_creacion')
	pagos 			= Pagos.objects.filter(proyecto=proyecto).order_by('-fecha_pago')

	return render(request, 'inicio/proyecto_edit.html', {'mensaje': mensaje,
														 'form': form,
														 'entregables': entregables, 
														 'anexostecnicos': anexostecnicos, 
														 'convenios': convenios,
														 'contratos': contratos,
														 'propuestas': propuestas,
														 'pagos':pagos})

@login_required(login_url='/')
def editar_proyecto_1(request, pk):
	proyecto = Proyectos.objects.get(id=pk)

	if request.method=="POST":
		form = RegistrarProyectoForm(request.POST)
		if form.is_valid():
			try:
				Proyectos.objects.filter(id=int(pk)).update( 
															nombre = form.cleaned_data['nombre'],
															siglas = form.cleaned_data['siglas'],
															fecha_inicio = form.cleaned_data['fecha_inicio'],
															fecha_fin = form.cleaned_data['fecha_fin'],
															avance = form.cleaned_data['avance'],
															comentario = form.cleaned_data['comentario'],
															cliente = form.cleaned_data['cliente'],								
															)

				proyecto = Proyectos.objects.get(id = int(pk))

				proyecto.responsable.clear()			

				for responsable in form.cleaned_data['responsable']:
					personal = Personal.objects.get(id = int(responsable))
					proyecto.responsable.add(personal)
				proyecto.save()

				return render(request, "inicio/modal_ok.html", {'cabecera':"Operación exitosa", 'mensaje':"Los campos fueron actualizados correctamente"})
			except Exception, e:				
				print "Error: ", e
				mensaje = "El proyecto no pudo ser actualizado"
		else:
			mensaje = "Los datos son incorrectos"
	else:
		mensaje=""
		form=RegistrarProyectoForm(model_to_dict(proyecto))

	return render(request, 'inicio/proyecto_edit_1.html', {'form': form,'id':proyecto.id, 'mensaje':mensaje})

@login_required(login_url='/')
def eliminar_proyecto(request):
	import json

	if not request.is_ajax():
		raise Http404

	pk = request.POST.get('pk')

	try:
		proyecto = Proyectos.objects.filter(id=pk).update(habilitado=False)
	except Exception, e:
		print "Error: ", e
		mensaje = {'mensaje': "Fallo la operación", 'error': True}
	else:
		mensaje = {'mensaje': "Operación exitosa", 'error': False}

	content = json.dumps(mensaje)
	http_response = HttpResponse(content, content_type="application/json")

	return http_response


@login_required(login_url='/')
def historico_proyecto(request):
	import json

	if not request.is_ajax():
		raise Http404

	pk = request.POST.get('pk')
	historico = request.POST.get('historico')

	try:
		proyecto = Proyectos.objects.filter(id=pk).update(historico=historico)
	except Exception as e:
		print "Error: ", e
		mensaje = {'mensaje': "Fallo la operación", 'error': True}
	else:
		mensaje = {'mensaje': "Operación exitosa", 'error': False}

	content = json.dumps(mensaje)
	http_response = HttpResponse(content, content_type="application/json")

	return http_response	

#
#==================OPERACIONES DE ANEXOSTECNICOS========================
#

@login_required(login_url='/')
def anexostecnicos(request):
	_historico = request.GET.get('historico', None)
	historico = [2,3] if _historico else [1]
	print historico
	anexostecnicos_list = AnexosTecnicos.objects.filter(habilitado=True, historico__in = historico).order_by('-fecha_creacion')

	paginator = Paginator(anexostecnicos_list, 9)
	page = request.GET.get('page', 1)

	try:
		anexostecnicos = paginator.page(page)
	except PageNotAnInteger:
		anexostecnicos = paginator.page(1)
	except EmptyPage:
		anexostecnicos = paginator.page(paginator.num_pages)

	return render(request, 'inicio/anexostecnicos.html', {'anexostecnicos':anexostecnicos, 'historico': _historico}, context_instance=RequestContext(request))


@login_required(login_url='/')
def crear_anexotecnico(request):
	if request.method=="POST":
		form = RegistrarAnexotecnicoForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				anexotecnico = AnexosTecnicos.objects.create(
															numero_oficio 	= form.cleaned_data['numero_oficio'],	
															proyecto 		= form.cleaned_data['proyecto'],
															nombre 			= form.cleaned_data['nombre'],
															siglas 			= form.cleaned_data['siglas'],
															status 			= form.cleaned_data['status'],
															)
				archivo = form.cleaned_data['archivo']
				if archivo:
					anexotecnico = archivo
					anexotecnico.save()

			except Exception, e:				
				print "Error: ", e
				mensaje = "El anexotecnico no pudo ser creado."
			else:
				mensaje = "El registro se creo correctamente."
				return HttpResponseRedirect('/administracion/editar_anexotecnico/'+str(anexotecnico.id)+'/')
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarAnexotecnicoForm()
	return render(request, 'inicio/anexotecnico_create.html', {'form': form, 'mensaje': mensaje})

@login_required(login_url='/')
def editar_anexotecnico(request, pk):
	anexotecnico = AnexosTecnicos.objects.get(id=int(pk))
	if request.method=="POST":
		form = RegistrarAnexotecnicoForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				AnexosTecnicos.objects.filter(id=int(pk)).update(
																numero_oficio 	= form.cleaned_data['numero_oficio'],	
																proyecto 		= form.cleaned_data['proyecto'],
																nombre 			= form.cleaned_data['nombre'],
																siglas 			= form.cleaned_data['siglas'],
																status 			= form.cleaned_data['status'],
																)
				archivo = form.cleaned_data['archivo']
				if archivo:
					if anexotecnico.archivo and os.path.isfile(anexotecnico.archivo.path):
						os.remove(anexotecnico.archivo.path)
					anexotecnico.archivo = archivo
					anexotecnico.save()

			except Exception, e:				
				print "Error: ", e
				mensaje = "El anexotecnico no pudo ser actualizado."
			else:
				mensaje = "Los campos fueron actualizados correctamente."
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarAnexotecnicoForm(model_to_dict(anexotecnico))
	return render(request, 'inicio/anexotecnico_edit.html', {'form': form, 'anexotecnico': anexotecnico, 'mensaje': mensaje})

@login_required(login_url='/')
def editar_anexotecnico_1(request, pk):
	anexotecnico = AnexosTecnicos.objects.get(id=int(pk))
	if request.method=="POST":
		form = RegistrarAnexotecnicoForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				AnexosTecnicos.objects.filter(id=int(pk)).update(
																numero_oficio 	= form.cleaned_data['numero_oficio'],	
																proyecto 		= form.cleaned_data['proyecto'],
																nombre 			= form.cleaned_data['nombre'],
																siglas 			= form.cleaned_data['siglas'],
																status 			= form.cleaned_data['status'],
																archivo         = form.cleaned_data['archivo'],
																)
				return render(request, "inicio/modal_ok.html", {'cabecera':"Operación exitosa", 'mensaje':"Los campos fueron actualizados correctamente"})
			except Exception, e:				
				print "Error: ", e
				mensaje = "El anexotecnico no pudo ser actualizado"
		else:
			mensaje = "El anexo técnico no pudo ser actualizado"
			print "No paso"
	else:
		mensaje = ''
		form=RegistrarAnexotecnicoForm(model_to_dict(anexotecnico))
	return render(request, 'inicio/anexotecnico_edit_1.html', {'form': form, 'id': anexotecnico.id, 'mensaje': mensaje})

class AnexotecnicoDetailView(DetailView):
	
	template_name = "inicio/anexotecnico_detail.html"
	model = AnexosTecnicos

	def get_object(self):
		object = super(AnexotecnicoDetailView, self).get_object()
		return object

@login_required(login_url='/')
def eliminar_anexotecnico(request):
	import json

	if not request.is_ajax():
		raise Http404

	pk = request.POST.get('pk')

	try:
		proyecto = AnexosTecnicos.objects.filter(id=pk).update(habilitado=False)
	except Exception, e:
		print "Error: ", e
		mensaje = {'mensaje': "Fallo la operación", 'error': True}
	else:
		mensaje = {'mensaje': "Operación exitosa", 'error': False}

	content = json.dumps(mensaje)
	http_response = HttpResponse(content, content_type="application/json")

	return http_response

@login_required(login_url='/')
def historico_anexotecnico(request):
	import json

	if not request.is_ajax():
		raise Http404

	pk = request.POST.get('pk')
	historico = request.POST.get('historico')

	try:
		proyecto = Proyectos.objects.filter(id=pk).update(historico=historico)
	except Exception as e:
		print "Error: ", e
		mensaje = {'mensaje': "Fallo la operación", 'error': True}
	else:
		mensaje = {'mensaje': "Operación exitosa", 'error': False}

	content = json.dumps(mensaje)
	http_response = HttpResponse(content, content_type="application/json")

	return http_response

#
#==================OPERACIONES DE CONVENIOS========================
#
@login_required(login_url='/')
def convenios(request):
	_historico = request.GET.get('historico', None)
	historico = [2,3] if _historico else [1]

	convenios_list = Convenios.objects.filter(habilitado=True, historico__in = historico).order_by('-fecha_creacion')

	paginator = Paginator(convenios_list, 9)
	page = request.GET.get('page', 1)

	try:
		convenios = paginator.page(page)
	except PageNotAnInteger:
		convenios = paginator.page(1)
	except EmptyPage:
		convenios = paginator.page(paginator.num_pages)

	return render(request, 'inicio/convenios.html', {'convenios':convenios, 'historico': _historico}, context_instance=RequestContext(request))

class ConvenioDetailView(DetailView):
	
	template_name = "inicio/convenio_detail.html"
	model = Convenios

	def get_object(self):
		object = super(ConvenioDetailView, self).get_object()
		return object

@login_required(login_url='/')
def crear_convenio(request):
	if request.method=="POST":
		form = RegistrarConvenioForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				convenio = Convenios.objects.create(
													numero 		= form.cleaned_data['numero'],
													proyecto 	= form.cleaned_data['proyecto'],
													encargado 	= form.cleaned_data['encargado'],
													)

				archivo = form.cleaned_data['archivo']
				if archivo:
					convenio.archivo = archivo
					convenio.save()

			except Exception, e:				
				print "Error: ", e
				mensaje = "Ocurrió un error al crear el convenio."
			else:
				mensaje = "El registro fue creado correctamente."
				return HttpResponseRedirect('/administracion/editar_convenio/'+str(convenio.id)+'/')
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarConvenioForm()
	return render(request, 'inicio/convenio_create.html', {'form': form, 'mensaje':mensaje})

@login_required(login_url='/')
def editar_convenio(request, pk):
	convenio = Convenios.objects.get(id=int(pk))
	if request.method=="POST":
		form = RegistrarConvenioForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				Convenios.objects.filter(id=int(pk)).update(
															numero 		= form.cleaned_data['numero'],
															proyecto 	= form.cleaned_data['proyecto'],
															encargado 	= form.cleaned_data['encargado'],
															)
				archivo = form.cleaned_data['archivo']	
				if archivo:	
					if convenio.archivo and os.path.isfile(convenio.archivo.path):
						os.remove(convenio.archivo.path)
					convenio.archivo = archivo
					convenio.save()

			except Exception, e:				
				print "Error: ", e
				mensaje = "Los datos no pudieron ser actualizados."
			else:
				mensaje = "Datos actualizados correctamente."
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarConvenioForm(model_to_dict(convenio))
	return render(request, 'inicio/convenio_edit.html', {'form': form, 'convenio':convenio, 'mensaje':mensaje})

@login_required(login_url='/')
def editar_convenio_1(request, pk):
	convenio = Convenios.objects.get(id=int(pk))
	if request.method=="POST":
		form = RegistrarConvenioForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				Convenios.objects.filter(id=int(pk)).update(
															numero 		= form.cleaned_data['numero'],
															proyecto 	= form.cleaned_data['proyecto'],
															encargado 	= form.cleaned_data['encargado'],
															archivo 	= form.cleaned_data['archivo'],					
															)

				return render(request, "inicio/modal_ok.html", {'cabecera':"Operación exitosa", 'mensaje':"Los campos fueron actualizados correctamente"})
			except Exception, e:				
				print "Error: ", e
				mensaje = "El convenio no pudo ser actualizado."
		else:
			mensaje = "Los datos son incorrectos."
	else:
		mensaje = ''
		form=RegistrarConvenioForm(model_to_dict(convenio))
	return render(request, 'inicio/convenio_edit_1.html', {'form': form, 'id': convenio.id, 'mensaje':mensaje})

@login_required(login_url='/')
def eliminar_convenio(request):
	import json

	if not request.is_ajax():
		raise Http404

	pk = request.POST.get('pk')

	try:
		convenio = Convenios.objects.filter(id=pk).update(habilitado=False)
	except Exception, e:
		print "Error: ", e
		mensaje = {'mensaje': "Fallo la operación", 'error': True}
	else:
		mensaje = {'mensaje': "Operación exitosa", 'error': False}

	content = json.dumps(mensaje)
	http_response = HttpResponse(content, content_type="application/json")

	return http_response

#
#==================OPERACIONES DE CONTATOS========================
#

@login_required(login_url='/')
def contratos(request):
	_historico = request.GET.get('historico', None)
	historico = [2,3] if _historico else [1]

	contratos_list = Contratos.objects.filter(habilitado=True, historico__in=historico).order_by('-fecha_creacion')

	paginator = Paginator(contratos_list, 9)
	page = request.GET.get('page', 1)

	try:
		contratos = paginator.page(page)
	except PageNotAnInteger:
		contratos = paginator.page(1)
	except EmptyPage:
		contratos = paginator.page(paginator.num_pages)

	return render(request, 'inicio/contratos.html', {'contratos':contratos, 'historico': _historico}, context_instance=RequestContext(request))

class ContratoDetailView(DetailView):
	
	template_name = "inicio/contrato_detail.html"
	model = Contratos

	def get_object(self):
		object = super(ContratoDetailView, self).get_object()
		return object

@login_required(login_url='/')
def crear_contrato(request):
	if request.method=="POST":
		form = RegistrarContratoForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				contrato = Contratos.objects.create(
													numero_oficio 	= form.cleaned_data['numero_oficio'],	
													proyecto 		= form.cleaned_data['proyecto'],
													encargado 		= form.cleaned_data['encargado'],
													)
				
				archivo = form.cleaned_data['archivo']
				if archivo:
					contrato.archivo = archivo
					contrato.save()

			except Exception, e:				
				print "Error: ", e
				mensaje = "Ocurrió un error al crear el contrato."
			else:
				mensaje = "El contrato fue creado exitosamente."
				return HttpResponseRedirect('/administracion/editar_contrato/'+str(contrato.id)+'/')
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarContratoForm()
	return render(request, 'inicio/contrato_create.html', {'form': form})

@login_required(login_url='/')
def editar_contrato(request, pk):
	contrato = Contratos.objects.get(id=int(pk))
	if request.method=="POST":
		form = RegistrarContratoForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				Contratos.objects.filter(id=int(pk)).update(
															numero_oficio 	= form.cleaned_data['numero_oficio'],	
															proyecto 		= form.cleaned_data['proyecto'],
															encargado 			= form.cleaned_data['encargado'],
															)
				archivo = form.cleaned_data['archivo']
				if archivo:
					if contrato.archivo and os.path.isfile(contrato.archivo.path):
						os.remove(contrato.archivo.path)
					contrato.archivo = archivo
					contrato.save()
			
			except Exception, e:				
				print "Error: ", e
				mensaje = "Los datos no pudieron ser actualizados."
			else:
				mensaje = "Datos actualizados correctamente."
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarContratoForm(model_to_dict(contrato))
	facturas = Facturas.objects.filter(contrato=contrato).order_by('numero_factura', '-fecha_emision')
	return render(request, 'inicio/contrato_edit.html', {'mensaje':mensaje,
														 'contrato': contrato,
														 'form': form,
														 'facturas':facturas})

@login_required(login_url='/')
def editar_contrato_1(request, pk):
	contrato = Contratos.objects.get(id=int(pk))
	if request.method=="POST":
		form = RegistrarContratoForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				Contratos.objects.filter(id=int(pk)).update(
															numero_oficio 	= form.cleaned_data['numero_oficio'],	
															proyecto 		= form.cleaned_data['proyecto'],
															encargado 			= form.cleaned_data['encargado'],
															archivo         = form.cleaned_data['archivo'],
															)

				return render(request, "inicio/modal_ok.html", {'cabecera':"Operación exitosa", 'mensaje':"Los campos fueron actualizados correctamente"})
			except Exception, e:				
				print "Error: ", e
				mensaje = "El contrato no pudo ser actualizado."
		else:
			mensaje = "Los datos son incorrectos."
	else:
		mensaje = ''
		form=RegistrarContratoForm(model_to_dict(contrato))

	return render(request, 'inicio/contrato_edit_1.html', {'form': form, 'id': contrato.id, 'mensaje':mensaje})

@login_required(login_url='/')
def eliminar_contrato(request):
	import json

	if not request.is_ajax():
		raise Http404

	pk = request.POST.get('pk')

	try:
		contrato = Contratos.objects.filter(id=pk).update(habilitado=False)
	except Exception, e:
		print "Error: ", e
		mensaje = {'mensaje': "Fallo la operación", 'error': True}
	else:
		mensaje = {'mensaje': "Operación exitosa", 'error': False}

	content = json.dumps(mensaje)
	http_response = HttpResponse(content, content_type="application/json")

	return http_response

#
#==================OPERACIONES DE ENTREGABLES========================
#

@login_required(login_url='/')
def entregables(request):
	_historico = request.GET.get('historico', None)
	historico = [2,3] if _historico else [1]

	entregables_list = Entregables.objects.filter(habilitado=True, historico__in=historico).order_by('-proyecto__fecha_inicio')

	paginator = Paginator(entregables_list, 9)
	page = request.GET.get('page', 1)

	try:
		entregables = paginator.page(page)
	except PageNotAnInteger:
		entregables = paginator.page(1)
	except EmptyPage:
		entregables = paginator.page(paginator.num_pages)

	return render(request, 'inicio/entregables.html', {'entregables':entregables, 'historico': _historico}, context_instance=RequestContext(request))

class EntregableDetailView(DetailView):
	
	template_name = "inicio/entregable_detail.html"
	model = Entregables

	def get_object(self):
		object = super(EntregableDetailView, self).get_object()
		return object

@login_required(login_url='/')
def crear_entregable(request):
	if request.method=="POST":
		form = RegistrarEntregableForm(request.POST)
		if form.is_valid():
			try:
				entregable = Entregables.objects.create(
														proyecto 	= form.cleaned_data['proyecto'],
														responsable = form.cleaned_data['responsable'],
														total 		= form.cleaned_data['total'],
														)
			except Exception as e:
				print "Error: ", e
				mensaje = "Algo fallo al guardar el registro, favor de reportarlo al area de sistemas."
			else:
				mensaje = "El empleado ha sido creado exitosamente."
				return HttpResponseRedirect('/administracion/editar_entregable/'+str(entregable.id)+'/')
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarEntregableForm()
	return render(request, 'inicio/entregable_create.html', {'form': form, 'mensaje': mensaje})

@login_required(login_url='/')
def editar_entregable(request, pk):
	entregable = Entregables.objects.get(id=int(pk))

	if request.method=="POST":
		form = RegistrarEntregableForm(request.POST)
		if form.is_valid():
			try:
				Entregables.objects.filter(id=int(pk)).update(
															proyecto 	= form.cleaned_data['proyecto'],
															responsable = form.cleaned_data['responsable'],
															total 		= form.cleaned_data['total'],
															)

			except Exception, e:				
				print "Error: ", e
				mensaje = "Los datos no pudieron ser actualizados."
			else:
				mensaje = "Datos actualizados correctamente."
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarEntregableForm(model_to_dict(entregable))

	detalles_entregables = DetallesEntregables.objects.filter(entregable=entregable)
	return render(request, 'inicio/entregable_edit.html', {'mensaje': mensaje,
														   'form': form,
														   'detalles_entregables': detalles_entregables})

@login_required(login_url='/')
def editar_entregable_1(request, pk):
	# if not request.is_ajax():
	# 	raise Http404
	entregable = Entregables.objects.get(id=int(pk))

	if request.method=="POST":
		import json
		form = RegistrarEntregableForm(request.POST)
		if form.is_valid():
			try:
				Entregables.objects.filter(id=int(pk)).update(
															proyecto 	= form.cleaned_data['proyecto'],
															responsable = form.cleaned_data['responsable'],
															total 		= form.cleaned_data['total'],
															)

				return render(request, "inicio/modal_ok.html", {'cabecera':"Operación exitosa", 'mensaje':"Los campos fueron actualizados correctamente"})
			except Exception, e:				
				print "Error: ", e
				mensaje = "El entregable no pudo ser actualizado."
		else:
			mensaje = "Los datos no son validos."

	else:
		entregable = Entregables.objects.get(id=int(pk))
		form=RegistrarEntregableForm(model_to_dict(entregable))
		mensaje = None
	return render(request, 'inicio/entregable_edit_1.html', {'form': form, 'id': entregable.id, 'mensaje':mensaje})	

@login_required(login_url='/')
def eliminar_entregable(request):
	import json

	if not request.is_ajax():
		raise Http404

	pk = request.POST.get('pk')

	try:
		entregable = Entregables.objects.filter(id=pk).update(habilitado=False)
	except Exception, e:
		print "Error: ", e
		mensaje = {'mensaje': "Fallo la operación", 'error': True}
	else:
		mensaje = {'mensaje': "Operación exitosa", 'error': False}

	content = json.dumps(mensaje)
	http_response = HttpResponse(content, content_type="application/json")

	return http_response

#
#==================OPERACIONES DE DETALLE DE ENTREGABLES========================
#

@login_required(login_url='/')
def detalle_entregables(request):
	_historico = request.GET.get('historico', None)
	historico = [2,3] if _historico else [1]

	detalles_entregables_list = DetallesEntregables.objects.filter(historico__in=historico).order_by('-fecha_creacion')

	paginator = Paginator(detalles_entregables_list, 9)
	page = request.GET.get('page', 1)

	try:
		detalles_entregables = paginator.page(page)
	except PageNotAnInteger:
		detalles_entregables = paginator.page(1)
	except EmptyPage:
		detalles_entregables = paginator.page(paginator.num_pages)

	return render(request, 'inicio/detalle_entregables.html', {'detalles_entregables':detalles_entregables, 'historico': _historico}, context_instance=RequestContext(request))

class DetalleEntregableDetailView(DetailView):
	
	template_name = "inicio/detalle_entregable_detail.html"
	model = DetallesEntregables

	def get_object(self):
		object = super(DetalleEntregableDetailView, self).get_object()
		return object

@login_required(login_url='/')
def crear_detalle_entregable(request):
	if request.method=="POST":
		form = RegistrarDetalleEntregableForm(request.POST,request.FILES)
		if form.is_valid():
			try:
				detalle_entregable = DetallesEntregables.objects.create(
																		entregable 		= form.cleaned_data['entregable'],
																		responsable 	= form.cleaned_data['responsable'],
																		numero 			= form.cleaned_data['numero'],
																		nombre 			= form.cleaned_data['nombre'],
																		siglas 			= form.cleaned_data['siglas'],
																		status 			= form.cleaned_data['status'],
																		)

				archivo = form.cleaned_data['archivo']
				if archivo:
					detalle_entregable.archivo = archivo
					detalle_entregable.save()

			except Exception as e:
				print "Error: ", e
				mensaje = "Algo fallo al guardar el registro, favor de reportarlo al area de sistemas."
			else:
				mensaje = "El detalle ha sido creado exitosamente."
				return HttpResponseRedirect('/administracion/editar_detalle_entregable/'+str(detalle_entregable.id)+'/')
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""		
		form=RegistrarDetalleEntregableForm()
	return render(request, 'inicio/detalle_entregable_create.html', {'form': form, 'mensaje': mensaje})

@login_required(login_url='/')
def editar_detalle_entregable(request, pk):
	detalle_entregable = DetallesEntregables.objects.get(id=int(pk))
	if request.method=="POST":
		form = RegistrarDetalleEntregableForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				DetallesEntregables.objects.filter(id=int(pk)).update(
																	entregable 		= form.cleaned_data['entregable'],
																	responsable 	= form.cleaned_data['responsable'],
																	numero 			= form.cleaned_data['numero'],
																	nombre 			= form.cleaned_data['nombre'],
																	siglas 			= form.cleaned_data['siglas'],
																	status 			= form.cleaned_data['status'],
																	)
				archivo = form.cleaned_data['archivo']
				if archivo:
					if detalle_entregable.archivo and os.path.isfile(detalle_entregable.archivo.path):
						os.remove(detalle_entregable.archivo.path)
					detalle_entregable.archivo = archivo
					detalle_entregable.save()

			except Exception, e:				
				print "Error: ", e
				mensaje = "Los datos no pudieron ser actualizados."
			else:
				mensaje = "Datos actualizados correctamente."
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarDetalleEntregableForm(model_to_dict(detalle_entregable))
	return render(request, 'inicio/detalle_entregable_edit.html', {'form': form, 
																   'detalle_entregable': detalle_entregable,
																   'mensaje':mensaje})

@login_required(login_url='/')
def editar_detalle_entregable_1(request, pk):
	detalle_entregable = DetallesEntregables.objects.get(id=int(pk))

	if request.method=="POST":
		import json
		form = RegistrarDetalleEntregableForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				DetallesEntregables.objects.filter(id=int(pk)).update(
																	entregable 		= form.cleaned_data['entregable'],
																	responsable 	= form.cleaned_data['responsable'],
																	numero 			= form.cleaned_data['numero'],
																	nombre 			= form.cleaned_data['nombre'],
																	siglas 			= form.cleaned_data['siglas'],
																	archivo 		= form.cleaned_data['archivo'],
																	)

				return render(request, "inicio/modal_ok.html", {'cabecera':"Operación exitosa", 'mensaje':"Los campos fueron actualizados correctamente"})
			except Exception, e:				
				print "Error: ", e
				mensaje = "El detalle no pudo ser actualizado."
		else:
			mensaje = "Los datos no son validos."
	else:
		mensaje = ""
		form=RegistrarDetalleEntregableForm(model_to_dict(detalle_entregable))
	return render(request, 'inicio/detalle_entregable_edit_1.html', {'form': form, 'id': detalle_entregable.id, 'mensaje':mensaje})	

#
#==================OPERACIONES DE FACTURAS========================
#

@login_required(login_url='/')
def facturas(request):
	_historico = request.GET.get('historico', None)
	historico = [2,3] if _historico else [1]

	facturas_list = Facturas.objects.filter(historico__in=historico)

	paginator = Paginator(facturas_list, 9)
	page = request.GET.get('page', 1)

	try:
		facturas = paginator.page(page)
	except PageNotAnInteger:
		facturas = paginator.page(1)
	except EmptyPage:
		facturas = paginator.page(paginator.num_pages)

	return render(request, 'inicio/facturas.html', {'facturas': facturas, 'historico': _historico}, context_instance=RequestContext(request))

class FacturaDetailView(DetailView):
	
	template_name = "inicio/factura_detail.html"
	model = Facturas

	def get_object(self):
		object = super(FacturaDetailView, self).get_object()
		return object

@login_required(login_url='/')
def crear_factura(request):
	if request.method=="POST":
		form = RegistrarFacturaForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				factura = Facturas.objects.create(
													contrato 			= form.cleaned_data['contrato'],
													responsable 		= form.cleaned_data['responsable'],
													numero_factura 		= form.cleaned_data['numero_factura'],
													fecha_entrega 		= form.cleaned_data['fecha_entrega'],
													folio_venta 		= form.cleaned_data['folio_venta'],
													rfc 				= form.cleaned_data['rfc'],
													direccion 			= form.cleaned_data['direccion'],
													subtotal 			= form.cleaned_data['subtotal'],
													iva 				= form.cleaned_data['iva'],
													total_con_numero 	= form.cleaned_data['total_con_numero'],
													total_con_letra 	= form.cleaned_data['total_con_letra'],
													status 				= form.cleaned_data['status'],
													pagada 				= form.cleaned_data['pagada'],
													)

				archivo_xml 		= form.cleaned_data['archivo_xml']
				archivo_fisico 		= form.cleaned_data['archivo_fisico']

				if archivo_xml:
					factura.archivo_xml = archivo_xml
				if archivo_fisico:
					factura.archivo_fisico = archivo_fisico

				factura.save()

			except Exception as e:
				print "Error: ", e
				mensaje = "Algo fallo al guardar el registro, favor de reportarlo al area de sistemas."
			else:
				mensaje = "La factura ha sido creada exitosamente."
				return HttpResponseRedirect('/administracion/editar_factura/'+str(factura.id)+'/')
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarFacturaForm()
	return render(request, 'inicio/factura_create.html', {'form': form, 'mensaje': mensaje})

@login_required(login_url='/')
def editar_factura(request, pk):
	factura = Facturas.objects.get(id=int(pk))

	if request.method=="POST":
		form = RegistrarFacturaForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				Facturas.objects.filter(id=int(pk)).update(
															contrato 			= form.cleaned_data['contrato'],
															responsable 		= form.cleaned_data['responsable'],
															numero_factura 		= form.cleaned_data['numero_factura'],
															fecha_entrega 		= form.cleaned_data['fecha_entrega'],
															folio_venta 		= form.cleaned_data['folio_venta'],
															rfc 				= form.cleaned_data['rfc'],
															direccion 			= form.cleaned_data['direccion'],
															subtotal 			= form.cleaned_data['subtotal'],
															iva 				= form.cleaned_data['iva'],
															total_con_numero 	= form.cleaned_data['total_con_numero'],
															total_con_letra 	= form.cleaned_data['total_con_letra'],
															status 				= form.cleaned_data['status'],
															pagada 				= form.cleaned_data['pagada'],
															)

				archivo_xml 		= form.cleaned_data['archivo_xml']
				archivo_fisico 		= form.cleaned_data['archivo_fisico']

				if archivo_xml:
					if factura.archivo_xml and os.path.isfile(factura.archivo_xml.path):
						os.remove(factura.archivo_xml.path)
					factura.archivo_xml = archivo_xml

				if archivo_fisico:
					if factura.archivo_fisico and os.path.isfile(factura.archivo_fisico.path):
						os.remove(factura.archivo_fisico.path)
					factura.archivo_fisico = archivo_fisico
				factura.save()

			except Exception, e:				
				print "Error: ", e
				mensaje = "Los datos no pudieron ser actualizados."
			else:
				mensaje = "Datos actualizados correctamente."
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarFacturaForm(model_to_dict(factura))

	detalle_facturas = DetallesFacturas.objects.filter(factura=factura)
	print factura
	return render(request, 'inicio/factura_edit.html', {'mensaje': mensaje,
														'form': form,
														'factura': factura,
														'detalle_facturas': detalle_facturas})
	
@login_required(login_url='/')
def editar_factura_1(request, pk):
	factura = Facturas.objects.get(id=int(pk))
	if request.method=="POST":
		form = RegistrarFacturaForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				Facturas.objects.filter(id=int(pk)).update(
															contrato 			= form.cleaned_data['contrato'],
															responsable 		= form.cleaned_data['responsable'],
															numero_factura 		= form.cleaned_data['numero_factura'],
															fecha_entrega 		= form.cleaned_data['fecha_entrega'],
															folio_venta 		= form.cleaned_data['folio_venta'],
															rfc 				= form.cleaned_data['rfc'],
															direccion 			= form.cleaned_data['direccion'],
															subtotal 			= form.cleaned_data['subtotal'],
															iva 				= form.cleaned_data['iva'],
															total_con_numero 	= form.cleaned_data['total_con_numero'],
															total_con_letra 	= form.cleaned_data['total_con_letra'],
															pagada 				= form.cleaned_data['pagada'],
															status 				= form.cleaned_data['status'],														
															archivo_xml 		= form.cleaned_data['archivo_xml'],
															archivo_fisico 		= form.cleaned_data['archivo_fisico'],
															)
				return render(request, "inicio/modal_ok.html", {'cabecera':"Operación exitosa", 'mensaje':"Los campos fueron actualizados correctamente"})
			except Exception, e:				
				print "Error: ", e
				mensaje = "La factura no pudo ser actualizada"
		else:
			mensaje = "Los datos son invalidos"
	else:
		mensaje = ""
		form=RegistrarFacturaForm(model_to_dict(factura))
	return render(request, 'inicio/factura_edit_1.html', {'form': form, 'id': factura.id, 'mensaje': mensaje})


#
#==================OPERACIONES DE DETALLES DE FACTURAS========================
#

@login_required(login_url='/')
def detalle_facturas(request):
	_historico = request.GET.get('historico', None)
	historico = [2,3] if _historico else [1]

	detalle_facturas_list = DetallesFacturas.objects.filter(historico__in=historico)

	paginator = Paginator(detalle_facturas_list, 9)
	page = request.GET.get('page', 1)

	try:
		detalle_facturas = paginator.page(page)
	except PageNotAnInteger:
		detalle_facturas = paginator.page(1)
	except EmptyPage:
		detalle_facturas = paginator.page(paginator.num_pages)

	return render(request, 'inicio/detalle_facturas.html', {'detalle_facturas': detalle_facturas, 'historico': _historico}, context_instance=RequestContext(request))

class DetalleFacturaDetailView(DetailView):
	
	template_name = "inicio/detalle_factura_detail.html"
	model = DetallesFacturas

	def get_object(self):
		object = super(DetalleFacturaDetailView, self).get_object()
		return object

@login_required(login_url='/')
def crear_detalle_factura(request):
	if request.method=="POST":
		form = RegistrarDetalleFacturaForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				detalle_factura = DetallesFacturas.objects.create(
																factura 		= form.cleaned_data['factura'],
																descripcion 	= form.cleaned_data['descripcion'],
																cantidad 		= form.cleaned_data['cantidad'],
																)
			except Exception as e:
				print "Error: ", e
				mensaje = "Algo fallo al guardar el registro, favor de reportarlo al area de sistemas."
			else:
				mensaje = "El detalle ha sido creado exitosamente."
				return HttpResponseRedirect('/administracion/editar_detalle_factura/'+str(detalle_factura.id)+'/')
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarDetalleFacturaForm()
	return render(request, 'inicio/detalle_factura_create.html', {'form': form, 'mensaje':mensaje})

@login_required(login_url='/')
def editar_detalle_factura(request, pk):
	detalle_factura = DetallesFacturas.objects.get(id=int(pk))

	if request.method=="POST":
		form = RegistrarDetalleFacturaForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				DetallesFacturas.objects.filter(id=int(pk)).update(
																factura 		= form.cleaned_data['factura'],
																descripcion 	= form.cleaned_data['descripcion'],
																cantidad 		= form.cleaned_data['cantidad'],
																)
			except Exception, e:				
				print "Error: ", e
				mensaje = "Los datos no pudieron ser actualizados."
			else:
				mensaje = "Datos actualizados correctamente."
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarDetalleFacturaForm(model_to_dict(detalle_factura))
	return render(request, 'inicio/detalle_factura_edit.html', {'form': form, 'mensaje':mensaje})


@login_required(login_url='/')
def editar_detalle_factura_1(request, pk):
	detalle_factura = DetallesFacturas.objects.get(id=int(pk))
	if request.method=="POST":
		form = RegistrarDetalleFacturaForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				DetallesFacturas.objects.filter(id=int(pk)).update(
																factura 		= form.cleaned_data['factura'],
																descripcion 	= form.cleaned_data['descripcion'],
																cantidad 		= form.cleaned_data['cantidad'],
																)
				return render(request, "inicio/modal_ok.html", {'cabecera':"Operación exitosa", 'mensaje':"Los campos fueron actualizados correctamente"})
			except Exception, e:				
				print "Error: ", e
				mensaje = "La factura no pudo ser actualizada"
		else:
			mensaje = "Los datos son invalidos"
	else:
		mensaje = ""
		form=RegistrarDetalleFacturaForm(model_to_dict(detalle_factura))
	return render(request, 'inicio/detalle_factura_edit_1.html', {'form': form, 'id': detalle_factura.id, 'mensaje': mensaje})


#
#==================OPERACIONES DE PROPUESTAS========================
#
@login_required(login_url='/')
def propuestas(request):
	_historico = request.GET.get('historico', None)
	historico = [2,3] if _historico else [1]
	
	propuestas_list = Propuestas.objects.filter(habilitado=True, historico__in=historico).order_by('-fecha_creacion')

	paginator = Paginator(propuestas_list, 9)
	page = request.GET.get('page', 1)

	try:
		propuestas = paginator.page(page)
	except PageNotAnInteger:
		propuestas = paginator.page(1)
	except EmptyPage:
		propuestas = paginator.page(paginator.num_pages)

	return render(request, 'inicio/propuestas.html', {'propuestas':propuestas, 'historico': _historico}, context_instance=RequestContext(request))

class PropuestaDetailView(DetailView):
	
	template_name = "inicio/propuesta_detail.html"
	model = Propuestas

	def get_object(self):
		object = super(PropuestaDetailView, self).get_object()
		return object

@login_required(login_url='/')
def crear_propuesta(request):
	if request.method=="POST":
		form = RegistrarPropuestaForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				propuesta = Propuestas.objects.create(
													numero_oficio 	= form.cleaned_data['numero_oficio'],
													proyecto 		= form.cleaned_data['proyecto'],
													responsable 	= form.cleaned_data['responsable'],
													status 			= form.cleaned_data['status'],
													)
				archivo = form.cleaned_data['archivo']
				if archivo:
					propuesta.archivo = archivo
					propuesta.save()
			except Exception as e:
				print "Error: ", e
				mensaje = "Algo fallo al guardar el registro, favor de reportarlo al area de sistemas."
			else:
				mensaje = "La propuesta ha sido creado exitosamente."
				return HttpResponseRedirect('/administracion/editar_propuesta/'+str(propuesta.id)+'/')
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarPropuestaForm()
	return render(request, 'inicio/propuesta_create.html', {'form': form, 'mensaje':mensaje})

@login_required(login_url='/')
def editar_propuesta(request, pk):
	propuesta = Propuestas.objects.get(id=int(pk))

	if request.method=="POST":
		form = RegistrarPropuestaForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				Propuestas.objects.filter(id=int(pk)).update(
															numero_oficio 	= form.cleaned_data['numero_oficio'],
															proyecto 		= form.cleaned_data['proyecto'],
															responsable 	= form.cleaned_data['responsable'],
															status 			= form.cleaned_data['status'],
															)
				archivo = form.cleaned_data['archivo']
				if archivo:
					if propuesta.archivo and os.path.isfile(propuesta.archivo.path):
						os.remove(propuesta.path.file)	
					propuesta.archivo = archivo
					propuesta.save()

			except Exception, e:				
				print "Error: ", e
				mensaje = "Los datos no pudieron ser actualizados."
			else:
				mensaje = "Datos actualizados correctamente."
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarPropuestaForm(model_to_dict(propuesta))
	return render(request, 'inicio/propuesta_edit.html', {'form': form, 'propuesta': propuesta, 'mensaje': mensaje})

@login_required(login_url='/')
def editar_propuesta_1(request, pk):
	propuesta = Propuestas.objects.get(id=int(pk))

	if request.method=="POST":
		form = RegistrarPropuestaForm(request.POST)
		if form.is_valid():
			try:
				Propuestas.objects.filter(id=int(pk)).update(
															numero_oficio 	= form.cleaned_data['numero_oficio'],
															proyecto 		= form.cleaned_data['proyecto'],
															responsable 	= form.cleaned_data['responsable'],
															)

				return render(request, "inicio/modal_ok.html", {'cabecera':"Operación exitosa", 'mensaje':"Los campos fueron actualizados correctamente"})
			except Exception, e:				
				print "Error: ", e
				mensaje = "El convenio no pudo ser actualizado"
		else:
			mensaje = "Los datos son invalidos"
	else:
		mensaje = ''
		form=RegistrarPropuestaForm(model_to_dict(propuesta))

	return render(request, 'inicio/propuesta_edit_1.html', {'form': form, 'id': propuesta.id, 'mensaje': mensaje})	

@login_required(login_url='/')
def eliminar_propuesta(request):
	import json

	if not request.is_ajax():
		raise Http404

	pk = request.POST.get('pk')

	try:
		propuesta = Propuestas.objects.filter(id=pk).update(habilitado=False)
	except Exception, e:
		print "Error: ", e
		mensaje = {'mensaje': "Fallo la operación", 'error': True}
	else:
		mensaje = {'mensaje': "Operación exitosa", 'error': False}

	content = json.dumps(mensaje)
	http_response = HttpResponse(content, content_type="application/json")

	return http_response

#
#==================OPERACIONES DE DOCS GENERALES========================
#

@login_required(login_url='/')
def docs_generales(request):
	_historico = request.GET.get('historico', None)
	historico = [2,3] if _historico else [1]

	docs_generales_list = DocumentosGenerales.objects.filter(historico__in=historico).order_by('-fecha_creacion')

	paginator = Paginator(docs_generales_list, 9)
	page = request.GET.get('page', 1)

	try:
		docs_generales = paginator.page(page)
	except PageNotAnInteger:
		docs_generales = paginator.page(1)
	except EmptyPage:
		docs_generales = paginator.page(paginator.num_pages)

	return render(request, 'inicio/docs_generales.html', {'doc_generales':docs_generales, 'historico':_historico}, context_instance=RequestContext(request))

class DocsGeneralesDetailView(DetailView):
	
	template_name = "inicio/doc_general_detail.html"
	model = DocumentosGenerales

	def get_object(self):
		object = super(DocsGeneralesDetailView, self).get_object()
		return object

@login_required(login_url='/')
def crear_doc_general(request):
	if request.method=="POST":
		form = RegistrarDocGeneralForm(request.POST)
		if form.is_valid():
			try:
				doc_general = DocumentosGenerales.objects.create(
																entidad 	= form.cleaned_data['entidad'], 
																clave 		= form.cleaned_data['clave'],
																)
			except Exception as e:
				print "Error: ", e
				mensaje = "Algo fallo al guardar el registro, favor de reportarlo al area de sistemas."
			else:
				mensaje = "El doc. general ha sido creado exitosamente."
				return HttpResponseRedirect('/administracion/editar_doc_general/'+str(doc_general.id)+'/')
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""		
		form=RegistrarDocGeneralForm()
	return render(request, 'inicio/doc_general_create.html', {'form': form, 'mensaje': mensaje})

@login_required(login_url='/')
def editar_doc_general(request, pk):
	doc_general = DocumentosGenerales.objects.get(id=int(pk))

	if request.method=="POST":
		form = RegistrarDocGeneralForm(request.POST)
		if form.is_valid():
			try:
				DocumentosGenerales.objects.filter(id=int(pk)).update(
																		entidad 	= form.cleaned_data['entidad'], 
																		clave 		= form.cleaned_data['clave'],
																	)
			except Exception, e:				
				print "Error: ", e
				mensaje = "Los datos no pudieron ser actualizados."
			else:
				mensaje = "Datos actualizados correctamente."
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarDocGeneralForm(model_to_dict(doc_general))
	detalles = DetallesDocumentosGenerales.objects.filter(documentos_generales=doc_general)
	return render(request, 'inicio/doc_general_edit.html', {'form': form, 'detalles': detalles, 'mensaje':mensaje})

@login_required(login_url='/')
def editar_doc_general_1(request, pk):
	# if not request.is_ajax():
	# 	raise Http404
	doc_general = DocumentosGenerales.objects.get(id=int(pk))

	if request.method=="POST":
		import json
		form = RegistrarDocGeneralForm(request.POST)
		if form.is_valid():
			try:
				DocumentosGenerales.objects.filter(id=int(pk)).update(
																	entidad 	= form.cleaned_data['entidad'], 
																	clave 		= form.cleaned_data['clave'],
																	)

				return render(request, "inicio/modal_ok.html", {'cabecera':"Operación exitosa", 'mensaje':"Los campos fueron actualizados correctamente"})
			except Exception, e:				
				print "Error: ", e
				mensaje = "El entregable no pudo ser actualizado."
		else:
			mensaje = "Los datos no son validos."
	else:
		mensaje = None
		form=RegistrarDocGeneralForm(model_to_dict(doc_general))
	return render(request, 'inicio/doc_general_edit_1.html', {'form': form, 'id': doc_general.id, 'mensaje':mensaje})

#
#==================OPERACIONES DE DETALLES DE DOCUMENTOS GENERALES========================
#

@login_required(login_url='/')
def detalle_docs_generales(request):
	_historico = request.GET.get('historico', None)
	historico = [2,3] if _historico else [1]

	detalle_docs_generales_list = DetallesDocumentosGenerales.objects.filter(historico__in=historico).order_by('-fecha_creacion')

	paginator = Paginator(detalle_docs_generales_list, 9)
	page = request.GET.get('page', 1)

	try:
		detalle_docs_generales = paginator.page(page)
	except PageNotAnInteger:
		detalle_docs_generales = paginator.page(1)
	except EmptyPage:
		detalle_docs_generales = paginator.page(paginator.num_pages)

	return render(request, 'inicio/detalle_docs_generales.html', {'detalle_docs_generales':detalle_docs_generales, 'historico': _historico}, context_instance=RequestContext(request))

class DetalleDocsGeneralesDetailView(DetailView):
	
	template_name = "inicio/detalle_doc_general_detail.html"
	model = DetallesDocumentosGenerales

	def get_object(self):
		object = super(DetalleDocsGeneralesDetailView, self).get_object()
		return object

@login_required(login_url='/')
def crear_detalle_doc_general(request):
	if request.method=="POST":
		form = RegistrarDetalleDocGeneralForm(request.POST, request.FILES)
		if form.is_valid():
			try:				
				detalle_doc_general = DetallesDocumentosGenerales.objects.create(
																				documentos_generales 	= form.cleaned_data['documentos_generales'],
																				responsable 			= form.cleaned_data['responsable'],
																				nombre 					= form.cleaned_data['nombre'],
																				status 					= form.cleaned_data['status'],
																				)
				archivo = form.cleaned_data['archivo']
				if archivo:
					detalle_doc_general.archivo = archivo
					detalle_doc_general.save()
			except Exception as e:
				print "Error: ", e
				mensaje = "Algo fallo al guardar el registro, favor de reportarlo al area de sistemas."
			else:
				mensaje = "El detalle ha sido creado exitosamente."
				return HttpResponseRedirect('/administracion/editar_detalle_doc_general/'+str(detalle_doc_general.id)+'/')
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarDetalleDocGeneralForm()
	return render(request, 'inicio/detalle_doc_general_create.html', {'form': form})

@login_required(login_url='/')
def editar_detalle_doc_general(request, pk):
	detalle_doc_general = DetallesDocumentosGenerales.objects.get(id=int(pk))

	if request.method=="POST":
		form = RegistrarDetalleDocGeneralForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				DetallesDocumentosGenerales.objects.filter(id=int(pk)).update(
																			documentos_generales 	= form.cleaned_data['documentos_generales'],
																			responsable 			= form.cleaned_data['responsable'],
																			nombre 					= form.cleaned_data['nombre'],
																			status 					= form.cleaned_data['status'],
																			)
				archivo = form.cleaned_data['archivo']
				if archivo:
					if detalle_doc_general.archivo and os.path.isfile(detalle_doc_general.archivo.path):
						os.remove(detalle_doc_general.archivo.path)
					detalle_doc_general.archivo = archivo
					detalle_doc_general.save()

			except Exception, e:				
				print "Error: ", e
				mensaje = "Los datos no pudieron ser actualizados."
			else:
				mensaje = "Datos actualizados correctamente."
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarDetalleDocGeneralForm(model_to_dict(detalle_doc_general))
	return render(request, 'inicio/detalle_doc_general_edit.html', {'form': form, 'mensaje': mensaje, 'detalle_doc_general': detalle_doc_general})

@login_required(login_url='/')
def editar_detalle_doc_general_1(request, pk):
	detalle_doc_general = DetallesDocumentosGenerales.objects.get(id=int(pk))
	if request.method=="POST":
		form = RegistrarDetalleDocGeneralForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				DetallesDocumentosGenerales.objects.filter(id=int(pk)).update(
																			documentos_generales 	= form.cleaned_data['documentos_generales'],
																			responsable 			= form.cleaned_data['responsable'],
																			numero 					= form.cleaned_data['numero'],
																			nombre 					= form.cleaned_data['nombre'],
																			siglas 					= form.cleaned_data['siglas'],
																			archivo 				= form.cleaned_data['archivo'],
																			)
				return render(request, "inicio/modal_ok.html", {'cabecera':"Operación exitosa", 'mensaje':"Los campos fueron actualizados correctamente"})
			except Exception, e:				
				print "Error: ", e
				mensaje = "El detalle no pudo ser actualizado"
		else:
			mensaje = "Los datos son invalidos"
	else:
		mensaje = ""
		form=RegistrarDetalleDocGeneralForm(model_to_dict(detalle_doc_general))
	return render(request, 'inicio/detalle_doc_general_edit_1.html', {'form': form, 'id': detalle_doc_general.id, 'mensaje': mensaje})


#
#==================OPERACIONES DE ENTIDADES========================
#

@login_required(login_url='/')
def entidades(request):
	_historico = request.GET.get('historico', None)
	historico = [2,3] if _historico else [1]

	entidades_list = Entidades.objects.filter(habilitado=True, historico__in=historico).order_by('-fecha_creacion')

	paginator = Paginator(entidades_list, 9)
	page = request.GET.get('page', 1)

	try:
		entidades = paginator.page(page)
	except PageNotAnInteger:
		entidades = paginator.page(1)
	except EmptyPage:
		entidades = paginator.page(paginator.num_pages)

	return render(request, 'inicio/entidades.html', {'entidades':entidades, 'historico': _historico}, context_instance=RequestContext(request))

class EntidadDetailView(DetailView):
	
	template_name = "inicio/entidad_detail.html"
	model = Entidades

	def get_object(self):
		object = super(EntidadDetailView, self).get_object()
		return object

@login_required(login_url='/')
def crear_entidad(request):
	if request.method=="POST":
		form = RegistrarEntidadForm(request.POST)
		if form.is_valid():
			try:
				entidad = Entidades.objects.create(
													nombre 	= form.cleaned_data['nombre'],
													siglas 	= form.cleaned_data['siglas'], 
													tipo 	= form.cleaned_data['tipo'],
													)
			except Exception as e:
				print "Error: ", e
				mensaje = "Algo fallo al guardar el registro, favor de reportarlo al area de sistemas."
			else:
				mensaje = "La entidad ha sido creada exitosamente."
				return HttpResponseRedirect('/administracion/editar_entidad/'+str(entidad.id)+'/')
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarEntidadForm()
	return render(request, 'inicio/entidad_create.html', {'form': form, 'mensaje': mensaje})

@login_required(login_url='/')
def editar_entidad(request, pk):
	entidad = Entidades.objects.get(id=int(pk))
	if request.method=="POST":
		form = RegistrarEntidadForm(request.POST)
		if form.is_valid():
			try:
				Entidades.objects.filter(id=int(pk)).update(
															nombre 	= form.cleaned_data['nombre'],
															siglas 	= form.cleaned_data['siglas'], 
															tipo 	= form.cleaned_data['tipo'],
															)

			except Exception, e:				
				print "Error: ", e
				mensaje = "Los datos no pudieron ser actualizados."
			else:
				mensaje = "Datos actualizados correctamente."
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarEntidadForm(model_to_dict(entidad))
	entidades_proyectos = EntidadProyecto.objects.filter(entidad=entidad)
	return render(request, 'inicio/entidad_edit.html', {'form': form,'mensaje':mensaje, 'entidades_proyectos': entidades_proyectos})	

@login_required(login_url='/')
def eliminar_entidad(request):
	import json

	if not request.is_ajax():
		raise Http404

	pk = request.POST.get('pk')

	try:
		entidad = Entidades.objects.filter(id=pk).update(habilitado=False)
	except Exception, e:
		print "Error: ", e
		mensaje = {'mensaje': "Fallo la operación", 'error': True}
	else:
		mensaje = {'mensaje': "Operación exitosa", 'error': False}

	content = json.dumps(mensaje)
	http_response = HttpResponse(content, content_type="application/json")

	return http_response

#
#==================OPERACIONES DE ENTIDADES PROYECTO========================
#

@login_required(login_url='/')
def entidades_proyecto(request):
	_historico = request.GET.get('historico', None)
	historico = [2,3] if _historico else [1]

	entidades_proyecto_list = EntidadProyecto.objects.filter(historico__in=historico)
	
	paginator = Paginator(entidades_proyecto_list, 9)
	page = request.GET.get('page', 1)

	try:
		entidades_proyecto = paginator.page(page)
	except PageNotAnInteger:
		entidades_proyecto = paginator.page(1)
	except EmptyPage:
		entidades_proyecto = paginator.page(paginator.num_pages)

	return render(request, 'inicio/entidades_proyecto.html', {'entidades_proyecto':entidades_proyecto, 'historico': _historico}, context_instance=RequestContext(request))

class EntidadProyectoDetailView(DetailView):
	
	template_name = "inicio/entidad_proyecto_detail.html"
	model = EntidadProyecto

	def get_object(self):
		object = super(EntidadProyectoDetailView, self).get_object()
		return object

@login_required(login_url='/')
def crear_entidad_proyecto(request):
	if request.method=="POST":
		form = RegistrarEntidadProyectoForm(request.POST)
		if form.is_valid():
			try:
				entidad_proyecto = EntidadProyecto.objects.create(
														entidad 	= form.cleaned_data['entidad'],
														proyecto 	= form.cleaned_data['proyecto'],
														porcentaje  = form.cleaned_data['porcentaje'],
														)
			except Exception as e:
				print "Error: ", e
				mensaje = "Algo fallo al guardar el registro, favor de reportarlo al area de sistemas."
			else:
				mensaje = "La relación ha sido creada exitosamente."
				return HttpResponseRedirect('/administracion/editar_entidad_proyecto/'+str(entidad_proyecto.id)+'/')
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarEntidadProyectoForm()
	return render(request, 'inicio/entidad_proyecto_create.html', {'form': form, 'mensaje': mensaje})

@login_required(login_url='/')
def editar_entidad_proyecto(request, pk):
	if request.method=="POST":
		form = RegistrarEntidadProyectoForm(request.POST)
		if form.is_valid():
			try:
				EntidadProyecto.objects.filter(id=int(pk)).update(
													entidad 	= form.cleaned_data['entidad'],
													proyecto 	= form.cleaned_data['proyecto'],
													porcentaje  = form.cleaned_data['porcentaje'],
															)

			except Exception, e:				
				print "Error: ", e
				mensaje = "Los datos no pudieron ser actualizados."
			else:
				mensaje = "Datos actualizados correctamente."
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		entidad_proyecto = EntidadProyecto.objects.get(id=int(pk))
		form=RegistrarEntidadProyectoForm(model_to_dict(entidad_proyecto))
	return render(request, 'inicio/entidad_proyecto_edit.html', {'form': form, 'mensaje':mensaje})	

@login_required(login_url='/')
def editar_entidad_proyecto_1(request, pk):
	entidad_proyecto = EntidadProyecto.objects.get(id=int(pk))
	if request.method=="POST":
		form = RegistrarEntidadProyectoForm(request.POST)
		if form.is_valid():
			try:
				EntidadProyecto.objects.filter(id=int(pk)).update(
													entidad 	= form.cleaned_data['entidad'],
													proyecto 	= form.cleaned_data['proyecto'],
													porcentaje  = form.cleaned_data['porcentaje'],
															)

				return render(request, "inicio/modal_ok.html", {'cabecera':"Operación exitosa", 'mensaje':"Los campos fueron actualizados correctamente"})
			except Exception, e:				
				print "Error: ", e
				mensaje = "Entidad-proyecto no pudo ser actualizada"
		else:
			mensaje = "Los datos son invalidos"
	else:
		mensaje = ""
		form=RegistrarEntidadProyectoForm(model_to_dict(entidad_proyecto))
	return render(request, 'inicio/entidad_proyecto_edit_1.html', {'form': form, 'id': entidad_proyecto.id, 'mensaje':mensaje})

#
#==================OPERACIONES DE PAGOS========================
#

@login_required(login_url='/')
def pagos(request):
	_historico = request.GET.get('historico', None)
	historico = [2,3] if _historico else [1]

	pagos_list = Pagos.objects.filter(historico__in=historico).order_by('fecha_pago')

	paginator = Paginator(pagos_list, 9)
	page = request.GET.get('page', 1)

	try:
		pagos = paginator.page(page)
	except PageNotAnInteger:
		pagos = paginator.page(1)
	except EmptyPage:
		pagos = paginator.page(paginator.num_pages)

	return render(request, 'inicio/pagos.html', {'pagos':pagos, 'historico': _historico}, context_instance=RequestContext(request))

class PagoDetailView(DetailView):
	
	template_name = "inicio/pago_detail.html"
	model = Pagos

	def get_object(self):
		object = super(PagoDetailView, self).get_object()
		return object

@login_required(login_url='/')
def crear_pago(request):
	if request.method=="POST":
		form = RegistrarPagoForm(request.POST)
		if form.is_valid():
			try:
				pago = Pagos.objects.create(
											proyecto 	= form.cleaned_data['proyecto'],
											monto_total = form.cleaned_data['monto_total'],
											fecha_pago 	= form.cleaned_data['fecha_pago'],
	  									  )

			except Exception as e:
				print "Error: ", e
				mensaje = "Algo fallo al guardar el registro, favor de reportarlo al area de sistemas."
			else:
				mensaje = "El pago ha sido creado exitosamente."
				return HttpResponseRedirect('/administracion/editar_pago/'+str(pago.id)+'/')
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarPagoForm()
	return render(request, 'inicio/pago_create.html', {'form': form, 'mensaje': mensaje})

@login_required(login_url='/')
def editar_pago(request, pk):
	pago = Pagos.objects.get(id=int(pk))
	if request.method=="POST":
		form = RegistrarPagoForm(request.POST)
		if form.is_valid():
			try:
				Pagos.objects.filter(id=int(pk)).update(
														proyecto 	= form.cleaned_data['proyecto'],
														monto_total = form.cleaned_data['monto_total'],
														fecha_pago 	= form.cleaned_data['fecha_pago'],
														)

			except Exception, e:				
				print "Error: ", e
				mensaje = "Los datos no pudieron ser actualizados."
			else:
				mensaje = "Datos actualizados correctamente."
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarPagoForm(model_to_dict(pago))
	detalles_pago = DetallePagos.objects.filter(pago=pago)

	return render(request, 'inicio/pago_edit.html', {'form': form, 'mensaje': mensaje, 'detalles_pago':detalles_pago})

@login_required(login_url='/')
def editar_pago_1(request, pk):
	pago = Pagos.objects.get(id=int(pk))

	if request.method=="POST":
		form = RegistrarPagoForm(request.POST)
		if form.is_valid():
			try:
				Pagos.objects.filter(id=int(pk)).update(
														proyecto 	= form.cleaned_data['proyecto'],
														monto_total = form.cleaned_data['monto_total'],
														fecha_pago 	= form.cleaned_data['fecha_pago'],
														)

				return render(request, "inicio/modal_ok.html", {'cabecera':"Operación exitosa", 'mensaje':"Los campos fueron actualizados correctamente"})
			except Exception, e:				
				print "Error: ", e
				mensaje = "El pago no pudo ser actualizado"
		else:
			mensaje = "Proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarPagoForm(model_to_dict(pago))
	return render(request, 'inicio/pago_edit_1.html', {'form': form, 'id': pago.id, 'mensaje': mensaje})

#
#==================OPERACIONES DE DETALLE DE PAGOS========================
#

@login_required(login_url='/')
def detalle_pagos(request):
	_historico = request.GET.get('historico', None)
	historico = [2,3] if _historico else [1]

	detalle_pagos_list = DetallePagos.objects.filter(historico__in=historico).order_by('fecha_pago')

	paginator = Paginator(detalle_pagos_list, 9)
	page = request.GET.get('page', 1)

	try:
		detalle_pagos = paginator.page(page)
	except PageNotAnInteger:
		detalle_pagos = paginator.page(1)
	except EmptyPage:
		detalle_pagos = paginator.page(paginator.num_pages)

	return render(request, 'inicio/detalle_pagos.html', {'detalle_pagos':detalle_pagos, 'historico':_historico}, context_instance=RequestContext(request))

class DetallePagosDetailView(DetailView):
	
	template_name = "inicio/detalle_pago_detail.html"
	model = DetallePagos

	def get_object(self):
		object = super(DetallePagosDetailView, self).get_object()
		return object

@login_required(login_url='/')
def crear_detalle_pago(request):
	if request.method=="POST":
		form = RegistrarDetallePagoForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				detalle_pago = DetallePagos.objects.create(
															entregable 			= form.cleaned_data['entregable'],
															pago 				= form.cleaned_data['pago'],
															nombre_pago_origen 	= form.cleaned_data['nombre_pago_origen'],
															siglas_pago_origen	= form.cleaned_data['siglas_pago_origen'],
															nombre_pago_destino	= form.cleaned_data['nombre_pago_destino'],
															siglas_pago_destino	= form.cleaned_data['siglas_pago_destino'],
															fecha_pago			= form.cleaned_data['fecha_pago'],
															monto 				= form.cleaned_data['monto'],
															porcentaje_de_pago	= form.cleaned_data['porcentaje_de_pago'],
															tipo_de_pago		= form.cleaned_data['tipo_de_pago'],
															responsable 		= form.cleaned_data['responsable'],
															pagado 				= form.cleaned_data['pagado'],
					  									  )

				_detalle_pago = form.cleaned_data['detalle_pago']
				if _detalle_pago:
					detalle_pago.detalle_pago = _detalle_pago
					detalle_pago.save()

				documento_deposito = form.cleaned_data['documento_deposito']
				if documento_deposito:
					detalle_pago.documento_deposito = documento_deposito
					detalle_pago.save()

			except Exception, e:
				print "Error: ", e
				mensaje = "Algo fallo al guardar el registro, favor de reportarlo al area de sistemas."
			else:
				mensaje = "El detalle ha sido creado exitosamente."
				return HttpResponseRedirect('/administracion/editar_detalle_pago/'+str(detalle_pago.id)+'/')
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarDetallePagoForm()
	return render(request, 'inicio/detalle_pago_create.html', {'form': form, 'mensaje': mensaje})

@login_required(login_url='/')
def editar_detalle_pago(request, pk):
	detalle_pago = DetallePagos.objects.get(id=int(pk))
	if request.method=="POST":
		form = RegistrarDetallePagoForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				DetallePagos.objects.filter(id=int(pk)).update(
														entregable 			= form.cleaned_data['entregable'],
														pago 				= form.cleaned_data['pago'],
														detalle_pago 		= form.cleaned_data['detalle_pago'],
														nombre_pago_origen 	= form.cleaned_data['nombre_pago_origen'],
														siglas_pago_origen	= form.cleaned_data['siglas_pago_origen'],
														nombre_pago_destino	= form.cleaned_data['nombre_pago_destino'],
														siglas_pago_destino	= form.cleaned_data['siglas_pago_destino'],
														fecha_pago			= form.cleaned_data['fecha_pago'],
														monto 				= form.cleaned_data['monto'],
														porcentaje_de_pago	= form.cleaned_data['porcentaje_de_pago'],
														tipo_de_pago		= form.cleaned_data['tipo_de_pago'],
														responsable 		= form.cleaned_data['responsable'],
														pagado 				= form.cleaned_data['pagado'],
														)
				
				documento_deposito	= form.cleaned_data['documento_deposito']
				if documento_deposito:
					if detalle_pago.documento_deposito and os.path.isfile(detalle_pago.documento_deposito.path):
						os.remove(detalle_pago.documento_deposito.path)
					detalle_pago.documento_deposito = documento_deposito
					detalle_pago.save() 

			except Exception, e:				
				print "Error: ", e
				mensaje = "Los datos no pudieron ser actualizados."
			else:
				mensaje = "Datos actualizados correctamente."
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarDetallePagoForm(model_to_dict(detalle_pago))
	return render(request, 'inicio/detalle_pago_edit.html', {'form': form, 'mensaje': mensaje, 'detalle_pago': detalle_pago})

@login_required(login_url='/')
def editar_detalle_pago_1(request, pk):
	detalle_pago = DetallePagos.objects.get(id=int(pk))

	if request.method=="POST":
		form = RegistrarDetallePagoForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				DetallePagos.objects.filter(id=int(pk)).update(
														entregable 			= form.cleaned_data['entregable'],
														pago 				= form.cleaned_data['pago'],
														detalle_pago 		= form.cleaned_data['detalle_pago'],														
														nombre_pago_origen 	= form.cleaned_data['nombre_pago_origen'],
														siglas_pago_origen	= form.cleaned_data['siglas_pago_origen'],
														nombre_pago_destino	= form.cleaned_data['nombre_pago_destino'],
														siglas_pago_destino	= form.cleaned_data['siglas_pago_destino'],
														fecha_pago			= form.cleaned_data['fecha_pago'],
														monto 				= form.cleaned_data['monto'],
														porcentaje_de_pago	= form.cleaned_data['porcentaje_de_pago'],
														tipo_de_pago		= form.cleaned_data['tipo_de_pago'],
														documento_deposito	= form.cleaned_data['documento_deposito'],
														responsable 		= form.cleaned_data['responsable'],
														pagado 				= form.cleaned_data['pagado'],
														)

				return render(request, "inicio/modal_ok.html", {'cabecera':"Operación exitosa", 'mensaje':"Los campos fueron actualizados correctamente"})
			except Exception, e:				
				print "Error: ", e
				mensaje = "El detalle de pago no pudo ser actualizado"
		else:
			mensaje = "Proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarDetallePagoForm(model_to_dict(detalle_pago))
	return render(request, 'inicio/detalle_pago_edit_1.html', {'form': form, 'id': detalle_pago.id, 'mensaje': mensaje})

#
# OPERACIONES DE HOMOLOGACION DE DOCUMENTOS
#
def homologacion(request):

	documentos = HomologacionDeDocs.objects.all().order_by('fecha')

	paginator = Paginator(documentos, 9)
	page = request.GET.get('page', 1)

	try:
		documentos = paginator.page(page)
	except PageNotAnInteger:
		documentos = paginator.page(1)
	except EmptyPage:
		documentos = paginator.page(paginator.num_pages)

	return render(request, 'inicio/homologacion.html', {'documentos':documentos}, context_instance=RequestContext(request))	

def crear_homologacion(request):
	if request.method=="POST":
		form = RegistrarHomologacionForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				homologacion = HomologacionDeDocs.objects.create(
															nombre 		= form.cleaned_data['nombre']
					  									  )

				_archivo = form.cleaned_data['archivo']
				if _archivo:
					homologacion.archivo = _archivo
					homologacion.save()

			except Exception, e:
				print "Error: ", e
				mensaje = "Algo fallo al guardar el registro, favor de reportarlo al area de sistemas."
			else:
				mensaje = "La homologacion ha sido creada exitosamente."
				return HttpResponseRedirect('/administracion/editar_homologacion/'+str(homologacion.id)+'/')
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarHomologacionForm()
	return render(request, 'inicio/homologacion_create.html', {'form': form, 'mensaje': mensaje})

class HomologacionDetailView(DetailView):
	
	template_name = "inicio/homologacion_detail.html"
	model = HomologacionDeDocs

	def get_object(self):
		object = super(HomologacionDetailView, self).get_object()
		return object

def editar_homologacion(request, pk):
	homologacion = HomologacionDeDocs.objects.get(id=int(pk))
	if request.method=="POST":
		form = RegistrarHomologacionForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				HomologacionDeDocs.objects.filter(pk=int(pk)).update(
																	nombre 		= form.cleaned_data['nombre']
					  												)

				_archivo = form.cleaned_data['archivo']
				if _archivo:
					if homologacion.archivo and os.path.isfile(homologacion.archivo.path):
						homologacion.archivo.delete()
					homologacion.archivo = _archivo
					homologacion.save()

			except Exception, e:				
				print "Error: ", e
				mensaje = "Los datos no pudieron ser actualizados."
			else:
				mensaje = "Datos actualizados correctamente."
		else:
			mensaje = "Por favor, proporcione los datos correctos."
	else:
		mensaje = ""
		form=RegistrarHomologacionForm(model_to_dict(homologacion))
	return render(request, 'inicio/homologacion_edit.html', {'form': form, 'mensaje': mensaje, 'homologacion': homologacion})


#
# FUNCION GENERAL PARA PONER EN HISTORICO CUALQUIER OBJETO
#

def en_historico(request):
	import json

	if not request.is_ajax():
		raise Http404

	modelo = request.POST.get('model', None)
	pk = request.POST.get('pk', -1)
	historico = request.POST.get('historico')

	try:
		if modelo == 'proyecto':
			proyecto = Proyectos.objects.filter(id=pk).update(historico=historico)

		elif modelo == 'anexotecnico':
			anexotecnico = AnexosTecnicos.objects.filter(id=pk)

			anexo = anexotecnico[0]
			if anexo.archivo:
				archivo = move_document(anexo.archivo, anexo)
				anexo.archivo.delete()
				anexo.archivo.name = '/'.join(archivo.split('/')[-3:])
				anexo.save()
			anexotecnico.update(historico=historico)

		elif modelo == 'convenio':
			convenio = Convenios.objects.filter(id=pk)
			
			_convenio = convenio[0]
			if _convenio.archivo:
				archivo = move_document(_convenio.archivo, _convenio)
				_convenio.archivo.delete()
				_convenio.archivo.name = '/'.join(archivo.split('/')[-3:])
				_convenio.save()

			convenio.update(historico=historico)

		elif modelo == 'contrato':
			contrato = Contratos.objects.filter(id=pk)
			_contrato = contrato[0]
			if _contrato.archivo:
				archivo = move_document(_contrato.archivo, _contrato)
				_contrato.archivo.delete()
				_contrato.archivo.name = '/'.join(archivo.split('/')[-3:])
				_contrato.save()
			
			contrato.update(historico=historico)

		elif modelo == 'propuesta':
			propuesta = Propuestas.objects.filter(id=pk)
			
			_propuesta = propuesta[0]
			if _propuesta.archivo:
				archivo = move_document(_propuesta.archivo, _propuesta)
				_propuesta.archivo.delete()
				_propuesta.archivo.name = '/'.join(archivo.split('/')[-3:])
				_propuesta.save()

			propuesta.update(historico=historico)

		elif modelo == 'entregable':
			entregable = Entregables.objects.filter(id=pk).update(historico=historico)

		elif modelo == 'detalle_entregable':
			detalle_entregable = DetallesEntregables.objects.filter(id=pk).update(historico=historico)
			_detalle_entregable = detalle_entregable[0]
			if _detalle_entregable.archivo:
				archivo = move_document(_detalle_entregable.archivo, _detalle_entregable)
				_detalle_entregable.archivo.delete()
				_detalle_entregable.archivo.name = '/'.join(archivo.split('/')[-3:])
				_detalle_entregable.save()

			detalle_entregable.update(historico=historico)

		elif modelo == 'doc_general':
			doc_general = DocumentosGenerales.objects.filter(id=pk).update(historico=historico)

		elif modelo == 'detalle_doc_general':
			detalle_doc_general = DetallesDocumentosGenerales.objects.filter(id=pk)

			_detalle_doc_general = detalle_doc_general[0]
			if _detalle_doc_general.archivo:
				archivo = move_document(_detalle_doc_general.archivo, _detalle_doc_general)
				_detalle_doc_general.archivo.delete()
				_detalle_doc_general.archivo.name = '/'.join(archivo.split('/')[-3:])
				_detalle_doc_general.save()

			detalle_doc_general.update(historico=historico)

		elif modelo == 'personal':
			personal = Personal.objects.filter(id=pk)
			persona = personal[0]
			if persona.credencial_elector:
				archivo = move_document(persona.credencial_elector, persona)
				persona.credencial_elector.delete()
				persona.credencial_elector.name = '/'.join(archivo.split('/')[-3:])
				persona.save()
			personal.update(historico=historico)

		elif modelo == 'detalle_pago_empleado':
			detalle_pago_empleado = DetallePagoEmpleado.objects.filter(id=pk)

			_detalle_pago_empleado = detalle_pago_empleadol[0]
			if _detalle_pago_empleado.archivo_documento_de_pago:
				archivo = move_document(_detalle_pago_empleado.archivo_documento_de_pago, _detalle_pago_empleado)
				_detalle_pago_empleado.archivo_documento_de_pago.delete()
				_detalle_pago_empleado.archivo_documento_de_pago.name = '/'.join(archivo.split('/')[-3:])
				_detalle_pago_empleado.save()

			detalle_pago_empleado.update(historico=historico)

		elif modelo == 'detalle_doc_responsiva':
			detalle_doc_responsiva = DetalleDocumentoResponsiva.objects.filter(id=pk)

			_detalle_doc_responsiva = detalle_doc_responsival[0]
			if _detalle_doc_responsiva.archivo_documento_responsiva:
				archivo = move_document(_detalle_doc_responsiva.archivo_documento_responsiva, _detalle_doc_responsiva)
				_detalle_doc_responsiva.archivo_documento_responsiva.delete()
				_detalle_doc_responsiva.archivo_documento_responsiva.name = '/'.join(archivo.split('/')[-3:])
				_detalle_doc_responsiva.save()

			detalle_doc_responsiva.update(historico=historico)


		elif modelo == 'cliente':
			cliente = Clientes.objects.filter(id=pk).update(historico=historico)
			1
		elif modelo == 'entidad':
			entidad = Entidades.objects.filter(id=pk).update(historico=historico)

		elif modelo == 'entidad_proyecto':
			entidad_proyecto = EntidadProyecto.objects.filter(id=pk).update(historico=historico)

		elif modelo == 'factura':
			factura = Facturas.objects.filter(id=pk)

			_factura = factural[0]
			if _factura.archivo_xml:
				archivo = move_document(_factura.archivo_xml, _factura)
				_factura.archivo_xml.delete()
				_factura.archivo_xml.name = '/'.join(archivo.split('/')[-3:])
				_factura.save()

			if _factura.archivo_fisico:
				archivo = move_document(_factura.archivo_fisico, _factura)
				_factura.archivo_fisico.delete()
				_factura.archivo_fisico.name = '/'.join(archivo.split('/')[-3:])
				_factura.save()

			factura.update(historico=historico)
		
		elif modelo == 'detalle_factura':
			detalle_factura = DetallesFacturas.objects.filter(id=pk).update(historico=historico)
		
		elif modelo == 'pago':
			pago = Pagos.objects.filter(id=pk).update(historico=historico)
		
		elif modelo == 'detalle_pago':
			detalle_pago = DetallePagos.objects.filter(id=pk)

			_detalle_pago = detalle_pagol[0]
			if _detalle_pago.documento_deposito:
				archivo = move_document(_detalle_pago.documento_deposito, _detalle_pago)
				_detalle_pago.documento_deposito.delete()
				_detalle_pago.documento_deposito.name = '/'.join(archivo.split('/')[-3:])
				_detalle_pago.save()

			detalle_pago.update(historico=historico)

	except Exception, e:	
		print "Error: ", e
		mensaje = {'mensaje': "Fallo la operación", 'error': True}
	else:
		mensaje = {'mensaje': "Operación exitosa", 'error': False}

	content = json.dumps(mensaje)
	http_response = HttpResponse(content, content_type="application/json")

	return http_response

#
# OPERACIONES CON ALARMAS
#
def crear_alarma(request):
	if request.method == 'POST':
		form = RegistrarAlarmaForm(request.POST)
		if form.is_valid():
			try:
				Alarmas.objects.create(
									emisor				= request.user,
									receptor 			= form.cleaned_data['receptor'],
									fecha_vencimiento	= form.cleaned_data['fecha_vencimiento'],
									mensaje				= form.cleaned_data['mensaje'],
										)
			except Exception, e:
				print "Error: ", e
				return render(request, "inicio/modal_error.html", {'cabecera':"Operación rechazada", 'mensaje':"La alarma no pudo ser creada."})		
			else:
				return render(request, "inicio/modal_ok.html", {'cabecera':"Alarma Generada", 'mensaje':"Alarma creada exitosamente."})		

	else:
		form = RegistrarAlarmaForm()
	return render(request, 'inicio/alarma_create.html', {'form': form})