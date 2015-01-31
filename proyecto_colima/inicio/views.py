#! -*- coding:utf-8 -*-

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

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

# Create your views here.

def registrar_proyecto(request):
	form = RegistrarProyectoForm()
	return render(request, 'inicio/registrar_proyecto.html', {'form': form}, context_instance=RequestContext(request))

def registrar_factura(request):
	form = FacturasForm()
	return render(request, 'inicio/registrar_factura.html', {'form': form}, context_instance=RequestContext(request))

def registrar_anexostecnicos(request):
	form = AnexosTecnicosForm()
	return render(request, 'inicio/registrar_anexostecnicos.html', {'form': form}, context_instance=RequestContext(request))

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

