# -*- coding: utf-8 -*-
# Django libs
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from django.utils.timezone import utc

from vademecum.models import Medicamento, MedicamentoPresentacion, PrincipioGrupo, \
	SubclaseNivel2, ClaseTerapeutica, TipoDiagnostico, Laboratorio, Clinica

from vademecum.views import unique_id

from datetime import timedelta, date, datetime

from optparse import make_option

class Command(BaseCommand):
	
	args = '<modelo ...>'
	help = 'Funcion para generar ids unicos de vademecum para los modelos'
	
	option_list = BaseCommand.option_list + (
		make_option('--empty',
			action='store_true',
			default=False,
			help='Solo modifica los elementos si su id de vademecum esta vacío'),
		)
	#To check the existence of a local variable:

	#if 'myVar' in locals():
	## myVar exists.

	#To check the existence of a global variable:

	#if 'myVar' in globals():
	## myVar exists.

	#To check if an object has an attribute:

	#if hasattr(obj, 'attr_name'):
	## obj.attr_name exists.

	def handle(self, *args, **options):
		time_init = datetime.utcnow().replace(tzinfo=utc)
		print 'Inicio',time_init
		
		sin_id = options.get('empty')
		
		nombradores = {
			'marca'       :{ 'modelo': Medicamento            , 'nombrador': lambda marca   : marca.nombre_medicamento  ,},
			'presentacion':{ 'modelo': MedicamentoPresentacion, 'nombrador': lambda med     : med.nombre_presentacion   ,},
			'principio'   :{ 'modelo': PrincipioGrupo         , 'nombrador': lambda prin    : prin.prigrup_nombre       ,},
			#'subclase'    :{ 'modelo': SubclaseNivel2         , 'nombrador': lambda subclase: subclase.titulo_vademecum ,},
			'clase'       :{ 'modelo': ClaseTerapeutica       , 'nombrador': lambda clase   : clase.nombre_clase        ,},
			'patologia'   :{ 'modelo': TipoDiagnostico        , 'nombrador': lambda td      : td.nombre_diagnostico     ,},
			'clinica'     :{ 'modelo': Clinica                , 'nombrador': lambda clinica : clinica.nombre_clinica    ,},
			'laboratorio' :{ 'modelo': Laboratorio            , 'nombrador': lambda lab     : lab.nombre_laboratorio    ,},
		}		
		
		modelos = args
		
		if modelos:
			for modelo in modelos:
				if modelo in nombradores:
					clase = nombradores[modelo]['modelo']
					nombrador = nombradores[modelo]['nombrador']
					if sin_id:
						if clase == Clinica:
							objetos_a_editar = clase.objects.filter(url_vademecum=None)
						else:
							objetos_a_editar = clase.objects.filter(id_vademecum=None)
					else:
						objetos_a_editar = clase.objects.all()
						
					for objeto in objetos_a_editar:
						if clase == Clinica:
							objeto.url_vademecum = unique_id(clase, nombrador(objeto))
						else:
							objeto.id_vademecum = unique_id(clase, nombrador(objeto))
						objeto.save()
				else:
					print "Modelo inexistente:",modelo
		
		else:
			for key,nombrador in nombradores.iteritems():
				if sin_id:
					if nombrador['modelo'] == Clinica:
						objetos_a_editar = nombrador['modelo'].objects.filter(url_vademecum=None)
					else:
						objetos_a_editar = nombrador['modelo'].objects.filter(id_vademecum=None)
				else:
					objetos_a_editar = nombrador['modelo'].objects.all()
				
				for objeto in objetos_a_editar:
					if nombrador['modelo'] == Clinica:
						objeto.url_vademecum = unique_id(nombrador['modelo'], nombrador['nombrador'](objeto))
					else:
						objeto.id_vademecum = unique_id(nombrador['modelo'], nombrador['nombrador'](objeto))
					objeto.save()
					
		time_end = datetime.utcnow().replace(tzinfo=utc)
		print 'Fin',time_end
		print 'Total',time_end - time_init
		
