#! -*- coding:utf-8 -*-

from django import forms
from inicio.models import ( Proyectos,
							Facturas,
							AnexosTecnicos,
							Contratos,
							Convenios,
							Propuestas,
							Empresas,
							Entregables,
							Personal
							)


class AuthForm(forms.Form):
    username = forms.CharField(required=True, max_length = 10, label=u'Usuario', widget = forms.TextInput(attrs = {'id':'usernames'}))  
    password = forms.CharField(required=True,label=u'Contraseña',widget=forms.PasswordInput(attrs = {'id':'elpassword'}))

class RegistrarProyectoForm(forms.ModelForm):
	class Meta:
		model = Proyectos

class FacturasForm(forms.ModelForm):
	class Meta:
		model = Facturas

class AnexosTecnicosForm(forms.ModelForm):
	class Meta:
		model = AnexosTecnicos

class ContratosForm(forms.ModelForm):
	class Meta:
		model = Contratos

class ConveniosForm(forms.ModelForm):
	class Meta:
		model = Convenios
		
class PropuestasForm(forms.ModelForm):
	class Meta:
		model = Propuestas

class EmpresasForm(forms.ModelForm):
	class Meta:
		model = Empresas

class EntregablesForm(forms.ModelForm):
	class Meta:
		model = Entregables

class PersonalForm(forms.ModelForm):
	class Meta:
		model= Personal