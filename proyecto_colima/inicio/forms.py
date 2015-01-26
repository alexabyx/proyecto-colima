#! -*- coding:utf-8 -*-

from django import forms

class AuthForm(forms.Form):
    username = forms.CharField(required=True, max_length = 10, label=u'Usuario', widget = forms.TextInput(attrs = {'id':'usernames'}))  
    password = forms.CharField(required=True,label=u'Contraseña',widget=forms.PasswordInput(attrs = {'id':'elpassword'}))