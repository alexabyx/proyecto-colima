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
from django.http import HttpResponseRedirect, Http404

from inicio.forms import (	AuthForm, 
						 )

def login_web(request):
	if request.method == "POST":
		form = AuthForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			url_redirect = request.POST.get('next', reverse_lazy('administracion:index'))

			try:
				usuario = authenticate(username = username, password=password)
			except:
				usuario = None

			if usuario is not None:
				if usuario.is_active:                        
					login(request, usuario)
					request.session.set_expiry(settings.TIEMPO_EXPIRACION_SESION)
					if url_redirect:
						return HttpResponseRedirect(url_redirect)						
					else:
						return HttpResponseRedirect(reverse_lazy('index'))
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
		url_redirect = request.GET.get('next')		
	return render(request, 'inicio/login.html', {'form': form, 'next': url_redirect }, context_instance=RequestContext(request))

@login_required(login_url='/')
def logout_web(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/')
def administracion(request):
	return render(request, 'inicio/administracion.html',{},context_instance=RequestContext(request))