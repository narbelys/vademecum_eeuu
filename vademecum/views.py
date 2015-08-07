# -*- coding: utf-8 -*-

import string
import json
import re
from collections import OrderedDict

# Django libs
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.db.models import Q, Count, Sum
from django.http import HttpResponse, Http404
from django.utils import simplejson
from django.core import serializers
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.utils.translation import ugettext as _, ugettext_noop as _noop

# Modelos
from vademecum.models import AuditRelpatologia, ClaseTerapeutica, PrincipioActivo, PrincipioGrupo, PrincipioSubclase, Medicamento, MedicamentoPresentacion, Laboratorio, TipoDiagnostico
from vademecum.models import SintomaEnfermedad, Sintoma, SubclaseNivel3 , SubclaseNivel2 , CausaEnfermedad, Causa, RankingClase, RankingSubclase, RankingMarca, RankingMedicamento, RankingPrincipioActivo, RankingEnfermedad
from vademecum.models import CausaEnfermedad, Causa, TipoDiagnosticorelacion, TipoDiagnostico2, AuditMedicamento, Clinica, Pais, Seo, MarcaIndicaciones, Idioma
import smtplib
from email.MIMEText import MIMEText
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from django.core.mail import send_mail, BadHeaderError
from email.mime.multipart import MIMEMultipart
from django.core.mail import EmailMessage
from django.core import mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

def getTOP20Marcas(pais):
	top20marcas = MedicamentoPresentacion.objects.\
		filter(pais = pais).\
		exclude(id_medicamento__nombre_medicamento__icontains=' ').\
		values_list('id_medicamento', flat=True).distinct()[:20]
	top20marcas_aux = [int(i) for i in top20marcas]
	top20marcas = Medicamento.objects.filter(pk__in=top20marcas_aux)
	
	return top20marcas

def getTOP20Medicamentos(pais):
	top20medicamentos = MedicamentoPresentacion.objects.filter(pais = pais).distinct()[:20]
	
	return top20medicamentos
	
def getLanguageCode(req):
	try:
		lang_code = req.LANGUAGE_CODE
		multilanguage = True
	except:
		try:
			lang_code = settings.LANGUAGE_CODE
		except:
			lang_code = 'es'
		finally:
			multilanguage = False
		
	regexp_es = re.compile('^es($|\-[a-z]{2}$)')
	regexp_en = re.compile('^en($|\-[a-z]{2}$)')
	if regexp_es.match(lang_code):
		idioma = Idioma.objects.get(iso_alpha__iexact='es')
	elif regexp_en.match(lang_code):
		idioma = Idioma.objects.get(iso_alpha__iexact='en')
	else:
		#Español por defecto
		idioma = Idioma.objects.get(iso_alpha__iexact='es')

	return lang_code, multilanguage, idioma
	

def getPaisVademecum():
	try:
		pais = Pais.objects.get(iso_alpha = settings.PAIS_VADEMECUM)
	except:
		pais = Pais.objects.get(pk=1) #Venezuela
	return pais
	
def getIdiomaPrincipios():
	try:
		if settings.IDIOMA_PRINCIPIOS == 'ES':
			idioma = 1
		elif settings.IDIOMA_PRINCIPIOS == 'EN':
			idioma = 2
		else: # Español por defecto
			idioma = 1
	except: # Español por defecto
		idioma = 1
	return idioma

def paginacionGenerador(page, paginator):
	
	pags = []
	elementos_paginados = []
	
	try:
		elementos_paginados = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		page = 1
		elementos_paginados = paginator.page(page)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		page = paginator.num_pages
		elementos_paginados = paginator.page(page)
		
	page = int(page)
	if 1 not in range( page-2, page+3 ):
		pags.append( 1 )
		if page not in [i for i in range(1,5)] : pags.append( '...' )
	for n in range( page-2, page+3):
		if n in paginator.page_range:
			pags.append( n )
	if paginator.num_pages not in range( page-2, page+3):
		if page not in [paginator.num_pages-i for i in range(1,4)]: pags.append( '...' )
		pags.append( paginator.num_pages )
		
	return (pags, elementos_paginados)

# ESTO ES UNA COCHINADA DE VARIABLE GLOBAL
#try:
	#metatag_base = Seo.objects.get(pais = getPaisVademecum(), pagina= 'Home', idioma)
#except:
	#metatag_base = None
	
def getMetatagBase(idioma, pais):
	try:
		metatag_base = Seo.objects.get(pais = pais, pagina= 'Home', idioma=idioma)
	except:
		#Espaniol por defecto, si no consigue.
		try:
			metatag_base = Seo.objects.get(pais = pais, pagina= 'Home', idioma__pk=1)
		except:
			metatag_base = None

	
letters_global = [{'show':i,'ref':i} for i in string.uppercase]
letters_global.append({'show':'#','ref':'others'})

def getPaisesActivos():
	paises = Pais.objects.filter(Q(iso_alpha = settings.PAIS_VADEMECUM) | Q(activo = True))
	nombres = []
	for pais in paises:
		pais_nombre= _(pais.pais_nombre)
		nombres.append({'pais':pais, 'nombre':pais_nombre})
	return (paises,nombres)

def contacto(request):
	if request.is_ajax():
		comentario = request.POST.get('comentario',None)
		print "holaaaaa"
		combinado = 'Mensaje de FB vademecum \r\n\r\nComentario: '+comentario
		msg = MIMEText(combinado.encode('utf-8'), 'plain', 'UTF-8')
		msg['From']= "vademecum"
		#msg['MIME-Version']="1.0"
		Subject="Mensaje de FB"
		#msg['Content-Type'] = "text/html; charset=utf-8"
		#msg['Content-Transfer-Encoding'] = "quoted-printable"
		#msg = 'From: '+nombre+' <'+email+'>\r\nTo: miguelmiguel19@gmail.com\r\n\r\n'+comentario
					
		if comentario:
			try:
				#send_mail('(Comentario) PCA-Audit', nombre+' <'+email+'>. Comentario: '+comentario, email,['miguel.ambrosio@pcaaudit.com'], fail_silently=False)
				
				conexion = mail.get_connection()
				conexion.password = settings.ALT_EMAIL_HOST_PASSWORD
				conexion.username = settings.ALT_EMAIL_HOST_USER
				conexion.host = settings.ALT_EMAIL_HOST
				conexion.port = settings.EMAIL_PORT
				conexion.use_tls = settings.EMAIL_USE_TLS
				conexion.open()

				#\"url\": \"https://pcafarma.com\" Si se quiere agregar landing page poner esto dentro del settings del header
				correo = EmailMessage(Subject, combinado, "Contacto FB <contacto@prxcontrolsolutions.com>", ['contacto@pcafarma.com'], headers = {"X-SMTPAPI": "{\"filters\": {\"subscriptiontrack\": {\"settings\":{\"enable\": 1, \"text/html\": \"Si usted quiere darse de baja y dejar de recibir estos correos, por favor haga <% click aqui %>.\" , \"text/plain\": \"Si usted quiere darse de baja y dejar de recibir estos correos, por favor haga click aqui <% %>.\" }}}}"} ,connection=conexion )

				correo.send()
				conexion.close()
				#server = smtplib.SMTP_SSL('smtp.gmail.com',465)
				#server.login('info@pcaaudit.com', 'prxinfo2012')
				#server.sendmail(email,['info@pcaaudit.com'], str(msg))
				#server.quit()
				return HttpResponse(json.JSONEncoder().encode({"comentario":comentario}), mimetype="application/json")
			except (smtplib.SMTPAuthenticationError):#BadHeaderError:
				print 'Error de header'
	else:
		raise Http404


def crear_id_vademecum(nombre):
	"""Quita los caracteres especiales de los nombres de los datos en cuestión."""
	return nombre.replace(" ", "_").replace(",", "_").replace("/", "_").replace(".", "").\
		replace(u"´", "").replace("-", "_").replace("+", "_").replace("%", "").replace(u"°", "").\
		replace("*", "").replace("&", "and").replace("[", "").replace("]", "").replace("{", "").\
		replace("}", "").replace("'","").replace('"',"").replace("(", "").replace(")", "").\
		replace(u'º',"").replace(';','').replace(':','').replace(u'`','').replace(u'^','').\
		replace('#',"").replace('>',"").replace('<',"").replace(u'?','').replace(u'¿','').\
		replace(u'!','').replace(u'¡','').lower()

def unique_id(clase,nombre):
	"""Crea un id_vademecum único a partir del nombre del elemento en cuestion, para nombres repetidos se añade _ al final"""
	
	next = True
	dummy =''

	while next:
		string = nombre+dummy
		id_vademecum = crear_id_vademecum(string)

		if clase == Clinica:
			elems = clase.objects.filter(url_vademecum=id_vademecum)
		else:
			elems = clase.objects.filter(id_vademecum=id_vademecum)

		next = len(elems) > 0
		dummy += "_"

	return id_vademecum

def vade_unique(nombre):
	"""Crea un id_vademecum único a partir del nombre del elemento en cuestion, para nombres repetidos se añade _ al final"""
	
	next = True
	dummy =''

	while next:
		string = nombre+dummy
		id_vademecum = crear_id_vademecum(string)

		
		#elems = Medicamento.objects.filter(id_vademecum=id_vademecum)
		#elems = MedicamentoPresentacion.objects.filter(id_vademecum=id_vademecum)
		#elems = PrincipioGrupo.objects.filter(id_vademecum=id_vademecum)
		#elems = SubclaseNivel2.objects.filter(id_vademecum=id_vademecum)
		#elems = ClaseTerapeutica.objects.filter(id_vademecum=id_vademecum)
		#elems = TipoDiagnostico.objects.filter(id_vademecum=id_vademecum)
		#elems = Laboratorio.objects.filter(id_vademecum=id_vademecum)
		#elems = Clinica.objects.filter(url_vademecum=id_vademecum)

		next = len(elems) > 0
		dummy += "_"

	return id_vademecum

# HOME
@ensure_csrf_cookie
def index(request, nombre=None):
	pais = getPaisVademecum()
	paises_activos, nombres_paises  = getPaisesActivos()
	
	lang_code, multilanguage, idioma = getLanguageCode(request)
	metatag_base = getMetatagBase(idioma, pais)
	#print "BASE", metatag_base.title
	
	"""
	Para crear los id_vademecum, descomentar uno por uno, y descomentar la linea correspondiente según el caso en vade_unique
	"""

	#marcas = Medicamento.objects.all()
	#for marca in marcas:
		#print "procesando ",marca.nombre_medicamento
		#marca.id_vademecum = vade_unique(marca.nombre_medicamento)
		#marca.save()

	##meds = MedicamentoPresentacion.objects.all().order_by('nombre_presentacion')
	#meds = MedicamentoPresentacion.objects.all()
	#for med in meds:
		#print "procesando ",med.nombre_presentacion
		
		#med.id_vademecum = vade_unique(med.nombre_presentacion)
		###med.id_vademecum = vade_unique(med.nombre_presentacion +"_"+med.id_laboratorio.abrev_laboratorio)
		#med.save()
		## OJO: NO DESCOMENTAR!!!
		## Se utilizó join en vez de concatenación de string buscando mayor eficiencia y NO se logró!
		##med.id_vademecum = vade_unique( u"_".join([med.nombre_presentacion, med.id_laboratorio.abrev_laboratorio]) )	

	#principios = PrincipioGrupo.objects.all()
	#for prin in principios:
		#print "procesando ",prin.prigrup_nombre
		#prin.id_vademecum = vade_unique(prin.prigrup_nombre)
		#prin.save()	

	##Para Subclase 2 se debe correr el script con los nombres de la base de datos anterior
	#subclases = SubclaseNivel2.objects.all()
	#for subclase in subclases:
		#print "procesando ",subclase.titulo_vademecum
		#subclase.id_vademecum = vade_unique(subclase.titulo_vademecum)
		#subclase.save()	

	#clases = ClaseTerapeutica.objects.all()
	#for clase in clases:
		#print "procesando ",clase.nombre_clase
		#clase.id_vademecum = vade_unique(clase.nombre_clase)
		#clase.save()

	#tds = TipoDiagnostico.objects.all()
	#for td in tds:
		#print "procesando ",td.nombre_diagnostico
		#td.id_vademecum = vade_unique(td.nombre_diagnostico)
		#td.save()

	#labs = Laboratorio.objects.all()
	#for lab in labs:
		#print "procesando ",lab.nombre_laboratorio
		#lab.id_vademecum = vade_unique(lab.nombre_laboratorio)
		#lab.save()

	#clinicas = Clinica.objects.all()
	#for clinica in clinicas:
		#print "procesando ",clinica.nombre_clinica
		#clinica.url_vademecum = vade_unique(clinica.nombre_clinica)
		#clinica.save()


	#nombradores = [
		#{ 'modelo': Medicamento            , 'nombrador': lambda marca   : marca.nombre_medicamento                                             },
		#{ 'modelo': MedicamentoPresentacion, 'nombrador': lambda med     : med.nombre_presentacion + "_" + med.id_laboratorio.abrev_laboratorio },
		#{ 'modelo': PrincipioGrupo         , 'nombrador': lambda prin    : prin.prigrup_nombre                                                  },
		#{ 'modelo': SubclaseNivel2         , 'nombrador': lambda subclase: subclase.titulo_vademecum                                            },
		#{ 'modelo': ClaseTerapeutica       , 'nombrador': lambda clase   : clase.nombre_clase                                                   },
		#{ 'modelo': TipoDiagnostico        , 'nombrador': lambda td      : td.nombre_diagnostico                                                },
		#{ 'modelo': Laboratorio            , 'nombrador': lambda lab     : lab.nombre_laboratorio                                               },
	#]

	#for nombrador in nombradores:
		#for objeto in nombrador['modelo'].objects.all()
			#objeto.id_vademecum = vade_unique(clase, nombrador['nombrador'](objeto))
			#objeto.save()


	#top10meds = RankingMedicamento.objects.all().order_by('-total')[:20]
	top10enfs = RankingEnfermedad.objects.all().order_by('-total')[:20]
		
	top20marcas = getTOP20Marcas(pais)
	top10meds = getTOP20Medicamentos(pais)
	
	return render_to_response(
		'home.html', 
		{
			"pais":pais,
			"meds":top10meds, 
			"enfs":top10enfs, 
			"top20marcas":top20marcas, 
			"activos": paises_activos, "nombres_paises": nombres_paises, 
			"metatag_base": metatag_base,
			"idioma":idioma,
			"multilanguage" :multilanguage,
		}, 
		context_instance=RequestContext(request)
	)

@ensure_csrf_cookie
def buscar(request, nombre=None):
	lang_code, multilanguage, idioma = getLanguageCode(request)
	pais = getPaisVademecum()
	
	metatag_base = getMetatagBase(idioma, pais)
	
	paises_activos, nombres_paises  = getPaisesActivos()
	buscar = request.GET.get("buscar", None)
	top20marcas = getTOP20Marcas(pais)

	return render_to_response(
		'buscar.html', 
		{
			"pais":pais, 
			"top20marcas":top20marcas, 
			"buscar":buscar, 
			"activos": paises_activos, "nombres_paises": nombres_paises, 
			"metatag_base": metatag_base,
			"idioma":idioma,
			"multilanguage" :multilanguage,
		}, 
		context_instance=RequestContext(request)
	)

def ajax_buscar(request, nombre=None):
	if request.is_ajax():
		pais = getPaisVademecum()
		idioma = getIdiomaPrincipios()
		
		buscar = request.POST.get("buscar", None)

		resultados = []

		if buscar:
			principios = PrincipioGrupo.objects.filter(prigrup_nombre__icontains=buscar, idioma=idioma)
			#if nombre:
				#pais=Pais.objects.get(pais_nombre="PANAMA")
				#meds = MedicamentoPresentacion.objects.filter(nombre_presentacion__icontains=buscar, pais=pais)
			#else:
			meds = MedicamentoPresentacion.objects.filter(nombre_presentacion__icontains=buscar, pais=pais)
			enfs = TipoDiagnostico.objects.filter(nombre_diagnostico__icontains=buscar)
			
			if pais.iso_alpha == 'VE':
				clinicas = Clinica.objects.filter(nombre_clinica__icontains=buscar)
			else:
				clinicas = []
			
			results = []
			for prin in principios:
				results.append( dict(nombre=prin.prigrup_nombre, id_vademecum="/PrincipiosActivos/"+prin.id_vademecum) )

			for med in meds:
				results.append( dict(nombre=med.nombre_presentacion, id_vademecum="/Medicamentos/"+med.id_vademecum) )

			for enf in enfs:
				results.append( dict(nombre=enf.nombre_diagnostico, id_vademecum="/Enfermedades/"+enf.id_vademecum) )
				
			for clinica in clinicas:
				#Cambiar clinica.id_clinica por id_vademecum
				results.append( dict(nombre=clinica.nombre_clinica, id_vademecum="/Clinicas/"+clinica.url_vademecum) )

			# Resultados por orden alfabético
			resultados = sorted(results, key=lambda k: k['nombre']) 

			json_data = simplejson.dumps(resultados)
			return HttpResponse(json_data, mimetype="application/json")

		return HttpResponse(serializers.serialize('json', resultados, ensure_ascii=False), mimetype="application/json")
	else:
		raise Http404


# INDEX
@ensure_csrf_cookie
def blogs(request):
	lang_code, multilanguage, idioma = getLanguageCode(request)
	pais=getPaisVademecum()
	
	metatag_base = getMetatagBase(idioma, pais)
	
	paises_activos, nombres_paises  = getPaisesActivos()
	top20marcas = getTOP20Marcas(pais)
	return render_to_response(
		'blogs.html',
		{
			"pais":pais, 
			"top20marcas":top20marcas, 
			"activos": paises_activos, "nombres_paises": nombres_paises, 
			"metatag_base": metatag_base, 
			"idioma":idioma,
			"multilanguage" :multilanguage,
		}, 
		context_instance=RequestContext(request)
	)

@ensure_csrf_cookie
def clinicas(request,id=None):
	lang_code, multilanguage, idioma = getLanguageCode(request)
	pais = getPaisVademecum()
	
	metatag_base = getMetatagBase(idioma, pais)
	
	paises_activos, nombres_paises  = getPaisesActivos()
	if id==None:
		top20marcas = getTOP20Marcas(pais)

		clinic = Clinica.objects.all().order_by('nombre_clinica')
		
		paginator = Paginator(clinic, 20) 
		page = request.GET.get('page')
	
		pags, clinicas = paginacionGenerador(page, paginator)
		
		return render_to_response(
			'clinicas_paginator.html',
			{
				"pais":pais, 
				"clinicas":clinicas, 
				"top20marcas":top20marcas, 
				"activos": paises_activos, "nombres_paises": nombres_paises, 
				"metatag_base": metatag_base,
				"pags": pags,
				"idioma":idioma,
				"multilanguage" :multilanguage,
			}, 
			context_instance=RequestContext(request)
		)
	else:
		top20marcas = getTOP20Marcas(pais)
		clinica =get_object_or_404( Clinica, url_vademecum=id )
			
		#return render_to_response('clinicasPrueba.html',{"clinica":clinica, "top20marcas":top20marcas}, context_instance=RequestContext(request))

		return render_to_response(
			'ver_clinica.html',
			{
				"pais":pais, 
				"clinica":clinica, 
				"top20marcas":top20marcas, 
				"activos": paises_activos, "nombres_paises": nombres_paises, 
				"metatag_base": metatag_base, 
				"idioma":idioma,
				"multilanguage" :multilanguage,
			}, 
			context_instance=RequestContext(request)
		)

@ensure_csrf_cookie
def otros_paises(request, nombre=None, letra=None):
	lang_code, multilanguage, idioma = getLanguageCode(request)
	pais = getPaisVademecum()
	
	metatag_base = getMetatagBase(idioma, pais)
	
	paises_activos, nombres_paises  = getPaisesActivos()
	print nombre
	top20marcas = getTOP20Marcas(pais)
	return render_to_response(
		'otros_paises.html',
		{
			"pais":pais, 
			"letra":letra, 
			"letters":string.uppercase, 
			"top20marcas":top20marcas, 
			"activos": paises_activos, "nombres_paises": nombres_paises, 
			"metatag_base": metatag_base, 
			"idioma":idioma,
			"multilanguage" :multilanguage,
		}, 
		context_instance=RequestContext(request)
	)

def ajax_marcas_paises(request):
	#pais_otros=Pais.objects.filter(pais_id__in=[1,2])
	pais = getPaisVademecum()
	
	if request.is_ajax():
		marcas = []
		ranking = request.POST.get("ranking", None)
		if ranking:
			marcas_rank = RankingMarca.objects.all().order_by('-total')
			for marca in marcas_rank:
				marcas.append( marca.marca )
		else:
			#pais_otros=Pais.objects.filter(pais_id__in=[1,2])
			letra = request.POST.get("letra", None)
			if letra:
				marcas=MedicamentoPresentacion.objects.filter(Q(id_medicamento__nombre_medicamento__startswith=letra) & ~Q(pais = pais) & Q(pais__activo=True)).order_by('id_medicamento__nombre_medicamento').values('id_medicamento__nombre_medicamento', 'pais__pais_nombre', 'pais', 'pais__flag', 'pais__link', 'id_medicamento__id_vademecum').distinct()  
				#marcas = Medicamento.objects.filter(nombre_medicamento__startswith=letra).order_by('nombre_medicamento')
			else:
				marcas=MedicamentoPresentacion.objects.filter( ~Q(pais = pais) & Q(pais__activo=True) ).order_by('id_medicamento__nombre_medicamento').values('id_medicamento__nombre_medicamento', 'pais__pais_nombre', 'pais', 'pais__flag', 'pais__link', 'id_medicamento__id_vademecum').distinct()

		#print "antesss", marcas
		return HttpResponse(json.JSONEncoder().encode({'data': list(marcas)}), mimetype="application/json")
		#return HttpResponse(serializers.serialize('json', marcas, ensure_ascii=False), mimetype="application/json")
	else:
		raise Http404
	
@ensure_csrf_cookie
def marcas_otros_paises(request, letra=None, otros=None):
	lang_code, multilanguage, idioma = getLanguageCode(request)
	pais = getPaisVademecum()
	
	metatag_base = getMetatagBase(idioma, pais)
	
	paises_activos, nombres_paises  = getPaisesActivos()
	top20marcas = getTOP20Marcas(pais)
	
	marcas_dict = OrderedDict()

	condicion = ~Q(pais = pais) & Q(pais__activo=True)
	
	if letra:
		condicion = condicion & Q(id_medicamento__nombre_medicamento__startswith=letra)
	elif otros:
		for l in string.uppercase:
			condicion = condicion & ~Q(id_medicamento__nombre_medicamento__startswith=l)

	marcas = MedicamentoPresentacion.objects.filter( condicion ).\
		select_related('id_medicamento','id_medicamento','pais').\
		order_by('id_medicamento__nombre_medicamento').\
		values('id_medicamento__nombre_medicamento', 'pais__pais_nombre', 'pais', \
			'pais__flag', 'pais__link', 'id_medicamento__id_vademecum').\
		distinct()  
			
	#Convierto QuerySet a OrderedDict para agrupar los datos de paises 
	#por marca y asi mantener el ordenamiento hecho previamente
	for elem in marcas:
		if elem['id_medicamento__nombre_medicamento'] in marcas_dict:
			marcas_dict[elem['id_medicamento__nombre_medicamento']].append({'pais':elem['pais'],'nombre':elem['pais__pais_nombre'],
				'link':elem['pais__link'], 'flag':elem['pais__flag'],'url':elem['id_medicamento__id_vademecum']
			})
		else:
			marcas_dict[elem['id_medicamento__nombre_medicamento']] = [{'pais':elem['pais'],'nombre':elem['pais__pais_nombre'],
				'link':elem['pais__link'], 'flag':elem['pais__flag'],'url':elem['id_medicamento__id_vademecum']
			}]
	
	#Convierto a tupla porque Paginator no acepta dict ni OrderedDict
	tupla = tuple((k,v) for k,v in marcas_dict.iteritems())
	
	paginator = Paginator(tupla, 20) 
	page = request.GET.get('page')
	
	pags, marcas_pais = paginacionGenerador(page, paginator)
	
	return render_to_response(
		'otros_paises_paginator.html', 
		{
			"pais":pais, 
			"letra":letra, 
			"otros":otros,
			"letters":letters_global,
			"top20marcas":top20marcas, 
			"activos": paises_activos, "nombres_paises": nombres_paises, 
			"metatag_base": metatag_base,
			"marcas": marcas_pais,
			"pags": pags,
			"idioma":idioma,
			"multilanguage" :multilanguage,
		}, 
		context_instance=RequestContext(request)
	)

@ensure_csrf_cookie
def marcas(request, nombre=None, letra=None, otros=None):
	lang_code, multilanguage, idioma = getLanguageCode(request)
	pais = getPaisVademecum()
	
	metatag_base = getMetatagBase(idioma, pais)
	
	paises_activos, nombres_paises  = getPaisesActivos()
	top20marcas = getTOP20Marcas(pais)
	return render_to_response(
		'marcas.html', 
		{
			"pais":pais, 
			"letra":letra, 
			"letters":string.uppercase, 
			"top20marcas":top20marcas, 
			"activos": paises_activos, "nombres_paises": nombres_paises, 
			"metatag_base": metatag_base, 
			"idioma":idioma,
			"multilanguage" :multilanguage,
		}, 
		context_instance=RequestContext(request)
	)
	
@ensure_csrf_cookie
def marcas_paginator(request, nombre=None, letra=None, otros=None):
	lang_code, multilanguage, idioma = getLanguageCode(request)
	pais = getPaisVademecum()
	
	metatag_base = getMetatagBase(idioma, pais)
	
	paises_activos, nombres_paises  = getPaisesActivos()
	top20marcas = getTOP20Marcas(pais)
	
	if letra:
		marcas_id = MedicamentoPresentacion.objects.\
			filter(pais = pais, id_medicamento__nombre_medicamento__startswith=letra).\
			values('id_medicamento').distinct()
	elif otros:
		condicion = Q()
		for l in string.uppercase:
			condicion = condicion & ~Q(id_medicamento__nombre_medicamento__startswith=l)
		marcas_id = MedicamentoPresentacion.objects.\
			filter(condicion & Q(pais=pais)).\
			values('id_medicamento').distinct()
	else:
		marcas_id = MedicamentoPresentacion.objects.\
			filter(pais = pais).\
			values('id_medicamento').distinct()
	
	marca = Medicamento.objects.filter(pk__in = marcas_id).order_by('nombre_medicamento')
	
	paginator = Paginator(marca, 20) 
	page = request.GET.get('page')
	
	pags, marcas = paginacionGenerador(page, paginator)
	
	return render_to_response(
		'marcas_paginator.html', 
		{
			"pais":pais, 
			"letra":letra, 
			"otros":otros, 
			"letters":letters_global, 
			"top20marcas":top20marcas, 
			"activos": paises_activos, "nombres_paises": nombres_paises, 
			"metatag_base": metatag_base, 
			"marcas": marcas, 
			"pags": pags, 
			"idioma":idioma, 
			"multilanguage" :multilanguage,
		}, 
		context_instance=RequestContext(request)
	)

def ajax_marcas(request):
	if request.is_ajax():
		pais = getPaisVademecum()
		marcas = []
		ranking = request.POST.get("ranking", None)
		if ranking:
			marcas_rank = RankingMarca.objects.all().order_by('-total')
			for marca in marcas_rank:
				marcas.append( marca.marca )
		else:
			letra = request.POST.get("letra", None)
			if letra:
				#marcas = Medicamento.objects.filter(nombre_medicamento__startswith=letra).order_by('nombre_medicamento')
				marcas_id = MedicamentoPresentacion.objects.\
					filter(pais = pais, id_medicamento__nombre_medicamento__startswith=letra).\
					values('id_medicamento').distinct()
			else:
				#marcas = Medicamento.objects.filter().order_by('nombre_medicamento')
				marcas_id = MedicamentoPresentacion.objects.\
					filter(pais = pais).\
					values('id_medicamento').distinct()
				
			marcas = Medicamento.objects.filter(pk__in = marcas_id).order_by('nombre_medicamento')

		return HttpResponse(serializers.serialize('json', marcas, ensure_ascii=False), mimetype="application/json")
	else:
		raise Http404

@ensure_csrf_cookie
def medicamentos(request, nombre=None, letra=None):
	lang_code, multilanguage, idioma = getLanguageCode(request)
	pais = getPaisVademecum()
	
	metatag_base = getMetatagBase(idioma, pais)
	
	paises_activos, nombres_paises  = getPaisesActivos()
	top20marcas = getTOP20Marcas(pais)
	return render_to_response(
		'medicamentos.html', 
		{
			"pais":pais, 
			"letra":letra, 
			"letters":string.uppercase, 
			"top20marcas":top20marcas, 
			"activos": paises_activos, "nombres_paises": nombres_paises, 
			"metatag_base": metatag_base, 
			"idioma":idioma,
			"multilanguage" :multilanguage,
		}, 
		context_instance=RequestContext(request)
	)
	
@ensure_csrf_cookie
def medicamentos_paginator(request, nombre=None, letra=None, otros=None):
	lang_code, multilanguage, idioma = getLanguageCode(request)
	pais = getPaisVademecum()
	
	metatag_base = getMetatagBase(idioma, pais)
	
	paises_activos, nombres_paises  = getPaisesActivos()
	top20marcas = getTOP20Marcas(pais)

	if letra:
		medicamento = MedicamentoPresentacion.objects.filter(nombre_presentacion__startswith=letra, pais=pais).order_by('nombre_presentacion')
	elif otros:
		condicion = Q()
		for l in string.uppercase:
			condicion = condicion & ~Q(nombre_presentacion__startswith=l)
		medicamento = MedicamentoPresentacion.objects.filter(condicion & Q(pais=pais)).order_by('nombre_presentacion')
	else:
		medicamento = MedicamentoPresentacion.objects.filter(pais=pais).order_by('nombre_presentacion')
	
	paginator = Paginator(medicamento, 20) 
	page = request.GET.get('page')
	
	pags, presentaciones = paginacionGenerador(page, paginator)
	
	return render_to_response(
		'medicamentos_paginator.html', 
		{
			"pais":pais, 
			"letra":letra, 
			"otros":otros,
			"letters":letters_global,
			"top20marcas":top20marcas, 
			"activos": paises_activos, "nombres_paises": nombres_paises, 
			"metatag_base": metatag_base,
			"presentaciones": presentaciones,
			"pags": pags, 
			"idioma":idioma,
			"multilanguage" :multilanguage,
		}, 
		context_instance=RequestContext(request)
	)

@ensure_csrf_cookie
def meds_sin_recipe(request, letra=None):
	lang_code, multilanguage, idioma = getLanguageCode(request)
	pais = getPaisVademecum()
	
	metatag_base = getMetatagBase(idioma, pais)
	
	paises_activos, nombres_paises  = getPaisesActivos()
	top20marcas = getTOP20Marcas(pais)
	return render_to_response(
		'meds_sin_recipe.html', 
		{
			"pais":pais, 
			"letra":letra, 
			"letters":string.uppercase, 
			"top20marcas":top20marcas, 
			"activos": paises_activos, "nombres_paises": nombres_paises, 
			"idioma":idioma,
			"multilanguage" :multilanguage,
		}, 
		context_instance=RequestContext(request)
	)


def ajax_medicamentos(request, nombre=None):
	if request.is_ajax():
		pais = getPaisVademecum()
		medicamento = []
		ranking = request.POST.get("ranking", None)
		sin_receta = request.POST.get("sin_receta", None)

		if ranking:
			meds_rank = RankingMedicamento.objects.all().order_by('-total')
			for med in meds_rank:
				medicamento.append( med.medicamento )
		elif sin_receta:
			letra = request.POST.get("letra", None)
			if letra:
				medicamento = MedicamentoPresentacion.objects.filter(requiere_recipe=0, nombre_presentacion__startswith=letra, pais=pais).order_by('nombre_presentacion')
			else:
				#if nombre:
					#pais=Pais.objects.get(pais_nombre="PANAMA")
					
					#medicamento = MedicamentoPresentacion.objects.filter(requiere_recipe=0, pais=pais).order_by('nombre_presentacion')[:220]
				#else:
					#pais=Pais.objects.get(pais_id=3)
				medicamento = MedicamentoPresentacion.objects.filter(requiere_recipe=0, pais=pais).order_by('nombre_presentacion')[:220]
		else:
			letra = request.POST.get("letra", None)
			if letra:
				medicamento = MedicamentoPresentacion.objects.filter(nombre_presentacion__startswith=letra, pais=pais).order_by('nombre_presentacion')
			else:
				# Aca deberia traer TODAS pero por eficiencia me traigo unas pocas mientras tanto
				# OJO solucionar!
				#if nombre:
					#pais=Pais.objects.get(pais_nombre="PANAMA")
					#medicamento = MedicamentoPresentacion.objects.filter(pais=pais).order_by('nombre_presentacion')[:900]
				#else:
					#pais=Pais.objects.get(pais_id=3)
				medicamento = MedicamentoPresentacion.objects.filter(pais=pais).order_by('nombre_presentacion')[:900]

		return HttpResponse(serializers.serialize('json', medicamento, ensure_ascii=False), mimetype="application/json")
	else:
		raise Http404


@ensure_csrf_cookie
def principios(request, nombre=None, letra=None):
	lang_code, multilanguage, idioma = getLanguageCode(request)
	pais = getPaisVademecum()
	
	metatag_base = getMetatagBase(idioma, pais)
	
	paises_activos, nombres_paises  = getPaisesActivos()
	top20marcas = getTOP20Marcas(pais)
	return render_to_response(
		'principios.html', 
		{
			"pais":pais, 
			"letra":letra, 
			"letters":string.uppercase,
			"top20marcas":top20marcas, 
			"activos": paises_activos, "nombres_paises": nombres_paises, 
			"metatag_base": metatag_base, 
			"idioma":idioma,
			"multilanguage" :multilanguage,
		}, 
		context_instance=RequestContext(request)
	)

@ensure_csrf_cookie
def principios_paginator(request, nombre=None, letra=None, otros=None):
	lang_code, multilanguage, idioma = getLanguageCode(request)
	pais = getPaisVademecum()
	
	metatag_base = getMetatagBase(idioma, pais)
	
	idioma_p = getIdiomaPrincipios()
	paises_activos, nombres_paises  = getPaisesActivos()
	top20marcas = getTOP20Marcas(pais)
	
	if letra: 
		principio = PrincipioGrupo.objects.filter(prigrup_nombre__startswith=letra, idioma=idioma_p).order_by('prigrup_nombre')
	elif otros:
		condicion = Q()
		for l in string.uppercase:
			condicion = condicion & ~Q(prigrup_nombre__startswith=l)
		principio = PrincipioGrupo.objects.filter(condicion & Q(idioma=idioma_p)).order_by('prigrup_nombre')
	else:
		principio = PrincipioGrupo.objects.filter(idioma=idioma_p).order_by('prigrup_nombre')
	
	paginator = Paginator(principio, 20) 
	page = request.GET.get('page',1)
	
	pags, principios = paginacionGenerador(page, paginator)
	
	return render_to_response(
		'principios_paginator.html', 
		{
			"pais":pais, 
			"letra":letra, 
			"otros":otros,
			"letters":letters_global,
			"top20marcas":top20marcas, 
			"activos": paises_activos, "nombres_paises": nombres_paises, 
			"metatag_base": metatag_base,
			"principios": principios,
			"pags": pags,
			"idioma":idioma,
			"multilanguage" :multilanguage,
		}, 
		context_instance=RequestContext(request)
	)

def ajax_principios(request, nombre=None):
	
	if request.is_ajax():
		idioma = getIdiomaPrincipios()
		principio_grupo = []
		ranking = request.POST.get("ranking", None)
		if ranking:
			principio_rank = RankingPrincipioActivo.objects.all().order_by('-total')
			for principio in principio_rank:
				principio_grupo.append( principio.principio )
		else:
			letra = request.POST.get("letra", None)
			if letra: 
				principio_grupo = PrincipioGrupo.objects.filter(prigrup_nombre__startswith=letra, idioma=idioma).order_by('prigrup_nombre')
			else:
				principio_grupo = PrincipioGrupo.objects.filter(idioma=idioma).order_by('prigrup_nombre')

		return HttpResponse(serializers.serialize('json', principio_grupo, ensure_ascii=False), mimetype="application/json")
	else:
		raise Http404

@ensure_csrf_cookie
def clases(request, nombre=None):
	lang_code, multilanguage, idioma = getLanguageCode(request)
	pais = getPaisVademecum()
	
	metatag_base = getMetatagBase(idioma, pais)
	
	paises_activos, nombres_paises  = getPaisesActivos()
	top20marcas = getTOP20Marcas(pais)
	return render_to_response(
		'clases.html', 
		{
			"pais": pais, 
			"top20marcas":top20marcas, 
			"activos": paises_activos, "nombres_paises": nombres_paises, 
			"metatag_base": metatag_base, 
			"idioma":idioma,
			"multilanguage" :multilanguage,
		}, 
		context_instance=RequestContext(request)
	)

def ajax_clases(request):
	
	if request.is_ajax():
		clases = []
		ranking = request.POST.get("ranking", None)
		if ranking:
			clases_rank = RankingClase.objects.all().order_by('-total')
			for clase in clases_rank:
				clases.append( clase.clase )
		else:
			clases = ClaseTerapeutica.objects.filter().order_by('nombre_clase')	

		return HttpResponse(serializers.serialize('json', clases, ensure_ascii=False), mimetype="application/json")
	else:
		raise Http404

def ajax_subclases(request, nombre=None):
	
	if request.is_ajax():
		subclases = []
		ranking = request.POST.get("ranking", None)
		if ranking:
			subclases_rank = RankingSubclase.objects.all().order_by('-total')[:100]
			for subclase in subclases_rank:
				if subclase.subclase:
					subclases.append( subclase.subclase )

		return HttpResponse(serializers.serialize('json', subclases, ensure_ascii=False), mimetype="application/json")
	else:
		raise Http404

@ensure_csrf_cookie
def enfermedades(request, nombre=None,  letra=None):
	lang_code, multilanguage, idioma = getLanguageCode(request)
	pais = getPaisVademecum()
	
	metatag_base = getMetatagBase(idioma, pais)
	
	paises_activos, nombres_paises  = getPaisesActivos()
	top20marcas = getTOP20Marcas(pais)
	return render_to_response(
		'enfermedades.html', 
		{
			"pais":pais, 
			"letra":letra, 
			"letters":string.uppercase, 
			"top20marcas":top20marcas, 
			"activos": paises_activos, "nombres_paises": nombres_paises, 
			"metatag_base": metatag_base, 
			"idioma":idioma,
			"multilanguage" :multilanguage,
		},
		context_instance=RequestContext(request)
	)

@ensure_csrf_cookie
def enfermedades_paginator(request, nombre=None,  letra=None, otros=None):
	lang_code, multilanguage, idioma = getLanguageCode(request)
	pais = getPaisVademecum()
	
	metatag_base = getMetatagBase(idioma, pais)
	
	paises_activos, nombres_paises  = getPaisesActivos()
	top20marcas = getTOP20Marcas(pais)
	if letra: 
		enfermedad = TipoDiagnostico.objects.filter(nombre_diagnostico__startswith=letra).order_by('nombre_diagnostico')
	elif otros:
		condicion = Q()
		for l in string.uppercase:
			condicion = condicion & ~Q(nombre_diagnostico__startswith=l)
		enfermedad = TipoDiagnostico.objects.filter(condicion).order_by('nombre_diagnostico')
	else:
		enfermedad = TipoDiagnostico.objects.all().order_by('nombre_diagnostico')
	
	paginator = Paginator(enfermedad, 20) 
	page = request.GET.get('page',1)
	
	pags, enfermedades = paginacionGenerador(page, paginator)
	
	return render_to_response(
		'enfermedades_paginator.html', 
		{
			"pais":pais, 
			"letra":letra, 
			"otros":otros,
			"letters":letters_global,
			"top20marcas":top20marcas, 
			"activos": paises_activos, "nombres_paises": nombres_paises, 
			"metatag_base": metatag_base,
			"enfermedades": enfermedades,
			"pags": pags, 
			"idioma":idioma,
			"multilanguage" :multilanguage,
		}, 
		context_instance=RequestContext(request)
	)

def ajax_enfermedades(request):

	if request.is_ajax():
		enfermedades = []
		ranking = request.POST.get("ranking", None)
		if ranking:
			enfs_rank = RankingEnfermedad.objects.all().order_by('-total')
			for enf in enfs_rank:
				enfermedades.append( enf.enfermedad )
		else:
			letra = request.POST.get("letra", None)
			if letra:
				enfermedades = TipoDiagnostico.objects.filter(nombre_diagnostico__startswith=letra).order_by('nombre_diagnostico')
			else:
				enfermedades = TipoDiagnostico.objects.filter().order_by('nombre_diagnostico')

		return HttpResponse(serializers.serialize('json', enfermedades, ensure_ascii=False), mimetype="application/json")
	else:
		raise Http404
	
def ajax_clinicas(request):

	if request.is_ajax():
		clinicas = []
		letra = request.POST.get("letra", None)
		if letra:
			clinicas = Clinica.objects.filter(nombre_clinica__startswith=letra).order_by('nombre_clinica')
		else:
			clinicas = Clinica.objects.filter().order_by('nombre_clinica')

		return HttpResponse(serializers.serialize('json', clinicas, ensure_ascii=False), mimetype="application/json")
	else:
		raise Http404

# RANKING
@ensure_csrf_cookie
def ranking_marcas(request, nombre=None):
	lang_code, multilanguage, idioma = getLanguageCode(request)
	pais = getPaisVademecum()
	
	metatag_base = getMetatagBase(idioma, pais)
	
	paises_activos, nombres_paises  = getPaisesActivos()
	top20marcas = RankingMarca.objects.all().order_by('-total')[:20]
	return render_to_response(
		'ranking_marcas.html', 
		{
			"pais":pais, 
			"top20marcas":top20marcas, 
			"activos": paises_activos, "nombres_paises": nombres_paises, 
			"metatag_base": metatag_base, 
			"idioma":idioma,
			"multilanguage" :multilanguage,
		}, 
		context_instance=RequestContext(request)
	)
	
@ensure_csrf_cookie
def ranking_medicamentos(request, nombre=None):
	lang_code, multilanguage, idioma = getLanguageCode(request)
	pais = getPaisVademecum()
	
	metatag_base = getMetatagBase(idioma, pais)
	
	paises_activos, nombres_paises  = getPaisesActivos()
	top20marcas = RankingMarca.objects.all().order_by('-total')[:20]
	return render_to_response(
		'ranking_medicamentos.html', 
		{
			"pais":pais, 
			"top20marcas":top20marcas, 
			"activos": paises_activos, "nombres_paises": nombres_paises, 
			"metatag_base": metatag_base, 
			"idioma":idioma,
			"multilanguage" :multilanguage,
		}, 
		context_instance=RequestContext(request)
	)

@ensure_csrf_cookie
def ranking_principios(request, nombre=None):
	lang_code, multilanguage, idioma = getLanguageCode(request)
	pais = getPaisVademecum()
	
	metatag_base = getMetatagBase(idioma, pais)
	
	paises_activos, nombres_paises  = getPaisesActivos()
	top20marcas = RankingMarca.objects.all().order_by('-total')[:20]
	return render_to_response(
		'ranking_principios.html', 
		{
			"pais":pais, 
			"top20marcas":top20marcas, 
			"activos": paises_activos, "nombres_paises": nombres_paises, 
			"metatag_base": metatag_base, 
			"idioma":idioma,
			"multilanguage" :multilanguage,
		}, 
		context_instance=RequestContext(request)
	)

@ensure_csrf_cookie
def ranking_clases(request, nombre=None):
	lang_code, multilanguage, idioma = getLanguageCode(request)
	pais = getPaisVademecum()
	
	metatag_base = getMetatagBase(idioma, pais)
	
	paises_activos, nombres_paises  = getPaisesActivos()
	top20marcas = RankingMarca.objects.all().order_by('-total')[:20]
	return render_to_response(
		'ranking_clases.html', 
		{
			"pais":pais, 
			"top20marcas":top20marcas, 
			"activos": paises_activos, "nombres_paises": nombres_paises, 
			"metatag_base": metatag_base, 
			"idioma":idioma,
			"multilanguage" :multilanguage,
		}, 
		context_instance=RequestContext(request)
	)

@ensure_csrf_cookie
def ranking_subclases(request, nombre=None):
	lang_code, multilanguage, idioma = getLanguageCode(request)
	pais = getPaisVademecum()
	
	metatag_base = getMetatagBase(idioma, pais)
	
	paises_activos, nombres_paises  = getPaisesActivos()
	top20marcas = RankingMarca.objects.all().order_by('-total')[:20]
	return render_to_response(
		'ranking_subclases.html', 
		{
			"pais":pais, 
			"top20marcas":top20marcas, 
			"activos": paises_activos, "nombres_paises": nombres_paises, 
			"metatag_base": metatag_base, 
			"idioma":idioma,
			"multilanguage" :multilanguage,
		}, 
		context_instance=RequestContext(request)
	)

@ensure_csrf_cookie
def ranking_enfermedades(request, nombre=None):
	lang_code, multilanguage, idioma = getLanguageCode(request)
	pais = getPaisVademecum()
	
	metatag_base = getMetatagBase(idioma, pais)
	
	paises_activos, nombres_paises  = getPaisesActivos()
	top20marcas = RankingMarca.objects.all().order_by('-total')[:20]
	return render_to_response(
		'ranking_enfermedades.html', 
		{
			"pais":pais, 
			"top20marcas":top20marcas, 
			"activos": paises_activos, "nombres_paises": nombres_paises, 
			"metatag_base": metatag_base, 
			"idioma":idioma,
			"multilanguage" :multilanguage,
		}, 
		context_instance=RequestContext(request)
	)

# VER / DETALLE
@ensure_csrf_cookie
def ver_marca_id(request,  id, nombre=None):
	marca = get_object_or_404(Medicamento, id_medicamento=id)
	datos = ver_marca(request, marca, nombre)
	return render_to_response('ver_marca.html', datos, context_instance=RequestContext(request))

@ensure_csrf_cookie
def ver_marca_vademecum(request, id_vademecum, nombre=None):
	marca = get_object_or_404(Medicamento, id_vademecum=id_vademecum.encode('utf-8'))
	datos = ver_marca(request, marca, nombre)
	return render_to_response('ver_marca.html', datos, context_instance=RequestContext(request))

def ver_marca(request, marca, nombre=None):
    
	pais = getPaisVademecum()
	paises_activos, nombres_paises  = getPaisesActivos()
	
	lang_code, multilanguage, idioma = getLanguageCode(request)
	
	metatag_base = getMetatagBase(idioma, pais)
	
	try:
		metatag = Seo.objects.get(pais = pais, pagina= 'Marcas',idioma = idioma)
	except:
		#Espaniol por defecto, si hay falla
		try:
			metatag = Seo.objects.get(pais = pais, pagina= 'Marcas',idioma__pk = 1)
		except:
			metatag = None
		
	if metatag:
		keywords = re.sub(r'#\+\*', marca.nombre_medicamento, metatag.keywords, flags=re.IGNORECASE)
	else:
		keywords = None
	
	try:
		marca_indicaciones = MarcaIndicaciones.objects.get(marca = marca, idioma = idioma)
	except:
		marca_indicaciones = None
	
	#pais_otros=Pais.objects.filter(pais_id__in=[1,2])
	marca_pais=MedicamentoPresentacion.objects.filter(id_medicamento = marca, pais__activo = True).\
		exclude(pais = pais).values('id_medicamento__nombre_medicamento', 'pais__pais_nombre', 'pais', 'pais__link').distinct()  
	#print marca_pais
	
	meds_filter = MedicamentoPresentacion.objects.filter(id_medicamento=marca, pais = pais)	
	
	#meds = MedicamentoPresentacion.objects.filter(id_medicamento=marca)
	principios = meds_filter.values('id_principio').distinct()
	
	#espaniol = meds_filter.filter(id_principio__idioma=1)
	#ingles = meds_filter.filter(id_principio__idioma=2)
	
	#print 'EN ESPAniol',espaniol.count(), 'EN INGLES',ingles.count()
	
	#print "----", principios

	#print marca.indicaciones, type(marca.indicaciones)
	
	# Listas que se pasan al template
	marcas, presentaciones = [], []

	for prin in principios:

		id_principio = prin['id_principio']
		meds_principio = MedicamentoPresentacion.objects.filter(
			~Q(id_medicamento=marca) & 
			Q(id_principio__id_principio=id_principio) & Q( pais = pais ) ).values('id_medicamento').distinct()
		for med in meds_principio:
			marca_asoc = Medicamento.objects.get(id_medicamento=med['id_medicamento'])
			if marca_asoc not in marcas:
				marcas.append(marca_asoc)
			if len(marcas) == 10:
				break
		if len(marcas) == 10:
			break	

	#top20marcas = RankingMarca.objects.all().order_by('-total')[:20]
	top20marcas = getTOP20Marcas(pais)

	principio = None
	if meds_filter:
		principio = meds_filter[0].id_principio.pri_grupo

	#datos = dict(marca = marca, presentaciones = meds, marcas = marcas, principio=principio, top20marcas = top20marcas, pais=nombre)
	datos = dict(
		marca = marca, 
		presentaciones = meds_filter, 
		marcas = marcas, 
		principio = principio, 
		top20marcas = top20marcas, 
		pais = pais, 
		marca_pais = marca_pais,
		activos = paises_activos, nombres_paises = nombres_paises,
		keywords = keywords, 
		metatag_base = metatag_base,
		indicaciones = marca_indicaciones, 
		idioma = idioma, 
		multilanguage = multilanguage,
	)

	return datos

@ensure_csrf_cookie
def ver_medicamento_id(request, id, nombre=None):
	medicamento = get_object_or_404(MedicamentoPresentacion, id_presentacion=id)
	datos = ver_medicamento(request, medicamento, nombre)
	return render_to_response('ver_medicamento.html', datos, context_instance=RequestContext(request))

@ensure_csrf_cookie
def ver_medicamento_vademecum(request, id_vademecum, nombre=None):
	medicamento = get_object_or_404(MedicamentoPresentacion, id_vademecum=id_vademecum.encode('utf-8'))
	datos = ver_medicamento(request, medicamento, nombre)
	return render_to_response('ver_medicamento.html', datos, context_instance=RequestContext(request))	


def ver_medicamento(request, medicamento, nombre):

	lang_code, multilanguage, idioma = getLanguageCode(request)
	pais = getPaisVademecum()
	paises_activos, nombres_paises  = getPaisesActivos()
	
	metatag_base = getMetatagBase(idioma, pais)
	
	try:
		metatag = Seo.objects.get(pais = pais, pagina= 'Medicamentos',idioma = idioma)
	except:
		#Espaniol por defecto, si hay falla
		try:
			metatag = Seo.objects.get(pais = pais, pagina= 'Medicamentos',idioma__pk = 1)
		except:
			metatag = None
		
	if metatag:
		keywords = re.sub(r'#\+\*', medicamento.nombre_presentacion, metatag.keywords, flags=re.IGNORECASE)
	else:
		keywords = None
	
	pagina = request.GET.get("page", 1)
	meds_rel = MedicamentoPresentacion.objects.\
		filter(id_principio=medicamento.id_principio, pais=pais).\
		exclude(id_presentacion=medicamento.id_presentacion)[:10]
		
	enfermedades = []

	# tiene el mismo mini-bug que la consulta hecha en principios activos.
	relpats = AuditRelpatologia.objects.values('arlp_idpatologia').\
		filter(arlp_idmedicamento__amed_presentacion=medicamento).\
		exclude(arlp_idpatologia=None).\
		annotate(cantidad=Count('arlp_idpatologia')).\
		order_by('-cantidad')[:10]

	for relpat in relpats:
		enfermedades.append( TipoDiagnostico.objects.get(id_diagnostico=relpat["arlp_idpatologia"]) )

	top20marcas = getTOP20Marcas(pais)

	datos = dict(
		medicamento = medicamento,
		meds_relacionados = meds_rel,
		enfermedades = enfermedades,
		pagina = pagina, 
		top20marcas = top20marcas,
		pais = pais,
		activos = paises_activos, nombres_paises = nombres_paises,
		keywords = keywords,
		metatag_base = metatag_base,
		idioma = idioma, 
		multilanguage = multilanguage,
	)

	return datos

@ensure_csrf_cookie
def ver_principio_id(request, id, nombre=None):
	principio_grupo = get_object_or_404(PrincipioGrupo, prigrup_id=id)
	datos = ver_principio(request, principio_grupo, nombre)
	return render_to_response('ver_principio.html', datos, context_instance=RequestContext(request))

@ensure_csrf_cookie
def ver_principio_vademecum(request, id_vademecum, nombre=None):
	principio_grupo = get_object_or_404(PrincipioGrupo, id_vademecum=id_vademecum.encode('utf-8'))
	datos = ver_principio(request, principio_grupo, nombre)
	return render_to_response('ver_principio.html', datos, context_instance=RequestContext(request))	


def ver_principio(request, principio_grupo, nombre):
	lang_code, multilanguage, idioma = getLanguageCode(request)
	pais = getPaisVademecum()
	paises_activos, nombres_paises  = getPaisesActivos()
	
	metatag_base = getMetatagBase(idioma, pais)
	
	print principio_grupo
	meds = MedicamentoPresentacion.objects.filter(id_principio__pri_grupo=principio_grupo, pais = pais)

	# Listas que se pasan al template
	marcas, enfermedades, principios_rel, subclases = [], [], [], []

	for med in meds:
		#print "el med",med.id_presentacion
		if med.id_medicamento not in marcas:
			marcas.append( med.id_medicamento )

		if len(marcas) == 3:
			break

	# Mejorar query!
	# el de php parace que daba un resultado mas cercano a la realidad
	relpats = AuditRelpatologia.objects.values('arlp_idpatologia').filter(arlp_idmedicamento__amed_presentacion__in=meds).exclude(arlp_idpatologia=None).annotate(cantidad=Count('arlp_idpatologia')).order_by('-cantidad')[:3]

	for relpat in relpats:
		enfermedades.append( TipoDiagnostico.objects.get(id_diagnostico=relpat["arlp_idpatologia"]) )


	principio_subclase = PrincipioSubclase.objects.filter(id_principio__pri_grupo=principio_grupo)

	subclases2 = []

	for ps in principio_subclase:
		subclases.append( ps.id_subclase3 )
		subclases2.append( ps.id_subclase3.id_subclase2 )

	principios = PrincipioSubclase.objects.filter(id_subclase3__id_subclase2__in=subclases2, prisub_prio=1).exclude(id_principio__pri_grupo=principio_grupo)[:3]

	for principio in principios:
		principios_rel.append(principio.id_principio.pri_grupo)	

	top20marcas = getTOP20Marcas(pais)
	ListaPrincipios = PrincipioActivo.objects.filter(pri_grupo=principio_grupo.prigrup_id)
	medicamentoPrincipio = MedicamentoPresentacion.objects.filter(id_principio__in=ListaPrincipios, pais = pais, tipo_medicamento='GENERICO').exclude(indicaciones=None)
	
	medicamento = None
	if medicamentoPrincipio:
		medicamento = medicamentoPrincipio[0]	

	datos = dict(
		principio = principio_grupo,
		marcas = marcas,
		subclases = subclases2,
		enfermedades = enfermedades,
		principios = principios_rel, 
		top20marcas = top20marcas, 
		medicamento = medicamento, 
		pais = pais,
		activos = paises_activos, nombres_paises = nombres_paises,
		metatag_base = metatag_base, 
		idioma = idioma, 
		multilanguage = multilanguage,
	)

	return datos

@ensure_csrf_cookie
def ver_enfermedad_id(request, id, nombre=None):
	enfermedad = get_object_or_404(TipoDiagnostico, id_diagnostico=id)
	datos = ver_enfermedad(request, enfermedad, nombre)
	return render_to_response('ver_enfermedad.html', datos, context_instance=RequestContext(request))

@ensure_csrf_cookie
def ver_enfermedad_vademecum(request, id_vademecum, nombre=None):
	enfermedad = get_object_or_404(TipoDiagnostico, id_vademecum=id_vademecum.encode('utf-8'))
	datos = ver_enfermedad(request, enfermedad, nombre)
	return render_to_response('ver_enfermedad.html', datos, context_instance=RequestContext(request))


def ver_enfermedad(request, enfermedad, nombre):
	lang_code, multilanguage, idioma = getLanguageCode(request)
	#if nombre=="panama":
		#pais_filter=Pais.objects.get(pais_nombre="PANAMA")
	#else:
		#pais_filter=Pais.objects.get(pais_id=3)
	pais = getPaisVademecum()
	paises_activos, nombres_paises  = getPaisesActivos()

	metatag_base = getMetatagBase(idioma, pais)

	pagina = request.GET.get("page", 1)

	sintomas = SintomaEnfermedad.objects.filter(id_enfermedad=enfermedad)	
	causas = CausaEnfermedad.objects.filter(enfermedad=enfermedad)
	
	# Enfermedades Relacionadas
	diagnosticos2 = TipoDiagnosticorelacion.objects.filter(id_diagnostico=enfermedad).values('id_diagnostico2')

	enfermedad_rel = TipoDiagnosticorelacion.objects.filter(~Q(id_diagnostico=enfermedad) & Q(id_diagnostico2__id__in=diagnosticos2))
	
	rel_patologia = AuditRelpatologia.objects.values('arlp_idpatologia').\
		filter( Q(arlp_idpatologia__in = [x.id_diagnostico for x in enfermedad_rel] ) ).\
		annotate(cantidad=Count('arlp_idpatologia')).\
		order_by('-cantidad')[:3]

	enfermedades_rel = TipoDiagnostico.objects.filter(id_diagnostico__in = [e["arlp_idpatologia"] for e in rel_patologia])

	# Marcas Relacionadas
	marcas_id = AuditRelpatologia.objects.values('arlp_idmedicamento__amed_presentacion__id_medicamento').\
		filter( arlp_idpatologia = enfermedad ).\
		annotate(cantidad=Count('arlp_idmedicamento__amed_presentacion__id_medicamento')).\
		order_by('-cantidad')
	marcas_rel = Medicamento.objects.filter(id_medicamento__in = [ marca["arlp_idmedicamento__amed_presentacion__id_medicamento"] for marca in marcas_id[:3] ])
	
	# Principios Relacionados
	principios_id = AuditRelpatologia.objects.values('arlp_idmedicamento__amed_presentacion__id_principio').\
		filter( arlp_idpatologia = enfermedad ).\
		annotate(cantidad=Count('arlp_idmedicamento__amed_presentacion__id_medicamento')).\
		order_by('-cantidad')
	principios_rel = PrincipioActivo.objects.\
		filter(id_principio__in = [ principio["arlp_idmedicamento__amed_presentacion__id_principio"] for principio in principios_id[:3] ])

	top20marcas = getTOP20Marcas(pais)
	
	# Presentaciones Relacionadas
	audmeds_id = AuditRelpatologia.objects.values('arlp_idmedicamento').\
		filter( arlp_idpatologia = enfermedad ).\
		annotate(cantidad=Count('arlp_idmedicamento')).\
		order_by('-cantidad')
	
	marcas_presentacion = AuditMedicamento.objects.values('amed_presentacion').\
		filter(amed_id__in = [e["arlp_idmedicamento"] for e in audmeds_id]).\
		annotate(cantidad=Count('amed_presentacion')).\
		order_by('-cantidad')

	presentacion_rel = MedicamentoPresentacion.objects.\
		filter(pais = pais, id_presentacion__in = [ e["amed_presentacion"] for e in marcas_presentacion[:3] ])

	datos = dict( 
		enfermedad = enfermedad, 
		sintomas = sintomas, 
		causas = causas, 
		enfermedades_rel = enfermedades_rel, 
		marcas_rel =  marcas_rel, 
		principios_rel = principios_rel, 
		presentacion_rel = presentacion_rel, 
		top20marcas = top20marcas, 
		pagina = pagina, 
		pais = pais, 
		activos = paises_activos, nombres_paises = nombres_paises, 
		metatag_base = metatag_base, 
		idioma = idioma, 
		multilanguage = multilanguage,
	)

	return datos

def ajax_laboratorios(request):
	if request.is_ajax():
		pais = getPaisVademecum()
		id_lab = request.POST.get("id_lab", None)
		meds = MedicamentoPresentacion.objects.filter(id_laboratorio=id_lab, pais=pais).order_by('nombre_presentacion')

		return HttpResponse(serializers.serialize('json', meds, ensure_ascii=False), mimetype="application/json")
	else:
		raise Http404

@ensure_csrf_cookie
def ver_laboratorio(request, id_vademecum, nombre=None):
	lang_code, multilanguage, idioma = getLanguageCode(request)
	pais = getPaisVademecum()

	metatag_base = getMetatagBase(idioma, pais)

	paises_activos, nombres_paises  = getPaisesActivos()

	lab = get_object_or_404(Laboratorio, id_vademecum=id_vademecum)
	top20marcas = getTOP20Marcas(pais)
	return render_to_response(
		'ver_laboratorio.html',
		{
				"pais":pais,
				"lab":lab,
				"top20marcas":top20marcas,
				"activos": paises_activos, "nombres_paises": nombres_paises,
				"metatag_base": metatag_base,
				"idioma":idioma,
				"multilanguage" :multilanguage,
		},
		context_instance=RequestContext(request)
	)

@ensure_csrf_cookie
def ver_clase(request, id_vademecum, nombre=None):
	lang_code, multilanguage, idioma = getLanguageCode(request)
	pais = getPaisVademecum()
	
	metatag_base = getMetatagBase(idioma, pais)
	
	paises_activos, nombres_paises  = getPaisesActivos()

	clase = get_object_or_404(ClaseTerapeutica, id_vademecum=id_vademecum.encode('utf-8'))

	subclases = SubclaseNivel3.objects.filter(id_subclase3__startswith=clase.id_clase)

	lista_sc2 = [s.id_subclase2.sc2_id for s in subclases]
	
	subclases2 = SubclaseNivel2.objects.filter(sc2_id__in=lista_sc2)

	principio_subclase = PrincipioSubclase.objects.filter(id_subclase3__in=subclases)

	principios_activos, principios = [], []
	for ps in principio_subclase:
		principios.append( ps.id_principio.pri_grupo )
		principios_activos.append( ps.id_principio )		
		
	meds = MedicamentoPresentacion.objects.filter(id_principio__in=principios_activos)
	marcas = []
	for med in meds:
		if med.id_medicamento not in marcas:
			marcas.append( med.id_medicamento )

		if len(marcas) == 3:
			break
	
	top20marcas = getTOP20Marcas(pais)
	datos = dict(
		clase = clase, 
		subclases = subclases2[:3], 
		marcas = marcas, 
		principios = principios[:3], 
		top20marcas = top20marcas, 
		pais = pais,
		activos = paises_activos, nombres_paises = nombres_paises,
		metatag_base = metatag_base, 
		idioma = idioma, 
		multilanguage = multilanguage,
	)

	return render_to_response('ver_clase.html', datos, context_instance=RequestContext(request))

def ver_subclase_id(request, id, nombre=None):

	subclase = get_object_or_404(SubclaseNivel2, sc2_id=id)
	datos = ver_subclase(request, subclase, nombre)
	return render_to_response('ver_subclase.html', datos, context_instance=RequestContext(request))

def ver_subclase_vademecum(request, id_vademecum, nombre=None):

	subclases = SubclaseNivel2.objects.filter(id_vademecum=id_vademecum.encode('utf-8'))
	if subclases:
		subclase = subclases[0]
	else:
		raise Http404
	datos = ver_subclase(request, subclase, nombre)
	return render_to_response('ver_subclase.html', datos, context_instance=RequestContext(request))

def ver_subclase(request, subclase, nombre):
	lang_code, multilanguage, idioma = getLanguageCode(request)
	pais = getPaisVademecum()
	
	metatag_base = getMetatagBase(idioma, pais)
	
	paises_activos, nombres_paises  = getPaisesActivos()
	
	subclases_rel = SubclaseNivel2.objects.filter(id_subclase2=subclase.id_subclase2).exclude(sc2_id=subclase.sc2_id)[:3]
	subclase3= SubclaseNivel3.objects.filter(id_subclase2=subclase.sc2_id) 
	principios_sub = PrincipioSubclase.objects.filter(id_subclase3__in=subclase3) 


	principios, principios_a = [], []
	for prin in principios_sub:
		if prin.id_principio.pri_grupo not in principios:
			principios.append( prin.id_principio.pri_grupo )

		if prin.id_principio not in principios_a:
			principios_a.append( prin.id_principio )


	meds = MedicamentoPresentacion.objects.filter(id_principio__in=principios_a, pais = pais)

	marcas = []
	for med in meds:
		if med.id_medicamento not in marcas:
			marcas.append( med.id_medicamento )

		if len(marcas) == 3:
			break

	top20marcas = getTOP20Marcas(pais)
	datos = dict(
		subclase = subclase, 
		subclases_rel = subclases_rel, 
		principios = principios[:3], marcas = marcas, 
		top20marcas = top20marcas, 
		pais = pais,
		activos = paises_activos, nombres_paises = nombres_paises,
		metatag_base = metatag_base, 
		idioma = idioma, 
		multilanguage = multilanguage,
	)

	return datos

def error500(request):
	if request.is_ajax():
		return HttpResponseServerError()
	else:
		return render_to_response('500.html', context_instance=RequestContext(request))
