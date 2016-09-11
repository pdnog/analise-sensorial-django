"""Analise_Sensorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add animport:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from webpage.views import *
from Fabricante.views import *
from Provador.views import *
from Fabricante.pdf import *

urlpatterns = [
#  Para login e cadastro
    url(r'^admin/', admin.site.urls),
    url(r'^$', Inicio, name="principal"),
    url(r'^Provador', Provador_page_cadastro),
    url(r'^Fabricante', Fabricante_page_cadastro),
    url(r'^Cadastro_Fabricante/$', Cadastro_Fabricante),
    url(r'^Cadastro_Provador/$', Cadastro_Provador),
    url(r'^Cadastro_principal_page', Cadastro_principal_page),
    url(r'^testeModal', Teste),
    url(r'^Login', Login),
    url(r'^Logout', Logout),
    url(r'^Inicio', Inicio),

    #Para fabricante
    url(r'^Funcionalidades', Funcionalidades),
    url(r'^Form_Dados_Analise_Page', FormDadosAnalise_Page),
    url(r'^CadastrarFormAnalise', CadastrarFormAnalise),
    #url(r'^Perguntas/(?P<id>[^\.]+)', cadastrarPerguntas),
    #url(r'^PerguntaDissertativa/(?P<id>[^\.]+)', cadastrarPerguntaDissertativa),
    #url(r'^PerguntaSimNao/(?P<id>[^\.]+)', cadastrarPerguntaSimNao),
    #url(r'^RetornaFormulario/(?P<id>[^\.]+)', retornaFormulario),
    #Edição dos dados do Fabricante
    url(r'^Perguntas/(?P<id>[^\.]+)', page_perguntas),
    url(r'^GoEdit', editaRed),
    #Edição dos dados das análises
    url(r'^EditarAnalise/(?P<id>[^\.]+)', editaAnalise),
    #Deletando
    url(r'^DeletarAnalise/(?P<id>[^\.]+)', deletar_analise),
    url(r'^NumerosAnalise/(?P<id>[^\.]+)/numeros', gerar_teste_page),
    url(r'^GerarAmostras/(?P<id>[^\.]+)/salvar', gerar_amostras_action),
    #Mostra análises
    url(r'^MostraAnalise', retornaAnalises),
    url(r'^GerarPdf/(?P<id>[^\.]+)', criando_estrutura),
    url(r'^SalvarPergunta/(?P<id>[^\.]+)', cadastrar_pergunta),
    url(r'^EditarPergunta/(?P<id>[^\.]+)', editarPergunta),
    url(r'^DeletarPergunta/(?P<id>[^\.]+)', deletarPergunta),

    #Para provador
    url(r'^Home_Provador', home_provador),
    url(r'^page_respostas/(?P<id>[^\.]+)', page_respostas),

]
