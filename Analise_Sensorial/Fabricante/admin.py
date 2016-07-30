from django.contrib import admin
from Fabricante.models import *
# Register your models here.

class AnaliseAdmin(admin.ModelAdmin):
	list_display = ('Nome', 'Descricao', 'user')
	search_fields = ('Nome', 'user')
	ordering = ('Nome',)

admin.site.register(Analise_Dados_Pessoais, AnaliseAdmin)
