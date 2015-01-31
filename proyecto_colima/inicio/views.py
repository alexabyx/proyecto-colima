#! -*- coding:utf-8 -*-
# Create your views here.

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.shortcuts import render, render_to_response, get_object_or_404
from django.conf import settings
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext

from inicio.forms import (	AuthForm, 
							RegistrarProyectoForm, 
							FacturasForm, 
							AnexosTecnicosForm, 
							ContratosForm, 
							ConveniosForm, 
							PropuestasForm, 
							EmpresasForm, 
							EntregablesForm, 
							PersonalForm
						  )

from inicio.models import ( AnexosTecnicos,
						  )

def registrar_proyecto(request):
	form = RegistrarProyectoForm()
	return render(request, 'inicio/registrar_proyecto.html', {'form': form}, context_instance=RequestContext(request))

def registrar_factura(request):
	form = FacturasForm()
	return render(request, 'inicio/registrar_factura.html', {'form': form}, context_instance=RequestContext(request))

#VIEWS PARA ANEXOS TECNICOS
def anexostecnicos(request):
	anexostecnicos_list = AnexosTecnicos.objects.all().order_by('-fecha_creacion')

	paginator = Paginator(anexostecnicos_list, 10)
	page = request.GET.get('page', 1)

	try:
		anexostecnicos = paginator.page(page)
	except PageNotAnInteger:
		anexostecnicos = paginator.page(1)
	except EmptyPage:
		anexostecnicos = paginator.page(paginator.num_pages)

	return render(request, 'inicio/anexostecnicos.html', {'anexostecnicos':anexostecnicos}, context_instance=RequestContext(request))

def agregar_anexotecnico(request):
	if request.method == "POST":
		form = AnexosTecnicosForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			mensaje = "Guardado"
			return render(request, 'inicio/agregar_anexotecnico.html', {'mensaje': mensaje}, context_instance=RequestContext(request))
	else:
		form = AnexosTecnicosForm()
	return render(request, 'inicio/agregar_anexotecnico.html', {'form':form}, context_instance=RequestContext(request))

def editar_anexotecnico(request, anexo_id):
	if request.method == "POST":
		form = AnexosTecnicosForm(request.POST)
		if form.is_valid():
			anexo = AnexosTecnicos.objects.get(id=anexo_id)
			anexo.numero_oficio = form.cleaned_data['numero_oficio']
			anexo.proyecto = form.cleaned_data['proyecto']
			anexo.tipo = form.cleaned_data['tipo']
			anexo.nombre = form.cleaned_data['nombre']
			anexo.siglas = form.cleaned_data['siglas']
			anexo.porcentaje = form.cleaned_data['porcentaje']
			anexo.fecha_creacion = form.cleaned_data['fecha_creacion']
			anexo.archivo = form.cleaned_data['archivo']
			anexo.save()
			mensaje = "Guardado"
			return render(request, 'inicio/editar_anexotecnico.html', {'mensaje': mensaje}, context_instance=RequestContext(request))
	else:					
		try:
			anexo = AnexosTecnicos.objects.get(id=anexo_id)
		except:
			anexo = None

		form = AnexosTecnicosForm(instance=anexo)	

	return render(request, 'inicio/editar_anexotecnico.html', {'form': form}, context_instance=RequestContext(request))

def eliminar_anexotecnico(request, anexo_id):
	try:
		anexo = AnexosTecnicos.objects.get(id=anexo_id)
		try:
			anexo.delete()
			mensaje = "Eliminado"
		except:
			mensaje = "Falló al eliminar"
	except:
		anexo = None
		mensaje = "Error inesperado"

	return render(request, 'inicio/eliminar_anexotecnico.html',{'mensaje': mensaje}, context_instance=RequestContext(request))

def registrar_contratos(request):
	form = ContratosForm()
	return render(request, 'inicio/registrar_contratos.html', {'form': form}, context_instance=RequestContext(request))

def registrar_convenios(request):
	form = ConveniosForm()
	return render(request, 'inicio/registrar_convenios.html', {'form': form}, context_instance=RequestContext(request))

def registrar_propuestas(request):
	form = PropuestasForm()
	return render(request, 'inicio/registrar_propuestas.html', {'form': form}, context_instance=RequestContext(request))

def registrar_empresa(request):
	form = EmpresasForm
	return render(request, 'inicio/registrar_empresa.html', {'form': form}, context_instance=RequestContext(request))

def registrar_entregable(request):
	form = EntregablesForm()
	return render(request, 'inicio/registrar_entregable.html', {'form': form}, context_instance=RequestContext(request))

def registrar_personal(request):
	form = PersonalForm()
	return render(request, 'inicio/registrar_personal.html', {'form': form}, context_instance=RequestContext(request))

def inicio(request):
	if request.method == "POST":
		form = AuthForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			try:
				usuario = authenticate(username = username, password=password)
			except:
				usuario = None
			print usuario
			if usuario is not None:
				if usuario.is_active:                        
					login(request, usuario)
					request.session.set_expiry(settings.TIEMPO_EXPIRACION_SESION)
					return HttpResponseRedirect('administrar_usuarios')
				else:
					mensaje = "Usuario inactivo"
					return render(request, 'inicio/login.html', {'form': form, 'mensaje': mensaje}, context_instance=RequestContext(request))					
			else:
				mensaje = "Usuario o contraseña incorrectos"
				return render(request, 'inicio/login.html', {'form': form, 'mensaje': mensaje}, context_instance=RequestContext(request))
		else:
			return render(request, 'inicio/login.html', {'form': form }, context_instance=RequestContext(request))
	else:
		form = AuthForm()
	return render(request, 'inicio/login.html', {'form': form }, context_instance=RequestContext(request))

@login_required(login_url="/inicio")
def administrar_usuarios(request):
	return render(request, 'inicio/administrar_usuarios.html',{},context_instance=RequestContext(request))

