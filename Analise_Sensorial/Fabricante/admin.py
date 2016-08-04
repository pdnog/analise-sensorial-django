from django.contrib import admin
from Fabricante.models import *
# Register your models here.

class AnaliseSensorialAdmin(admin.ModelAdmin):
	list_display = ('nome', 'descricao', 'user')
	search_fields = ('nome', 'user')
	ordering = ('nome',)

class TesteAdmin(admin.ModelAdmin):
	list_display = ('id','analise',)
	ordering = ('analise',)

class AmostraAdmin(admin.ModelAdmin):
	list_display = ('numero', 'tipo')
	ordering = ('numero',)

admin.site.register(AnaliseSensorial, AnaliseSensorialAdmin)
admin.site.register(Teste, TesteAdmin)
admin.site.register(Amostra, AmostraAdmin)

		
