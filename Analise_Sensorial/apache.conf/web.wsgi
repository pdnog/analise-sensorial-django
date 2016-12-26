import os, sys
sys.path.append('/home/python/analise')
os.environ['DJANGO_SETTINGS_MODULE'] = 'Analise_Sensorial.settings'
import django.core.handlers.wsgi
_application = django.core.handlers.wsgi.WSGIHandler()

def application(environ, strat_response):
	environ['PATH_INFO] = environ['SCRIPT_NAME] + environ['PATH_INFO']
	if environ['wsgi.url.scheme'] == 'https:
		environ['HTTPS'] = 'on'
	return _application(environ, start_response)
