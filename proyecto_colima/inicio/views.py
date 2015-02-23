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
						  )
#
#==================OPERACIONES DE PROYECTOS========================
#

@login_required(login_url='/')
def proyectos(request):
	proyectos_list = Proyectos.objects.filter(habilitado=True)

	paginator = Paginator(proyectos_list, 9)
	page = request.GET.get('page', 1)

	try:
		proyectos = paginator.page(page)
	except PageNotAnInteger:
		proyectos = paginator.page(1)
	except EmptyPage:
		proyectos = paginator.page(paginator.num_pages)

	return render(request, 'inicio/proyectos.html', {'proyectos': proyectos}, context_instance=RequestContext(request))

class ProyectoDetailView(DetailView):
	
	template_name = "inicio/proyecto_detail.html"
	model = Proyectos

	def get_object(self):
		object = super(ProyectoDetailView, self).get_object()
		return object

	def get_context_data(self, **kwargs):
		context = super(ProyectoDetailView, self).get_context_data(**kwargs)

		context['entregables'] = Entregables.objects.filter(proyecto=self.get_object(), habilitado=True)

		return context

@login_required(login_url='/')
def editar_proyecto(request, pk):
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

				return HttpResponseRedirect('/administracion/proyectos/')
			except Exception, e:				
				print "Error: ", e
				mensaje = "El proyecto no pudo ser actualizado"
		else:
			print "No paso Proyectos"
	else:

		form=RegistrarProyectoForm(model_to_dict(proyecto))
	entregables = Entregables.objects.filter(proyecto = proyecto, habilitado=True).order_by('total')
	anexostecnicos = AnexosTecnicos.objects.filter(proyecto=proyecto, habilitado=True).order_by('-fecha_creacion')
	convenios = Convenios.objects.filter(proyecto=proyecto, habilitado=True).order_by('-fecha_creacion')
	contratos = Contratos.objects.filter(proyecto=proyecto, habilitado=True).order_by('-fecha_creacion')
	propuestas = Propuestas.objects.filter(proyecto=proyecto, habilitado=True).order_by('-fecha_creacion')
	doc_generales = DocumentosGenerales.objects.filter(proyecto=proyecto).order_by('-fecha_creacion')

	return render(request, 'inicio/proyecto_edit.html', {'form': form,
														 'entregables': entregables, 
														 'anexostecnicos': anexostecnicos, 
														 'convenios': convenios,
														 'contratos': contratos,
														 'propuestas': propuestas,
														 'doc_generales': doc_generales})

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
def crear_proyecto(request):
	if request.method=="POST":
		form = RegistrarProyectoForm(request.POST)
		if form.is_valid():
			proyecto = Proyectos.objects.create(
												nombre = form.cleaned_data['nombre'],
												siglas = form.cleaned_data['siglas'],
												fecha_inicio = form.cleaned_data['fecha_inicio'],
												fecha_fin = form.cleaned_data['fecha_fin'],
												avance = form.cleaned_data['avance'],
												comentario = form.cleaned_data['comentario'],
												cliente = form.cleaned_data['cliente'],
												)
			print form.cleaned_data['responsable']
			for responsable in form.cleaned_data['responsable']:
				proyecto.responsable.add(responsable)
			proyecto.save()

			mensaje = "El proyecto ha sido creado exitosamente"
			return HttpResponseRedirect('/administracion/proyectos/')
		else:
			print "No paso"
	else:
		form=RegistrarProyectoForm()
	return render(request, 'inicio/proyecto_create.html', {'form': form})

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

#
#==================OPERACIONES DE FACTURAS========================
#
@login_required(login_url='/')
def facturas(request):
	facturas_list = Facturas.objects.all()

	paginator = Paginator(facturas_list, 9)
	page = request.GET.get('page', 1)

	try:
		facturas = paginator.page(page)
	except PageNotAnInteger:
		facturas = paginator.page(1)
	except EmptyPage:
		facturas = paginator.page(paginator.num_pages)

	return render(request, 'inicio/facturas.html', {'facturas': facturas}, context_instance=RequestContext(request))


class FacturaDetailView(DetailView):
	
	template_name = "inicio/factura_detail.html"
	model = Facturas

	def get_object(self):
		object = super(FacturaDetailView, self).get_object()
		return object

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
															tipo 				= form.cleaned_data['tipo'],
															nombre 				= form.cleaned_data['nombre'],
															siglas 				= form.cleaned_data['siglas'],
															numero_factura 		= form.cleaned_data['numero_factura'],
															fecha_factura 		= form.cleaned_data['fecha_factura'],
															folio_venta 		= form.cleaned_data['folio_venta'],
															rfc 				= form.cleaned_data['rfc'],
															direccion 			= form.cleaned_data['direccion'],
															subtotal 			= form.cleaned_data['subtotal'],
															iva 				= form.cleaned_data['iva'],
															total_con_numero 	= form.cleaned_data['total_con_numero'],
															total_con_letra 	= form.cleaned_data['total_con_letra'],
															pagada 				= form.cleaned_data['pagada'],
															archivo_xml 		= form.cleaned_data['archivo_xml'],
															archivo_fisico 		= form.cleaned_data['archivo_fisico'],
															)

				return HttpResponseRedirect('/administracion/facturas/')
			except Exception, e:				
				print "Error: ", e
				mensaje = "La factura no pudo ser actualizada"
		else:
			print "No paso"
	else:
		form=RegistrarFacturaForm(model_to_dict(factura))
	detalle_facturas = DetallesFacturas.objects.filter(factura=factura)
	return render(request, 'inicio/factura_edit.html', {'form': form,
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
															tipo 				= form.cleaned_data['tipo'],
															nombre 				= form.cleaned_data['nombre'],
															siglas 				= form.cleaned_data['siglas'],
															numero_factura 		= form.cleaned_data['numero_factura'],
															fecha_factura 		= form.cleaned_data['fecha_factura'],
															folio_venta 		= form.cleaned_data['folio_venta'],
															rfc 				= form.cleaned_data['rfc'],
															direccion 			= form.cleaned_data['direccion'],
															subtotal 			= form.cleaned_data['subtotal'],
															iva 				= form.cleaned_data['iva'],
															total_con_numero 	= form.cleaned_data['total_con_numero'],
															total_con_letra 	= form.cleaned_data['total_con_letra'],
															pagada 				= form.cleaned_data['pagada'],
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

@login_required(login_url='/')
def crear_factura(request):
	if request.method=="POST":
		form = RegistrarFacturaForm(request.POST, request.FILES)
		if form.is_valid():
			factura = Facturas.objects.create(
												contrato 			= form.cleaned_data['contrato'],
												responsable 		= form.cleaned_data['responsable'],
												tipo 				= form.cleaned_data['tipo'],
												nombre 				= form.cleaned_data['nombre'],
												siglas 				= form.cleaned_data['siglas'],
												numero_factura 		= form.cleaned_data['numero_factura'],
												fecha_factura 		= form.cleaned_data['fecha_factura'],
												folio_venta 		= form.cleaned_data['folio_venta'],
												rfc 				= form.cleaned_data['rfc'],
												direccion 			= form.cleaned_data['direccion'],
												subtotal 			= form.cleaned_data['subtotal'],
												iva 				= form.cleaned_data['iva'],
												total_con_numero 	= form.cleaned_data['total_con_numero'],
												total_con_letra 	= form.cleaned_data['total_con_letra'],
												pagada 				= form.cleaned_data['pagada'],
												archivo_xml 		= form.cleaned_data['archivo_xml'],
												archivo_fisico 		= form.cleaned_data['archivo_fisico'],
												)

			mensaje = "La factura ha sido creada exitosamente"
			return HttpResponseRedirect('/administracion/facturas/')

		else:
			print "No paso"
	else:
		form=RegistrarFacturaForm()
	return render(request, 'inicio/factura_create.html', {'form': form})


#
#==================OPERACIONES DE DETALLES DE FACTURAS========================
#
@login_required(login_url='/')
def detalle_facturas(request):
	detalle_facturas_list = DetallesFacturas.objects.all()

	paginator = Paginator(detalle_facturas_list, 9)
	page = request.GET.get('page', 1)

	try:
		detalle_facturas = paginator.page(page)
	except PageNotAnInteger:
		detalle_facturas = paginator.page(1)
	except EmptyPage:
		detalle_facturas = paginator.page(paginator.num_pages)

	return render(request, 'inicio/detalle_facturas.html', {'detalle_facturas': detalle_facturas}, context_instance=RequestContext(request))

class DetalleFacturaDetailView(DetailView):
	
	template_name = "inicio/detalle_factura_detail.html"
	model = DetallesFacturas

	def get_object(self):
		object = super(DetalleFacturaDetailView, self).get_object()
		return object

@login_required(login_url='/')
def editar_detalle_factura(request, pk):
	if request.method=="POST":
		form = RegistrarDetalleFacturaForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				DetallesFacturas.objects.filter(id=int(pk)).update(
																factura 		= form.cleaned_data['factura'],
																descripcion 	= form.cleaned_data['descripcion'],
																cantidad 		= form.cleaned_data['cantidad'],
																)

				return HttpResponseRedirect('/administracion/detalle_facturas/')
			except Exception, e:				
				print "Error: ", e
				mensaje = "La factura no pudo ser actualizada"
		else:
			print "No paso"
	else:
		detalle_factura = DetallesFacturas.objects.get(id=int(pk))
		form=RegistrarDetalleFacturaForm(model_to_dict(detalle_factura))
	return render(request, 'inicio/detalle_factura_edit.html', {'form': form})


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


@login_required(login_url='/')
def crear_detalle_factura(request):
	if request.method=="POST":
		form = RegistrarDetalleFacturaForm(request.POST, request.FILES)
		if form.is_valid():
			detalle_factura = DetallesFacturas.objects.create(
															factura 		= form.cleaned_data['factura'],
															descripcion 	= form.cleaned_data['descripcion'],
															cantidad 		= form.cleaned_data['cantidad'],
															)

			mensaje = "La factura ha sido creada exitosamente"
			return HttpResponseRedirect('/administracion/detalle_facturas/')

		else:
			print "No paso"
	else:
		form=RegistrarDetalleFacturaForm()
	return render(request, 'inicio/detalle_factura_create.html', {'form': form})

#
#==================OPERACIONES DE ANEXOSTECNICOS========================
#

@login_required(login_url='/')
def anexostecnicos(request):
	anexostecnicos_list = AnexosTecnicos.objects.filter(habilitado=True).order_by('-fecha_creacion')

	paginator = Paginator(anexostecnicos_list, 9)
	page = request.GET.get('page', 1)

	try:
		anexostecnicos = paginator.page(page)
	except PageNotAnInteger:
		anexostecnicos = paginator.page(1)
	except EmptyPage:
		anexostecnicos = paginator.page(paginator.num_pages)

	return render(request, 'inicio/anexostecnicos.html', {'anexostecnicos':anexostecnicos}, context_instance=RequestContext(request))


@login_required(login_url='/')
def crear_anexotecnico(request):
	if request.method=="POST":
		form = RegistrarAnexotecnicoForm(request.POST, request.FILES)
		if form.is_valid():
			anexotecnico = AnexosTecnicos.objects.create(
														numero_oficio 	= form.cleaned_data['numero_oficio'],	
														proyecto 		= form.cleaned_data['proyecto'],
														nombre 			= form.cleaned_data['nombre'],
														siglas 			= form.cleaned_data['siglas'],
														status 			= form.cleaned_data['status'],
														archivo         = form.cleaned_data['archivo'],
														)

			mensaje = "El anexotecnico ha sido creado exitosamente"
			return HttpResponseRedirect('/administracion/anexostecnicos/')
		else:
			print "No paso"
	else:
		form=RegistrarAnexotecnicoForm()
	return render(request, 'inicio/anexotecnico_create.html', {'form': form})


@login_required(login_url='/')
def editar_anexotecnico(request, pk):
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

				return HttpResponseRedirect('/administracion/anexostecnicos/')
			except Exception, e:				
				print "Error: ", e
				mensaje = "El anexotecnico no pudo ser actualizado"
		else:
			print "No paso"
	else:
		anexotecnico = AnexosTecnicos.objects.get(id=int(pk))
		form=RegistrarAnexotecnicoForm(model_to_dict(anexotecnico))
	return render(request, 'inicio/anexotecnico_edit.html', {'form': form})


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

#
#==================OPERACIONES DE CONTATOS========================
#


@login_required(login_url='/')
def contratos(request):
	contratos_list = Contratos.objects.filter(habilitado=True).order_by('-fecha_creacion')

	paginator = Paginator(contratos_list, 9)
	page = request.GET.get('page', 1)

	try:
		contratos = paginator.page(page)
	except PageNotAnInteger:
		contratos = paginator.page(1)
	except EmptyPage:
		contratos = paginator.page(paginator.num_pages)

	return render(request, 'inicio/contratos.html', {'contratos':contratos}, context_instance=RequestContext(request))

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
			contrato = Contratos.objects.create(
												numero_oficio 	= form.cleaned_data['numero_oficio'],	
												proyecto 		= form.cleaned_data['proyecto'],
												encargado 		= form.cleaned_data['encargado'],
												archivo         = form.cleaned_data['archivo'],
												)

			mensaje = "El contrato ha sido creado exitosamente"
			return HttpResponseRedirect('/administracion/contratos/')
		else:
			print "No paso"
	else:
		form=RegistrarContratoForm()
	return render(request, 'inicio/contrato_create.html', {'form': form})

@login_required(login_url='/')
def editar_contrato(request, pk):
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

				return HttpResponseRedirect('/administracion/contratos/')
			except Exception, e:				
				print "Error: ", e
				mensaje = "El contrato no pudo ser actualizado"
		else:
			print "No paso"
	else:
		contrato = Contratos.objects.get(id=int(pk))
		form=RegistrarContratoForm(model_to_dict(contrato))
	facturas = Facturas.objects.filter(contrato=contrato).order_by('numero_factura', '-fecha_factura')
	return render(request, 'inicio/contrato_edit.html', {'form': form,
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
#==================OPERACIONES DE CONVENIOS========================
#
@login_required(login_url='/')
def convenios(request):
	convenios_list = Convenios.objects.filter(habilitado=True).order_by('-fecha_creacion')

	paginator = Paginator(convenios_list, 9)
	page = request.GET.get('page', 1)

	try:
		convenios = paginator.page(page)
	except PageNotAnInteger:
		convenios = paginator.page(1)
	except EmptyPage:
		convenios = paginator.page(paginator.num_pages)

	return render(request, 'inicio/convenios.html', {'convenios':convenios}, context_instance=RequestContext(request))

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
			convenio = Convenios.objects.create(
												numero 		= form.cleaned_data['numero'],
												proyecto 	= form.cleaned_data['proyecto'],
												encargado 	= form.cleaned_data['encargado'],
												archivo 	= form.cleaned_data['archivo'],
												)

			mensaje = "El convenio ha sido creado exitosamente"
			return HttpResponseRedirect('/administracion/convenios/')
		else:
			print "No paso"
	else:
		form=RegistrarConvenioForm()
	return render(request, 'inicio/convenio_create.html', {'form': form})

@login_required(login_url='/')
def editar_convenio(request, pk):
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

				return HttpResponseRedirect('/administracion/convenios/')
			except Exception, e:				
				print "Error: ", e
				mensaje = "El convenio no pudo ser actualizado"
		else:
			print "No paso"
	else:
		convenio = Convenios.objects.get(id=int(pk))
		form=RegistrarConvenioForm(model_to_dict(convenio))
	return render(request, 'inicio/convenio_edit.html', {'form': form})

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
		contrato = Convenios.objects.filter(id=pk).update(habilitado=False)
	except Exception, e:
		print "Error: ", e
		mensaje = {'mensaje': "Fallo la operación", 'error': True}
	else:
		mensaje = {'mensaje': "Operación exitosa", 'error': False}

	content = json.dumps(mensaje)
	http_response = HttpResponse(content, content_type="application/json")

	return http_response

#
#==================OPERACIONES DE PROPUESTAS========================
#
@login_required(login_url='/')
def propuestas(request):
	propuestas_list = Propuestas.objects.filter(habilitado=True).order_by('-fecha_creacion')

	paginator = Paginator(propuestas_list, 9)
	page = request.GET.get('page', 1)

	try:
		propuestas = paginator.page(page)
	except PageNotAnInteger:
		propuestas = paginator.page(1)
	except EmptyPage:
		propuestas = paginator.page(paginator.num_pages)

	return render(request, 'inicio/propuestas.html', {'propuestas':propuestas}, context_instance=RequestContext(request))

class PropuestaDetailView(DetailView):
	
	template_name = "inicio/propuesta_detail.html"
	model = Propuestas

	def get_object(self):
		object = super(PropuestaDetailView, self).get_object()
		return object

@login_required(login_url='/')
def crear_propuesta(request):
	if request.method=="POST":
		form = RegistrarPropuestaForm(request.POST)
		if form.is_valid():
			propuestas = Propuestas.objects.create(
												numero_oficio 	= form.cleaned_data['numero_oficio'],
												proyecto 		= form.cleaned_data['proyecto'],
												responsable 	= form.cleaned_data['responsable'],
												)

			mensaje = "La propuesta ha sido creada exitosamente"
			return HttpResponseRedirect('/administracion/propuestas/')
		else:
			print "No paso"
	else:
		form=RegistrarPropuestaForm()
	return render(request, 'inicio/propuesta_create.html', {'form': form})

@login_required(login_url='/')
def editar_propuesta(request, pk):
	if request.method=="POST":
		form = RegistrarPropuestaForm(request.POST)
		if form.is_valid():
			try:
				Propuestas.objects.filter(id=int(pk)).update(
															numero_oficio 	= form.cleaned_data['numero_oficio'],
															proyecto 		= form.cleaned_data['proyecto'],
															responsable 	= form.cleaned_data['responsable'],
															)

				return HttpResponseRedirect('/administracion/propuestas/')
			except Exception, e:				
				print "Error: ", e
				mensaje = "El convenio no pudo ser actualizado"
		else:
			print "No paso"
	else:
		propuesta = Propuestas.objects.get(id=int(pk))
		form=RegistrarPropuestaForm(model_to_dict(propuesta))
	return render(request, 'inicio/propuesta_edit.html', {'form': form})

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
#==================OPERACIONES DE PERSONAL========================
#
@login_required(login_url='/')
def personal(request):
	personal_list = Personal.objects.filter(habilitado=True).order_by('-fecha_ingreso')

	paginator = Paginator(personal_list, 9)
	page = request.GET.get('page', 1)

	try:
		personal = paginator.page(page)
	except PageNotAnInteger:
		personal = paginator.page(1)
	except EmptyPage:
		personal = paginator.page(paginator.num_pages)

	return render(request, 'inicio/personal.html', {'personal':personal}, context_instance=RequestContext(request))

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
			personal = Personal.objects.create(	
												rfc 						= form.cleaned_data['rfc'],
												credencial_elector 			= form.cleaned_data['credencial_elector'],
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

			mensaje = "El empleado ha sido creada exitosamente"
			return HttpResponseRedirect('/administracion/personal/')
		else:
			print "No paso"
	else:
		form=RegistrarPersonalForm()
	return render(request, 'inicio/personal_create.html', {'form': form})

@login_required(login_url='/')
def editar_personal(request, pk):
	personal = Personal.objects.get(id=int(pk))

	if request.method=="POST":
		form = RegistrarPersonalForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				Personal.objects.filter(id=int(pk)).update(
															rfc 						= form.cleaned_data['rfc'],
															credencial_elector 			= form.cleaned_data['credencial_elector'],
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

				return HttpResponseRedirect('/administracion/personal/')
			except Exception, e:				
				print "Error: ", e
				mensaje = "El convenio no pudo ser actualizado"
		else:
			print "No paso"
	else:
		form=RegistrarPersonalForm(model_to_dict(personal))

	convenios = Convenios.objects.filter(encargado=personal, habilitado=True).order_by('-fecha_creacion')
	contratos = Contratos.objects.filter(encargado=personal, habilitado=True).order_by('-fecha_creacion')
	entregables = Entregables.objects.filter(responsable=personal, habilitado=True).order_by('total')
	propuestas = Propuestas.objects.filter(responsable=personal, habilitado=True).order_by('-fecha_creacion')
	detalles_doc_generales = DetallesDocumentosGenerales.objects.filter(responsable=personal).order_by('-fecha_creacion')
	detalles_doc_responsiva = DetalleDocumentoResponsiva.objects.filter(personal=personal)
	detalles_pago_empleado = DetallePagoEmpleado.objects.filter(personal=personal)
	facturas = Facturas.objects.filter(responsable=personal).order_by('-fecha_factura')
	return render(request, 'inicio/personal_edit.html', {'form': form,
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
#==================OPERACIONES DE CLIENTES========================
#
@login_required(login_url='/')
def clientes(request):
	clientes_list = Clientes.objects.filter(habilitado=True).order_by('-fecha_creacion')

	paginator = Paginator(clientes_list, 9)
	page = request.GET.get('page', 1)

	try:
		clientes = paginator.page(page)
	except PageNotAnInteger:
		clientes = paginator.page(1)
	except EmptyPage:
		clientes = paginator.page(paginator.num_pages)

	return render(request, 'inicio/clientes.html', {'clientes':clientes}, context_instance=RequestContext(request))

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
			cliente = Clientes.objects.create(
												nombre 	= form.cleaned_data['nombre'],
												siglas	= form.cleaned_data['siglas'],
												)

			mensaje = "El cliente ha sido creada exitosamente"
			return HttpResponseRedirect('/administracion/clientes/')
		else:
			print "No paso"
	else:
		form=RegistrarClienteForm()
	return render(request, 'inicio/cliente_create.html', {'form': form})

@login_required(login_url='/')
def editar_cliente(request, pk):
	if request.method=="POST":
		form = RegistrarClienteForm(request.POST)
		if form.is_valid():
			try:
				Clientes.objects.filter(id=int(pk)).update(
															nombre 	= form.cleaned_data['nombre'],
															siglas	= form.cleaned_data['siglas'],
															)

				return HttpResponseRedirect('/administracion/clientes/')
			except Exception, e:				
				print "Error: ", e
				mensaje = "El cliente no pudo ser actualizado"
		else:
			print "No paso"
	else:
		cliente = Clientes.objects.get(id=int(pk))
		form=RegistrarClienteForm(model_to_dict(cliente))
	proyectos = Proyectos.objects.filter(cliente=cliente, habilitado=True).order_by('-fecha_inicio')

	return render(request, 'inicio/cliente_edit.html', {'form': form,
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
#==================OPERACIONES DE ENTIDADES========================
#

@login_required(login_url='/')
def entidades(request):
	entidades_list = Entidades.objects.filter(habilitado=True).order_by('-fecha_creacion')

	paginator = Paginator(entidades_list, 9)
	page = request.GET.get('page', 1)

	try:
		entidades = paginator.page(page)
	except PageNotAnInteger:
		entidades = paginator.page(1)
	except EmptyPage:
		entidades = paginator.page(paginator.num_pages)

	return render(request, 'inicio/entidades.html', {'entidades':entidades}, context_instance=RequestContext(request))

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
			entidad = Entidades.objects.create(
												nombre 	= form.cleaned_data['nombre'],
												siglas 	= form.cleaned_data['siglas'], 
												tipo 	= form.cleaned_data['tipo'],
												)

			mensaje = "La entidad ha sido creada exitosamente"
			return HttpResponseRedirect('/administracion/entidades/')
		else:
			print "No paso"
	else:
		form=RegistrarEntidadForm()
	return render(request, 'inicio/entidad_create.html', {'form': form})

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

				return HttpResponseRedirect('/administracion/entidades/')
			except Exception, e:				
				print "Error: ", e
				mensaje = "La entidad no pudo ser actualizada"
		else:
			print "No paso"
	else:
		form=RegistrarEntidadForm(model_to_dict(entidad))
	entidades_proyectos = EntidadProyecto.objects.filter(entidad=entidad)
	return render(request, 'inicio/entidad_edit.html', {'form': form, 'entidades_proyectos': entidades_proyectos})	

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
#==================OPERACIONES DE ENTIDADES PRYECTO========================
#
@login_required(login_url='/')
def entidades_proyecto(request):
	entidades_proyecto_list = EntidadProyecto.objects.all()
	
	paginator = Paginator(entidades_proyecto_list, 9)
	page = request.GET.get('page', 1)

	try:
		entidades_proyecto = paginator.page(page)
	except PageNotAnInteger:
		entidades_proyecto = paginator.page(1)
	except EmptyPage:
		entidades_proyecto = paginator.page(paginator.num_pages)

	return render(request, 'inicio/entidades_proyecto.html', {'entidades_proyecto':entidades_proyecto}, context_instance=RequestContext(request))

class EntidadProyectoDetailView(DetailView):
	
	template_name = "inicio/entidad_detail.html"
	model = Entidades

	def get_object(self):
		object = super(EntidadProyectoDetailView, self).get_object()
		return object

@login_required(login_url='/')
def crear_entidad_proyecto(request):
	if request.method=="POST":
		form = RegistrarEntidadProyectoForm(request.POST)
		if form.is_valid():
			entidad = EntidadProyecto.objects.create(
													entidad 	= form.cleaned_data['entidad'],
													proyecto 	= form.cleaned_data['proyecto'],
													porcentaje  = form.cleaned_data['porcentaje'],
													)

			mensaje = "La entidad ha sido creada exitosamente"
			return HttpResponseRedirect('/administracion/entidades_proyecto/')
		else:
			print "No paso"
	else:
		form=RegistrarEntidadProyectoForm()
	return render(request, 'inicio/entidad_proyecto_create.html', {'form': form})

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

				return HttpResponseRedirect('/administracion/entidades_proyecto/')
			except Exception, e:				
				print "Error: ", e
				mensaje = "La entidad no pudo ser actualizada"
		else:
			print "No paso"
	else:
		entidad_proyecto = EntidadProyecto.objects.get(id=int(pk))
		form=RegistrarEntidadProyectoForm(model_to_dict(entidad_proyecto))
	return render(request, 'inicio/entidad_proyecto_edit.html', {'form': form})	

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
#==================OPERACIONES DE ENTREGABLES========================
#
@login_required(login_url='/')
def entregables(request):
	entregables_list = Entregables.objects.filter(habilitado=True).order_by('-proyecto__fecha_inicio')

	paginator = Paginator(entregables_list, 9)
	page = request.GET.get('page', 1)

	try:
		entregables = paginator.page(page)
	except PageNotAnInteger:
		entregables = paginator.page(1)
	except EmptyPage:
		entregables = paginator.page(paginator.num_pages)

	return render(request, 'inicio/entregables.html', {'entregables':entregables}, context_instance=RequestContext(request))

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
			entregable = Entregables.objects.create(
													proyecto 	= form.cleaned_data['proyecto'],
													responsable = form.cleaned_data['responsable'],
													total 		= form.cleaned_data['total'],
													)

			mensaje = "El entregable ha sido creado exitosamente"
			return HttpResponseRedirect('/administracion/entregables/')
		else:
			print "No paso"
	else:
		form=RegistrarEntregableForm()
	return render(request, 'inicio/entregable_create.html', {'form': form})


@login_required(login_url='/')
def editar_entregable(request, pk):
	entregable = Entregables.objects.get(id=int(pk))	
	if request.method=="POST":
		form = RegistrarEntregableForm(request.POST)
		print "POST_1", request.POST
		if form.is_valid():
			try:
				Entregables.objects.filter(id=int(pk)).update(
															proyecto 	= form.cleaned_data['proyecto'],
															responsable = form.cleaned_data['responsable'],
															total 		= form.cleaned_data['total'],
															)

				return HttpResponseRedirect('/administracion/entregables/')
			except Exception, e:				
				print "Error: ", e
				mensaje = "El entregable no pudo ser actualizado"
		else:
			print "No paso"
	else:
		form=RegistrarEntregableForm(model_to_dict(entregable))

	detalles_entregables = DetallesEntregables.objects.filter(entregable=entregable)
	return render(request, 'inicio/entregable_edit.html', {'form': form, 'detalles_entregables': detalles_entregables})


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
	detalles_entregables_list = DetallesEntregables.objects.all().order_by('-fecha_creacion')

	paginator = Paginator(detalles_entregables_list, 9)
	page = request.GET.get('page', 1)

	try:
		detalles_entregables = paginator.page(page)
	except PageNotAnInteger:
		detalles_entregables = paginator.page(1)
	except EmptyPage:
		detalles_entregables = paginator.page(paginator.num_pages)

	return render(request, 'inicio/detalle_entregables.html', {'detalles_entregables':detalles_entregables}, context_instance=RequestContext(request))

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
			detalle_entregable = DetallesEntregables.objects.create(
																	entregable 		= form.cleaned_data['entregable'],
																	responsable 	= form.cleaned_data['responsable'],
																	numero 			= form.cleaned_data['numero'],
																	nombre 			= form.cleaned_data['nombre'],
																	siglas 			= form.cleaned_data['siglas'],
																	archivo 		= form.cleaned_data['archivo'],
																	)

			mensaje = "El detalle ha sido creado exitosamente"
			return HttpResponseRedirect('/administracion/detalle_entregables/')
		else:
			print "No paso"
	else:
		form=RegistrarDetalleEntregableForm()
	return render(request, 'inicio/detalle_entregable_create.html', {'form': form})

@login_required(login_url='/')
def editar_detalle_entregable(request, pk):
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
																	archivo 		= form.cleaned_data['archivo'],
																	)


			except Exception, e:				
				print "Error: ", e
				mensaje = "El entregable no pudo ser actualizado"
		else:
			mensaje="Los datos son incorrectos"
	else:
		detalle_entregable = DetallesEntregables.objects.get(id=int(pk))
		form=RegistrarDetalleEntregableForm(model_to_dict(detalle_entregable))
	return render(request, 'inicio/detalle_entregable_edit.html', {'form': form})

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
		form=RegistrarDetalleEntregableForm(model_to_dict(detalle_entregable))
		mensaje = None
	return render(request, 'inicio/detalle_entregable_edit_1.html', {'form': form, 'id': detalle_entregable.id, 'mensaje':mensaje})	


#
#==================OPERACIONES DE DOCS GENERALES========================
#
@login_required(login_url='/')
def docs_generales(request):
	docs_generales_list = DocumentosGenerales.objects.all().order_by('-fecha_creacion')

	paginator = Paginator(docs_generales_list, 9)
	page = request.GET.get('page', 1)

	try:
		docs_generales = paginator.page(page)
	except PageNotAnInteger:
		docs_generales = paginator.page(1)
	except EmptyPage:
		docs_generales = paginator.page(paginator.num_pages)

	return render(request, 'inicio/docs_generales.html', {'doc_generales':docs_generales}, context_instance=RequestContext(request))

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
			doc_general = DocumentosGenerales.objects.create(
															proyecto 	= form.cleaned_data['proyecto'], 
															clave 		= form.cleaned_data['clave'],
															)

			mensaje = "El documento ha sido creado exitosamente"
			return HttpResponseRedirect('/administracion/doc_generales/')
		else:
			print "No paso"
	else:
		form=RegistrarDocGeneralForm()
	return render(request, 'inicio/doc_general_create.html', {'form': form})

@login_required(login_url='/')
def editar_doc_general(request, pk):
	if request.method=="POST":
		form = RegistrarDocGeneralForm(request.POST)
		if form.is_valid():
			try:
				DocumentosGenerales.objects.filter(id=int(pk)).update(
																		proyecto 	= form.cleaned_data['proyecto'],
																		clave 		= form.cleaned_data['clave'],
																	)

				return HttpResponseRedirect('/administracion/doc_generales/')
			except Exception, e:				
				print "Error: ", e
				mensaje = "El entregable no pudo ser actualizado"
		else:
			print "No paso"
	else:
		doc_general = DocumentosGenerales.objects.get(id=int(pk))
		form=RegistrarDocGeneralForm(model_to_dict(doc_general))
	return render(request, 'inicio/doc_general_edit.html', {'form': form})

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
																	proyecto 	= form.cleaned_data['proyecto'], 
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
	detalle_docs_generales_list = DetallesDocumentosGenerales.objects.all().order_by('-fecha_creacion')

	paginator = Paginator(detalle_docs_generales_list, 9)
	page = request.GET.get('page', 1)

	try:
		detalle_docs_generales = paginator.page(page)
	except PageNotAnInteger:
		detalle_docs_generales = paginator.page(1)
	except EmptyPage:
		detalle_docs_generales = paginator.page(paginator.num_pages)

	return render(request, 'inicio/detalle_docs_generales.html', {'detalle_docs_generales':detalle_docs_generales}, context_instance=RequestContext(request))

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
			detalle_doc_general = DetallesDocumentosGenerales.objects.create(
																			documentos_generales 	= form.cleaned_data['documentos_generales'],
																			responsable 			= form.cleaned_data['responsable'],
																			numero 					= form.cleaned_data['numero'],
																			nombre 					= form.cleaned_data['nombre'],
																			siglas 					= form.cleaned_data['siglas'],
																			archivo 				= form.cleaned_data['archivo'],
																			)

			mensaje = "El detalle ha sido creado exitosamente"
			return HttpResponseRedirect('/administracion/detalle_docs_generales/')
		else:
			print "No paso"
	else:
		form=RegistrarDetalleDocGeneralForm()
	return render(request, 'inicio/detalle_doc_general_create.html', {'form': form})

@login_required(login_url='/')
def editar_detalle_doc_general(request, pk):
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
				return HttpResponseRedirect('/administracion/detalle_docs_generales/')
			except Exception, e:				
				print "Error: ", e
				mensaje = "El entregable no pudo ser actualizado"
		else:
			mensaje = "Los datos son invalidos."
			print "No paso"
	else:
		detalle_doc_general = DetallesDocumentosGenerales.objects.get(id=int(pk))
		form=RegistrarDetalleDocGeneralForm(model_to_dict(detalle_doc_general))
	return render(request, 'inicio/detalle_doc_general_edit.html', {'form': form})

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
#==================OPERACIONES DE DETALLES DE DOCUMENTOS RESPONSIVA========================
#

@login_required(login_url='/')
def detalle_doc_responsiva(request):
	detalle_doc_responsiva_list = DetalleDocumentoResponsiva.objects.all()

	paginator = Paginator(detalle_doc_responsiva_list, 9)
	page = request.GET.get('page', 1)

	try:
		detalles_doc_responsiva = paginator.page(page)
	except PageNotAnInteger:
		detalles_doc_responsiva = paginator.page(1)
	except EmptyPage:
		detalles_doc_responsiva = paginator.page(paginator.num_pages)

	return render(request, 'inicio/detalles_doc_responsiva.html', {'detalles_doc_responsiva':detalles_doc_responsiva}, context_instance=RequestContext(request))

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
		if form.is_valid():
			detalle_doc_responsiva = DetalleDocumentoResponsiva.objects.create(
																				personal 						= form.cleaned_data['personal'],
																				archivo_documento_responsiva 	= form.cleaned_data['archivo_documento_responsiva'],
																				)

			mensaje = "El detalle ha sido creado exitosamente"
			return HttpResponseRedirect('/administracion/detalles_doc_responsiva/')
		else:
			print "No paso"
	else:
		form=RegistrarDetalleDocResponsivaForm()
	return render(request, 'inicio/detalle_doc_responsiva_create.html', {'form': form})

@login_required(login_url='/')
def editar_detalle_doc_responsiva(request, pk):
	if request.method=="POST":
		form = RegistrarDetalleDocResponsivaForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				DetalleDocumentoResponsiva.objects.filter(id=int(pk)).update(
																			personal 						= form.cleaned_data['personal'],
																			archivo_documento_responsiva 	= form.cleaned_data['archivo_documento_responsiva'],
																			)

				return HttpResponseRedirect('/administracion/detalles_doc_responsiva/')
			except Exception, e:				
				print "Error: ", e
				mensaje = "El entregable no pudo ser actualizado"
		else:
			print "No paso"
	else:
		detalle_doc_general = DetalleDocumentoResponsiva.objects.get(id=int(pk))
		form=RegistrarDetalleDocResponsivaForm(model_to_dict(detalle_doc_general))
	return render(request, 'inicio/detalle_doc_responsiva_edit.html', {'form': form})

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
#==================OPERACIONES DE DETALLE DE PAGO EMPLEADO========================
#
@login_required(login_url='/')
def detalles_pago_empleado(request):
	detalles_pago_empleado_list = DetallePagoEmpleado.objects.all()

	paginator = Paginator(detalles_pago_empleado_list, 9)
	page = request.GET.get('page', 1)

	try:
		detalles_pago_empleado = paginator.page(page)
	except PageNotAnInteger:
		detalles_pago_empleado = paginator.page(1)
	except EmptyPage:
		detalles_pago_empleado = paginator.page(paginator.num_pages)

	return render(request, 'inicio/detalles_pago_empleado.html', {'detalles_pago_empleado':detalles_pago_empleado}, context_instance=RequestContext(request))

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
			detalle_pago_empleado = DetallePagoEmpleado.objects.create(
																	personal 					= form.cleaned_data['personal'],
																	responsable 				= form.cleaned_data['responsable'],
																	archivo_documento_de_pago 	= form.cleaned_data['archivo_documento_de_pago'],
																	)

			mensaje = "El detalle ha sido creado exitosamente"
			return HttpResponseRedirect('/administracion/detalles_pago_empleado/')
		else:
			print "No paso"
	else:
		form=RegistrarPagoEmpleadoForm()
	return render(request, 'inicio/detalle_pago_empleado_create.html', {'form': form})

@login_required(login_url='/')
def editar_detalle_pago_empleado(request, pk):
	if request.method=="POST":
		form = RegistrarPagoEmpleadoForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				DetallePagoEmpleado.objects.filter(id=int(pk)).update(
																	personal 					= form.cleaned_data['personal'],
																	responsable 				= form.cleaned_data['responsable'],
																	archivo_documento_de_pago 	= form.cleaned_data['archivo_documento_de_pago'],
																	)

				return HttpResponseRedirect('/administracion/detalles_pago_empleado/')
			except Exception, e:				
				print "Error: ", e
				mensaje = "El detalle no pudo ser actualizado"
		else:
			print "No paso"
	else:
		detalle_pago_empleado = DetallePagoEmpleado.objects.get(id=int(pk))
		form=RegistrarPagoEmpleadoForm(model_to_dict(detalle_pago_empleado))
	return render(request, 'inicio/detalle_pago_empleado_edit.html', {'form': form})

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