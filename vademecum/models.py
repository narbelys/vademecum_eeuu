# -*- coding: utf-8 -*-
from django.db import models

class Idioma(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=60)
	iso_alpha = models.CharField(max_length=10)
	class Meta:
		db_table = u'idioma'
		verbose_name_plural = "idiomas"
	def __unicode__(self):
		return self.nombre
        
class Pais(models.Model):
    pais_id = models.IntegerField(primary_key=True)
    pais_nombre = models.CharField(max_length=100)
    flag = models.CharField(max_length=1500)
    link = models.CharField(max_length=1500, null=True)
    iso_alpha = models.CharField(max_length = 3, null=True, blank=True, default='VE')
    activo = models.BooleanField(default=True)
    class Meta:
        db_table = u'pais'
        verbose_name_plural = "paises"
    def __unicode__(self):
        return self.pais_nombre

class Seo(models.Model):
	id = models.AutoField(primary_key=True)
	pais = models.ForeignKey(Pais, db_column='pais',default=1)
	idioma = models.ForeignKey(Idioma, db_column='idioma', default=1)
	pagina = models.CharField(max_length = 100)
	keywords = models.TextField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	title = models.TextField(blank=True, null=True)
	class Meta:
		db_table = u'ceo'
		unique_together = ('pais','pagina',)

class TipoDiagnostico(models.Model):
    id_diagnostico = models.IntegerField(primary_key=True)
    id_vademecum = models.CharField(max_length=300)
    nombre_diagnostico = models.CharField(max_length=300, blank=True)
    descripcion = models.CharField(max_length=1500, blank=True)
    img_diagnostico = models.CharField(max_length=45)
    keywords= models.CharField(max_length=1500)
    class Meta:
        db_table = u'tipo_diagnostico'

class Causa(models.Model):
    id_causa = models.IntegerField(primary_key=True)
    nombre_causa = models.CharField(max_length=150)
    class Meta:
        db_table = u'causa'

class CausaEnfermedad(models.Model):
    id_causa_enf = models.IntegerField(primary_key=True)
    enfermedad = models.ForeignKey(TipoDiagnostico, db_column='enfermedad')
    causa = models.ForeignKey(Causa, db_column='causa')
    class Meta:
        db_table = u'causa_enfermedad'

class Sintoma(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre_sintoma = models.CharField(max_length=150)
    enfermedad_relacionada = models.ForeignKey(TipoDiagnostico, null=True, db_column='enfermedad_relacionada', blank=True)
    class Meta:
        db_table = u'sintoma'

class SintomaEnfermedad(models.Model):
    id = models.IntegerField(primary_key=True)
    id_sintoma = models.ForeignKey(Sintoma, db_column='id_sintoma')
    id_enfermedad = models.ForeignKey(TipoDiagnostico, db_column='id_enfermedad')
    class Meta:
        db_table = u'sintoma_enfermedad'

class TipoDiagnostico1(models.Model):
    id_diagnostico1 = models.CharField(max_length=9, primary_key=True)
    nombre_tipo1 = models.CharField(max_length=600)
    class Meta:
        db_table = u'tipo_diagnostico1'

class TipoDiagnostico2(models.Model):
    id = models.IntegerField(primary_key=True)
    id_diagnostico2 = models.CharField(max_length=12)
    nombre_tipo2 = models.CharField(max_length=600)
    id_diagnostico1 = models.ForeignKey(TipoDiagnostico1, db_column='id_diagnostico1')
    class Meta:
        db_table = u'tipo_diagnostico2'

class TipoDiagnosticorelacion(models.Model):
    id_relacion = models.IntegerField(primary_key=True)
    id_diagnostico = models.ForeignKey(TipoDiagnostico, db_column='id_diagnostico')
    id_diagnostico2 = models.ForeignKey(TipoDiagnostico2, db_column='id_diagnostico2')
    class Meta:
        db_table = u'tipo_diagnosticorelacion'

class ClaseTerapeutica(models.Model):
    id_clase = models.CharField(max_length=15, primary_key=True)
    id_vademecum = models.CharField(max_length=300)
    nombre_clase = models.CharField(max_length=300)
    class Meta:
        db_table = u'clase_terapeutica'

class SubclaseTerapeutica(models.Model):
    sc_id = models.IntegerField(primary_key=True)
    id_subclase = models.CharField(max_length=15)
    nombre_subclase = models.CharField(max_length=300, blank=True)
    id_clase = models.ForeignKey(ClaseTerapeutica, null=True, db_column='id_clase', blank=True)
    class Meta:
        db_table = u'subclase_terapeutica'

class SubclaseNivel2(models.Model):
    sc2_id = models.IntegerField(primary_key=True)
    id_vademecum = models.CharField(max_length=200)
    titulo_vademecum = models.CharField(max_length=300)
    id_subclase2 = models.CharField(max_length=15)
    nombre_subclase2 = models.CharField(max_length=300)
    id_subclase = models.ForeignKey(SubclaseTerapeutica, db_column='id_subclase')
    class Meta:
        db_table = u'subclase_nivel2'

class SubclaseNivel3(models.Model):
    sc3_id = models.AutoField(primary_key=True)
    id_subclase3 = models.CharField(max_length=15)
    nombre_subclase3 = models.CharField(max_length=300)
    id_subclase2 = models.ForeignKey(SubclaseNivel2, db_column='id_subclase2')
    class Meta:
        db_table = u'subclase_nivel3'

class SubclaseDiagnostico(models.Model):
    id_subdia = models.IntegerField(primary_key=True)
    id_subclase = models.ForeignKey(SubclaseNivel2, db_column='id_subclase')
    id_diagnostico2 = models.ForeignKey(TipoDiagnostico2, db_column='id_diagnostico2')
    prioridad = models.IntegerField()
    class Meta:
        db_table = u'subclase_diagnostico'

class PrincipioGrupo(models.Model):
    prigrup_id = models.AutoField(primary_key=True)
    id_vademecum = models.CharField(max_length=300, null=True, blank=True)
    prigrup_nombre = models.CharField(max_length=240)
    idioma = models.IntegerField(default=1)
    class Meta:
        db_table = u'principio_grupo'

class PrincipioActivo(models.Model):
    id_principio = models.AutoField(primary_key=True)
    nombre_principio = models.CharField(max_length=300, blank=True)
    pri_grupo = models.ForeignKey(PrincipioGrupo, db_column='pri_grupo')
    idioma = models.IntegerField(default=1)
    class Meta:
        db_table = u'principio_activo'

class PrincipioSubclase(models.Model):
    id_prisub = models.IntegerField(primary_key=True)
    id_principio = models.ForeignKey(PrincipioActivo, db_column='id_principio')
    id_subclase3 = models.ForeignKey(SubclaseNivel3, db_column='id_subclase3')
    prisub_prio = models.IntegerField()
    class Meta:
        db_table = u'principio_subclase'

class Laboratorio(models.Model):
    id_laboratorio = models.CharField(max_length=15, primary_key=True)
    id_vademecum = models.CharField(max_length=300)
    nombre_laboratorio = models.CharField(max_length=300)
    abrev_laboratorio = models.CharField(max_length=60)
    logo = models.CharField(max_length=45)
    website = models.CharField(max_length=300, null=True, blank=True, default=None)
    class Meta:
        db_table = u'laboratorio'

class MarcaGrupo(models.Model):
    magr_id = models.IntegerField(primary_key=True)
    magr_nombre = models.CharField(max_length=240)
    class Meta:
        db_table = u'marca_grupo'

class Medicamento(models.Model):
    id_medicamento = models.AutoField(primary_key=True)
    id_vademecum = models.CharField(max_length=300)
    nombre_medicamento = models.CharField(max_length=300)
    id_grupo = models.ForeignKey(MarcaGrupo, db_column='id_grupo')
    indicaciones = models.CharField(max_length=1500, blank=True)
    keywords = models.CharField(max_length=1500, blank=True)
    reacciones_adversas = models.CharField(max_length=1500, blank=True)
    contraindicaciones = models.CharField(max_length=1500, blank=True)
    posologia = models.CharField(max_length=1500, blank=True)
    class Meta:
        db_table = u'medicamento'

class MarcaIndicaciones(models.Model):
	id = models.AutoField(primary_key=True)
	idioma = models.ForeignKey(Idioma, db_column='idioma')
	marca = models.ForeignKey(Medicamento, db_column='marca')
	indicaciones = models.TextField(null=True, blank=True)
	keywords = models.TextField(null=True, blank=True)
	reacciones_adversas = models.TextField(null=True, blank=True)
	contraindicaciones = models.TextField(null=True, blank=True)
	posologia = models.TextField(null=True, blank=True)
	class Meta:
		db_table = u'marca_indicaciones'
		unique_together = ('idioma','marca',)

class MedicamentoGrupo(models.Model):
    mgrupo_id = models.IntegerField(primary_key=True)
    mgrupo_nombre = models.CharField(max_length=150)
    class Meta:
        db_table = u'medicamento_grupo'

class MedicamentoAdm(models.Model):
    mdad_id = models.IntegerField(primary_key=True)
    mdad_nombre = models.CharField(max_length=150)
    mdad_grupo = models.ForeignKey(MedicamentoGrupo, db_column='mdad_grupo')
    mdad_dosis = models.IntegerField()
    class Meta:
        db_table = u'medicamento_adm'

class MedicamentoPresentacion(models.Model):
    id_presentacion = models.AutoField(primary_key=True)
    id_vademecum = models.CharField(max_length=300)
    nombre_presentacion = models.CharField(max_length=300)
    tipo_medicamento = models.CharField(max_length=300)
    rx_otc = models.CharField(max_length=300)
    id_medicamento = models.ForeignKey(Medicamento, db_column='id_medicamento')
    id_principio = models.ForeignKey(PrincipioActivo, db_column='id_principio')
    id_laboratorio = models.ForeignKey(Laboratorio, db_column='id_laboratorio')
    forma_adm = models.ForeignKey(MedicamentoAdm, db_column='forma_adm')
    indicaciones = models.CharField(max_length=1500, blank=True)
    keywords = models.CharField(max_length=1500)
    requiere_recipe = models.NullBooleanField()
    img_presentacion = models.ImageField(max_length=1500, upload_to=".", blank = True)
    pais = models.ForeignKey(Pais, db_column='pais',null=True, blank=True,default=1)
    class Meta:
        db_table = u'medicamento_presentacion'

class RankingMarca(models.Model):
    id = models.AutoField(primary_key=True)
    marca = models.ForeignKey(Medicamento, db_column='marca')
    total = models.IntegerField()
    class Meta:
        db_table = u'ranking_marca'

class RankingMedicamento(models.Model):
    id = models.AutoField(primary_key=True)
    medicamento = models.ForeignKey(MedicamentoPresentacion, db_column='medicamento')
    total = models.IntegerField()
    class Meta:
        db_table = u'ranking_medicamento'

class RankingPrincipioActivo(models.Model):
    id = models.AutoField(primary_key=True)
    principio = models.ForeignKey(PrincipioGrupo, db_column='principio')
    total = models.IntegerField()
    class Meta:
        db_table = u'ranking_principio'

class RankingEnfermedad(models.Model):
    id = models.AutoField(primary_key=True)
    enfermedad = models.ForeignKey(TipoDiagnostico, db_column='enfermedad')
    total = models.IntegerField()
    class Meta:
        db_table = u'ranking_enfermedad'

class RankingClase(models.Model):
    id = models.AutoField(primary_key=True)
    clase = models.ForeignKey(ClaseTerapeutica, db_column='clase')
    total = models.IntegerField()
    class Meta:
        db_table = u'ranking_clase'

class RankingSubclase(models.Model):
    id = models.AutoField(primary_key=True)
    subclase = models.ForeignKey(SubclaseNivel2, db_column='subclase')
    total = models.IntegerField()
    class Meta:
        db_table = u'ranking_subclase'

# Modelos del Audit

class AuditCaso(models.Model):
    ac_id = models.AutoField(primary_key=True)
    ac_numero = models.IntegerField()
    ac_fecha = models.DateField(auto_now_add=True)
    ac_aseguradora = models.IntegerField()
    ac_user = models.IntegerField()    
    ac_edad = models.IntegerField(null=True, blank=True)
    ac_tipoedad = models.CharField(max_length=3, blank=True)
    ac_sexo = models.CharField(max_length=3, blank=True)
    ac_tipocaso = models.IntegerField(null=True, blank=True)
    total_caso = models.FloatField(null=True, blank=True)
    total_ahorro = models.FloatField(null=True, blank=True)
    ac_desvahorro = models.IntegerField(null=True, db_column='ac_desvAhorro', blank=True)
    ac_desvfarma = models.IntegerField(null=True, db_column='ac_desvFarma', blank=True)
    ac_status = models.IntegerField()
    ac_observaciones = models.CharField(max_length=1500, blank=True)
    ac_tipoci = models.CharField(max_length=3, blank=True)
    ac_paciente = models.IntegerField()
    ac_nombre = models.CharField(max_length=150, blank=True)
    ac_apellido = models.CharField(max_length=150, blank=True)
    ac_colectivo = models.IntegerField()
    ac_fechacierre = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'audit_caso'
    def __unicode__(self):
        return self.ac_observaciones

class AuditInforme(models.Model):
    ai_id = models.AutoField(primary_key=True)
    ai_fecha = models.DateField(null=True, blank=True)
    ai_vence = models.DateField(null=True, blank=True)
    ai_medico = models.IntegerField(null=True, blank=True)
    ai_clinica = models.IntegerField(null=True, blank=True)
    ai_caso = models.ForeignKey(AuditCaso, db_column='ai_caso')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    ai_status = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'audit_informe'

class AuditMedicamento(models.Model):
    amed_id = models.AutoField(primary_key=True)
    amed_presentacion = models.ForeignKey(MedicamentoPresentacion, db_column='amed_presentacion')
    amed_informe = models.ForeignKey(AuditInforme, db_column='amed_informe')
    amed_cantidad = models.IntegerField()
    class Meta:
        db_table = u'audit_medicamento'

class AuditRelpatologia(models.Model):
    arlp_id = models.IntegerField(primary_key=True)
    arlp_idmedicamento = models.ForeignKey(AuditMedicamento, db_column='arlp_idmedicamento')
    arlp_idpatologia = models.ForeignKey(TipoDiagnostico, db_column='arlp_idpatologia',null=True, blank=True)
    arlp_caso = models.ForeignKey(AuditCaso, db_column='arlp_caso')
    informe = models.ForeignKey(AuditInforme, db_column='informe')
    class Meta:
        db_table = u'audit_relpatologia'
        

class Clinica(models.Model):
    id_clinica = models.IntegerField(primary_key=True)
    nombre_clinica = models.CharField(max_length=300)
    direccion_clinica = models.CharField(max_length=750, blank=True)
    telefono_clinica = models.CharField(max_length=300, blank=True)
    pagina = models.CharField(max_length=750, blank=True)
    url_vademecum = models.CharField(max_length=500, null=True)
    class Meta:
        db_table = u'clinica'
