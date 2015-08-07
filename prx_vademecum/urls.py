# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

# mostrar archivos estáticos en el error 500
handler500 = 'vademecum.views.error500'

urlpatterns = patterns('',
	url(r'^$', 'vademecum.views.index'),
	
	(r'^i18n/', include('django.conf.urls.i18n')),
	
	url(r'^Otros_paises/$','vademecum.views.marcas_otros_paises'),
	url(r'^Otros_paises/(?P<letra>[A-Z])?$','vademecum.views.marcas_otros_paises'),
	url(r'^Otros_paises/(?P<otros>others)?$', 'vademecum.views.marcas_otros_paises'),
	#url(r'^Otros_paises/$', 'vademecum.views.otros_paises'),
	#url(r'^Otros_paises/(?P<letra>[A-Z])?$', 'vademecum.views.otros_paises'),
	url(r'^Otros_paises/getMarcas$', 'vademecum.views.ajax_marcas_paises'),
                       
	url(r'^Marcas/(?P<letra>[A-Z])?$', 'vademecum.views.marcas_paginator'),
	url(r'^Marcas/(?P<otros>others)?$', 'vademecum.views.marcas_paginator'),
	#url(r'^Marcas/$', 'vademecum.views.marcas'),
	#url(r'^Marcas/(?P<letra>[A-Z])?$', 'vademecum.views.marcas'),
	url(r'^Marcas/getMarcas$', 'vademecum.views.ajax_marcas'),
    url(r'^Marcas/Ranking$', 'vademecum.views.ranking_marcas'),
	url(r'^Marcas/(?P<id>\d+)$', 'vademecum.views.ver_marca_id'),
	url(r'^Marcas/(?P<id_vademecum>[\w.()ñÑ\+\-,]+)$', 'vademecum.views.ver_marca_vademecum'),

	url(r'^Medicamentos/(?P<letra>[A-Z])?$', 'vademecum.views.medicamentos_paginator'),
	url(r'^Medicamentos/(?P<otros>others)?$', 'vademecum.views.medicamentos_paginator'),
	#url(r'^Medicamentos/(?P<letra>([A-Z])?$', 'vademecum.views.medicamentos'),
	url(r'^Medicamentos/getMeds$', 'vademecum.views.ajax_medicamentos'),
	url(r'^Medicamentos/Ranking$', 'vademecum.views.ranking_medicamentos'),
	url(r'^Medicamentos/(?P<id>\d+)$', 'vademecum.views.ver_medicamento_id'),
	url(r'^Medicamentos/(?P<id_vademecum>[\w()ñÑ]+)$', 'vademecum.views.ver_medicamento_vademecum'),

	url(r'^MedicamentosSinRecipe/(?P<letra>[A-Z])?$', 'vademecum.views.meds_sin_recipe'),

	url(r'^PrincipiosActivos/(?P<letra>[A-Z])?$', 'vademecum.views.principios_paginator'),
	url(r'^PrincipiosActivos/(?P<otros>others)?$', 'vademecum.views.principios_paginator'),
	#url(r'^PrincipiosActivos/(?P<letra>[A-Z])?$', 'vademecum.views.principios'),
	url(r'^PrincipiosActivos/getPrincipios$', 'vademecum.views.ajax_principios'),
	url(r'^PrincipiosActivos/Ranking$', 'vademecum.views.ranking_principios'),
	url(r'^PrincipiosActivos/(?P<id>\d+)$', 'vademecum.views.ver_principio_id'),
	url(r'^PrincipiosActivos/(?P<id_vademecum>[\w()ñÑ]+)$', 'vademecum.views.ver_principio_vademecum'),	
    
	url(r'^ClasesTerapeuticas/$', 'vademecum.views.clases'),
	url(r'^ClasesTerapeuticas/getClases$', 'vademecum.views.ajax_clases'),
	url(r'^ClasesTerapeuticas/Ranking$', 'vademecum.views.ranking_clases'),
	url(r'^ClasesTerapeuticas/(?P<id_vademecum>[\w()ñÑ]+)$', 'vademecum.views.ver_clase'),	


	url(r'^SubclasesTerapeuticas/getSubclases$', 'vademecum.views.ajax_subclases'),
	url(r'^SubclasesTerapeuticas/Ranking$', 'vademecum.views.ranking_subclases'),
	url(r'^SubclasesTerapeuticas/(?P<id>\d+)$', 'vademecum.views.ver_subclase_id'),
	url(r'^SubclasesTerapeuticas/(?P<id_vademecum>[\w()ñÑ]+)$', 'vademecum.views.ver_subclase_vademecum'),

	url(r'^Enfermedades/(?P<letra>[A-Z])?$', 'vademecum.views.enfermedades_paginator'),
	url(r'^Enfermedades/(?P<otros>others)?$', 'vademecum.views.enfermedades_paginator'),
	#url(r'^Enfermedades/(?P<letra>[A-Z])?$', 'vademecum.views.enfermedades'),
	url(r'^Enfermedades/getEnfermedades$', 'vademecum.views.ajax_enfermedades'),
	url(r'^Clinicas/getClinicas$', 'vademecum.views.ajax_clinicas'),
	url(r'^Enfermedades/Ranking$', 'vademecum.views.ranking_enfermedades'),
	url(r'^Enfermedades/(?P<id>\d+)$', 'vademecum.views.ver_enfermedad_id'),
	url(r'^Enfermedades/(?P<id_vademecum>[\w.()ñÑ\+\-,]+)$', 'vademecum.views.ver_enfermedad_vademecum'),
                       

	url(r'^Laboratorios/getMeds$', 'vademecum.views.ajax_laboratorios'),
	url(r'^Laboratorios/(?P<id_vademecum>[\w()ñÑ]+)$', 'vademecum.views.ver_laboratorio'),

	url(r'^Buscar/$', 'vademecum.views.buscar'),
	url(r'^Buscar/buscar$', 'vademecum.views.ajax_buscar'),

	url(r'^Blogs/$', 'vademecum.views.blogs'),
	url(r'^Contacto/$', 'vademecum.views.contacto'),
	url(r'^Clinicas/$', 'vademecum.views.clinicas'),
	url(r'^Clinicas/(?P<id>[\w()ñÑ]+)$', 'vademecum.views.clinicas'),

)


from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()