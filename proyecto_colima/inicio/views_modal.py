#! -*- coding:utf-8 -*-

from django.shortcuts import render

def modal_ok(request):
	cabecera = request.GET.get('cabecera', "Operación realizada")
	mensaje = request.GET.get('mensaje', "La operación se realizó exitosamente.")
	return render(request, 'inicio/modal_ok.html', {'cabecera': cabecera, 'mensaje':mensaje})

def modal_aviso(request):
	cabecera = request.GET.get('cabecera', "Confirmación")
	mensaje = request.GET.get('mensaje', "¿Está seguro de querer realizar esta operación?")
	return render(request, 'inicio/modal_aviso.html', {'cabecera': cabecera, 'mensaje':mensaje})

def modal_error(request):
	cabecera = request.GET.get('cabecera', "Operación rechazada")
	mensaje = request.GET.get('mensaje', "La operación no fue completada.")
	print cabecera, mensaje, "Error"
	return render(request, 'inicio/modal_error.html', {'cabecera': cabecera, 'mensaje':mensaje})