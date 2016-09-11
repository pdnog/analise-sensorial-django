from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import admin
from django.contrib.auth.forms import UserChangeForm
from webpage.forms import * 
from webpage.models import *

#Retirando registro de usuário
admin.site.unregister(User)

class FabricanteAdmin(UserAdmin):
	#Criando campos no administrador
	fieldsets = (
            (None, {'fields': ('username', 'password', 'first_name', 
            	'last_name', 'email', 'curso', 'ano',  'is_active') } ),
    	)
	#O que aparecerá na tabela de Fabricnates.
	list_display = ('username', 'email', 'first_name', 'last_name',)

admin.site.register(Fabricante, FabricanteAdmin)

class ProvadorAdmin(UserAdmin):
	#Criando campos no administrador
	fieldsets = (
            (None, {'fields': ('username', 'password', 'email', 'data_nascimento', 'is_active') } ),
    	)
	#O que aparecerá na tabela de Provador.
	list_display = ('username', 'email', 'first_name', 'last_name',)

admin.site.register(Provador, ProvadorAdmin)