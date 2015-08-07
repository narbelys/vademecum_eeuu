-- MySQL dump 10.13  Distrib 5.5.38, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: vademecum
-- ------------------------------------------------------
-- Server version	5.5.38-0ubuntu0.12.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `audit_caso`
--

DROP TABLE IF EXISTS `audit_caso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `audit_caso` (
  `ac_id` int(11) NOT NULL AUTO_INCREMENT,
  `ac_numero` int(11) NOT NULL,
  `ac_fecha` date NOT NULL,
  `ac_aseguradora` int(11) NOT NULL,
  `ac_user` int(11) NOT NULL,
  `ac_edad` int(11) DEFAULT NULL,
  `ac_tipoedad` varchar(3) COLLATE utf8_spanish_ci NOT NULL,
  `ac_sexo` varchar(3) COLLATE utf8_spanish_ci NOT NULL,
  `ac_tipocaso` int(11) DEFAULT NULL,
  `total_caso` double DEFAULT NULL,
  `total_ahorro` double DEFAULT NULL,
  `ac_desvAhorro` int(11) DEFAULT NULL,
  `ac_desvFarma` int(11) DEFAULT NULL,
  `ac_status` int(11) NOT NULL,
  `ac_observaciones` varchar(1500) COLLATE utf8_spanish_ci NOT NULL,
  `ac_tipoci` varchar(3) COLLATE utf8_spanish_ci NOT NULL,
  `ac_paciente` int(11) NOT NULL,
  `ac_nombre` varchar(150) COLLATE utf8_spanish_ci NOT NULL,
  `ac_apellido` varchar(150) COLLATE utf8_spanish_ci NOT NULL,
  `ac_colectivo` int(11) NOT NULL,
  `ac_fechacierre` datetime DEFAULT NULL,
  PRIMARY KEY (`ac_id`)
) ENGINE=MyISAM AUTO_INCREMENT=1694 DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `audit_informe`
--

DROP TABLE IF EXISTS `audit_informe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `audit_informe` (
  `ai_id` int(11) NOT NULL AUTO_INCREMENT,
  `ai_fecha` date DEFAULT NULL,
  `ai_vence` date DEFAULT NULL,
  `ai_medico` int(11) DEFAULT NULL,
  `ai_clinica` int(11) DEFAULT NULL,
  `ai_caso` int(11) NOT NULL,
  `fecha_registro` datetime NOT NULL,
  `ai_status` int(11) DEFAULT NULL,
  PRIMARY KEY (`ai_id`),
  KEY `audit_informe_325c5ebb` (`ai_caso`)
) ENGINE=MyISAM AUTO_INCREMENT=53726 DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `audit_medicamento`
--

DROP TABLE IF EXISTS `audit_medicamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `audit_medicamento` (
  `amed_id` int(11) NOT NULL AUTO_INCREMENT,
  `amed_presentacion` int(11) NOT NULL,
  `amed_informe` int(11) NOT NULL,
  `amed_cantidad` int(11) NOT NULL,
  PRIMARY KEY (`amed_id`),
  KEY `audit_medicamento_3b13aeff` (`amed_presentacion`),
  KEY `audit_medicamento_4f0c8be5` (`amed_informe`)
) ENGINE=MyISAM AUTO_INCREMENT=129186 DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `audit_relpatologia`
--

DROP TABLE IF EXISTS `audit_relpatologia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `audit_relpatologia` (
  `arlp_id` int(11) NOT NULL,
  `arlp_idmedicamento` int(11) NOT NULL,
  `arlp_idpatologia` int(11) DEFAULT NULL,
  `arlp_caso` int(11) NOT NULL,
  `informe` int(11) NOT NULL,
  PRIMARY KEY (`arlp_id`),
  KEY `audit_relpatologia_3c5ef85a` (`arlp_idmedicamento`),
  KEY `audit_relpatologia_2fdbedec` (`arlp_idpatologia`),
  KEY `audit_relpatologia_79552950` (`arlp_caso`),
  KEY `audit_relpatologia_133e69f8` (`informe`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `causa`
--

DROP TABLE IF EXISTS `causa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `causa` (
  `id_causa` int(11) NOT NULL,
  `nombre_causa` varchar(150) COLLATE utf8_spanish_ci NOT NULL,
  PRIMARY KEY (`id_causa`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `causa_enfermedad`
--

DROP TABLE IF EXISTS `causa_enfermedad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `causa_enfermedad` (
  `id_causa_enf` int(11) NOT NULL,
  `enfermedad` int(11) NOT NULL,
  `causa` int(11) NOT NULL,
  PRIMARY KEY (`id_causa_enf`),
  KEY `causa_enfermedad_597cb910` (`enfermedad`),
  KEY `causa_enfermedad_6fed733b` (`causa`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ceo`
--

DROP TABLE IF EXISTS `ceo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ceo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pais` int(11) NOT NULL COMMENT 'pais asociado a keywords',
  `pagina` varchar(100) NOT NULL COMMENT 'pagina asociada a keywords',
  `keywords` text COMMENT 'keywords a meta tags',
  `description` text,
  `title` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `pagina_x_pais` (`pais`,`pagina`),
  KEY `pais` (`pais`),
  KEY `pagina` (`pagina`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8 COMMENT='tabla de meta tags por pagina y pais';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `clase_terapeutica`
--

DROP TABLE IF EXISTS `clase_terapeutica`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clase_terapeutica` (
  `id_clase` varchar(1) COLLATE utf8_spanish_ci NOT NULL,
  `id_vademecum` varchar(300) COLLATE utf8_spanish_ci NOT NULL,
  `nombre_clase` varchar(300) COLLATE utf8_spanish_ci NOT NULL,
  PRIMARY KEY (`id_clase`),
  UNIQUE KEY `id_vademecum` (`id_vademecum`),
  UNIQUE KEY `id_vademecum_2` (`id_vademecum`),
  UNIQUE KEY `id_vademecum_3` (`id_vademecum`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `clinica`
--

DROP TABLE IF EXISTS `clinica`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clinica` (
  `id_clinica` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_clinica` varchar(300) DEFAULT NULL,
  `direccion_clinica` text,
  `telefono_clinica` varchar(300) DEFAULT NULL,
  `pagina` text,
  `url_vademecum` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id_clinica`),
  KEY `url_vademecum_index` (`url_vademecum`)
) ENGINE=InnoDB AUTO_INCREMENT=12668 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `laboratorio`
--

DROP TABLE IF EXISTS `laboratorio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `laboratorio` (
  `id_laboratorio` varchar(5) COLLATE utf8_spanish_ci NOT NULL DEFAULT '',
  `nombre_laboratorio` varchar(100) COLLATE utf8_spanish_ci NOT NULL DEFAULT '',
  `abrev_laboratorio` varchar(20) COLLATE utf8_spanish_ci NOT NULL,
  `id_vademecum` varchar(200) COLLATE utf8_spanish_ci DEFAULT NULL,
  `logo` varchar(100) COLLATE utf8_spanish_ci DEFAULT NULL COMMENT 'Campo para agregar un logo al laboratorio',
  PRIMARY KEY (`id_laboratorio`),
  UNIQUE KEY `id_vademecum` (`id_vademecum`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci COMMENT='labs';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `marca_grupo`
--

DROP TABLE IF EXISTS `marca_grupo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marca_grupo` (
  `magr_id` int(11) NOT NULL,
  `magr_nombre` varchar(240) COLLATE utf8_spanish_ci NOT NULL,
  PRIMARY KEY (`magr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `medicamento`
--

DROP TABLE IF EXISTS `medicamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `medicamento` (
  `id_medicamento` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_medicamento` varchar(100) COLLATE utf8_spanish_ci NOT NULL DEFAULT '',
  `id_grupo` int(11) NOT NULL,
  `id_vademecum` varchar(200) COLLATE utf8_spanish_ci DEFAULT NULL,
  `indicaciones` text COLLATE utf8_spanish_ci COMMENT 'indicaciones de la marca',
  `keywords` text COLLATE utf8_spanish_ci COMMENT 'keywords de busqueda de la marca',
  `reacciones_adversas` text COLLATE utf8_spanish_ci,
  `posologia` text COLLATE utf8_spanish_ci,
  `contraindicaciones` text COLLATE utf8_spanish_ci,
  PRIMARY KEY (`id_medicamento`),
  KEY `medicamento_ibfk_1` (`id_grupo`)
) ENGINE=MyISAM AUTO_INCREMENT=79149 DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `medicamento_adm`
--

DROP TABLE IF EXISTS `medicamento_adm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `medicamento_adm` (
  `mdad_id` int(11) NOT NULL,
  `mdad_nombre` varchar(150) COLLATE utf8_spanish_ci NOT NULL,
  `mdad_grupo` int(11) NOT NULL,
  `mdad_dosis` int(11) NOT NULL,
  PRIMARY KEY (`mdad_id`),
  KEY `medicamento_adm_4eb6f255` (`mdad_grupo`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `medicamento_grupo`
--

DROP TABLE IF EXISTS `medicamento_grupo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `medicamento_grupo` (
  `mgrupo_id` int(11) NOT NULL,
  `mgrupo_nombre` varchar(150) COLLATE utf8_spanish_ci NOT NULL,
  PRIMARY KEY (`mgrupo_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `medicamento_presentacion`
--

DROP TABLE IF EXISTS `medicamento_presentacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `medicamento_presentacion` (
  `id_presentacion` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_presentacion` varchar(300) COLLATE utf8_spanish_ci NOT NULL DEFAULT '',
  `tipo_medicamento` varchar(100) COLLATE utf8_spanish_ci NOT NULL DEFAULT '',
  `rx_otc` varchar(100) COLLATE utf8_spanish_ci NOT NULL DEFAULT '',
  `id_medicamento` int(11) NOT NULL DEFAULT '0',
  `id_principio` int(11) NOT NULL DEFAULT '0',
  `id_laboratorio` varchar(5) COLLATE utf8_spanish_ci NOT NULL DEFAULT '',
  `forma_adm` int(11) NOT NULL,
  `mp_precio` double DEFAULT '0',
  `indicaciones` varchar(1000) COLLATE utf8_spanish_ci DEFAULT NULL,
  `id_vademecum` varchar(300) COLLATE utf8_spanish_ci DEFAULT NULL,
  `reacciones_adversas` varchar(1500) COLLATE utf8_spanish_ci DEFAULT NULL COMMENT 'Reacciones adversas que puede tener un medicamentos',
  `contraindicaciones` varchar(1500) COLLATE utf8_spanish_ci DEFAULT NULL COMMENT 'Riesgos involucrados al usar el medicamento',
  `posologia` varchar(1500) COLLATE utf8_spanish_ci DEFAULT NULL COMMENT 'Dosis en la que debe administrarse el medicamento',
  `keywords` varchar(1500) COLLATE utf8_spanish_ci DEFAULT NULL COMMENT 'Campo para agregar nombres claves por los cuales se quiere que salga en busquedas de google, se ponen separados con comas',
  `requiere_recipe` tinyint(1) DEFAULT NULL COMMENT 'indica si el medicamendo requiere ser recetado por principio activo (true=1) o por su nombre (false=0)',
  `img_presentacion` text COLLATE utf8_spanish_ci,
  `pais` int(11) DEFAULT '1' COMMENT 'FK a pais. Indica el pais al que pertenece la presentacion',
  PRIMARY KEY (`id_presentacion`),
  KEY `i2` (`id_medicamento`),
  KEY `id_principio` (`id_principio`),
  KEY `id_laboratorio` (`id_laboratorio`),
  KEY `id_medicamento` (`id_medicamento`),
  KEY `forma_adm` (`forma_adm`),
  KEY `pais` (`pais`)
) ENGINE=MyISAM AUTO_INCREMENT=68110 DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pais`
--

DROP TABLE IF EXISTS `pais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pais` (
  `pais_id` int(11) NOT NULL AUTO_INCREMENT,
  `pais_nombre` varchar(100) NOT NULL,
  `flag` text,
  `link` text NOT NULL,
  `iso_alpha` varchar(3) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '1' COMMENT 'pais activo en el vademecum',
  PRIMARY KEY (`pais_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `principio_activo`
--

DROP TABLE IF EXISTS `principio_activo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `principio_activo` (
  `id_principio` int(11) NOT NULL,
  `nombre_principio` varchar(300) COLLATE utf8_spanish_ci NOT NULL,
  `pri_grupo` int(11) NOT NULL,
  `idioma` int(11) NOT NULL DEFAULT '1' COMMENT 'Idioma del principio activo ( 1 = Espaniol, 2 = Ingles )',
  PRIMARY KEY (`id_principio`),
  KEY `principio_activo_496ed913` (`pri_grupo`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `principio_grupo`
--

DROP TABLE IF EXISTS `principio_grupo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `principio_grupo` (
  `prigrup_id` int(11) NOT NULL AUTO_INCREMENT,
  `prigrup_nombre` varchar(300) COLLATE utf8_spanish_ci NOT NULL,
  `idioma` int(11) NOT NULL DEFAULT '1' COMMENT 'Idioma del principio grupo ( 1 = Espaniol, 2 = Ingles )',
  `id_vademecum` varchar(300) COLLATE utf8_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`prigrup_id`),
  UNIQUE KEY `id_vademecum` (`id_vademecum`)
) ENGINE=MyISAM AUTO_INCREMENT=6168 DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `principio_subclase`
--

DROP TABLE IF EXISTS `principio_subclase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `principio_subclase` (
  `id_prisub` int(11) NOT NULL,
  `id_principio` int(11) NOT NULL,
  `id_subclase3` int(11) NOT NULL,
  `prisub_prio` int(11) NOT NULL,
  PRIMARY KEY (`id_prisub`),
  KEY `principio_subclase_70c81568` (`id_principio`),
  KEY `principio_subclase_5f39bc52` (`id_subclase3`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ranking_clase`
--

DROP TABLE IF EXISTS `ranking_clase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ranking_clase` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `clase` varchar(1) COLLATE utf8_spanish_ci NOT NULL,
  `total` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ranking_clase_6290ba1d` (`clase`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ranking_enfermedad`
--

DROP TABLE IF EXISTS `ranking_enfermedad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ranking_enfermedad` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `enfermedad` int(11) NOT NULL,
  `total` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ranking_enfermedad_e019cb9` (`enfermedad`)
) ENGINE=MyISAM AUTO_INCREMENT=88 DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ranking_marca`
--

DROP TABLE IF EXISTS `ranking_marca`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ranking_marca` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `marca` int(11) NOT NULL,
  `total` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ranking_marca_e83dedb` (`marca`)
) ENGINE=MyISAM AUTO_INCREMENT=101 DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ranking_medicamento`
--

DROP TABLE IF EXISTS `ranking_medicamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ranking_medicamento` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `medicamento` int(11) NOT NULL,
  `total` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ranking_medicamento_57619273` (`medicamento`)
) ENGINE=MyISAM AUTO_INCREMENT=101 DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ranking_principio`
--

DROP TABLE IF EXISTS `ranking_principio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ranking_principio` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `principio` int(11) NOT NULL,
  `total` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ranking_principio_443d718c` (`principio`)
) ENGINE=MyISAM AUTO_INCREMENT=101 DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ranking_subclase`
--

DROP TABLE IF EXISTS `ranking_subclase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ranking_subclase` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subclase` int(11) NOT NULL,
  `total` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ranking_subclase_7fa98034` (`subclase`)
) ENGINE=MyISAM AUTO_INCREMENT=101 DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sintoma`
--

DROP TABLE IF EXISTS `sintoma`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sintoma` (
  `id` int(11) NOT NULL,
  `nombre_sintoma` varchar(150) COLLATE utf8_spanish_ci NOT NULL,
  `enfermedad_relacionada` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sintoma_17ecf806` (`enfermedad_relacionada`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sintoma_enfermedad`
--

DROP TABLE IF EXISTS `sintoma_enfermedad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sintoma_enfermedad` (
  `id` int(11) NOT NULL,
  `id_sintoma` int(11) NOT NULL,
  `id_enfermedad` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sintoma_enfermedad_26b637bc` (`id_sintoma`),
  KEY `sintoma_enfermedad_2af087cb` (`id_enfermedad`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `subclase_diagnostico`
--

DROP TABLE IF EXISTS `subclase_diagnostico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `subclase_diagnostico` (
  `id_subdia` int(11) NOT NULL,
  `id_subclase` int(11) NOT NULL,
  `id_diagnostico2` int(11) NOT NULL,
  `prioridad` int(11) NOT NULL,
  PRIMARY KEY (`id_subdia`),
  KEY `subclase_diagnostico_47f0b682` (`id_subclase`),
  KEY `subclase_diagnostico_5d50e6a0` (`id_diagnostico2`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `subclase_nivel2`
--

DROP TABLE IF EXISTS `subclase_nivel2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `subclase_nivel2` (
  `sc2_id` int(11) NOT NULL,
  `id_subclase2` varchar(15) COLLATE utf8_spanish_ci NOT NULL,
  `nombre_subclase2` varchar(300) COLLATE utf8_spanish_ci NOT NULL,
  `id_subclase` int(11) NOT NULL,
  `titulo_vademecum` varchar(300) COLLATE utf8_spanish_ci NOT NULL COMMENT 'El titulo que va a salir de la subclase en la pagina de vademecum',
  `id_vademecum` varchar(200) COLLATE utf8_spanish_ci NOT NULL COMMENT 'El nombre que va a salir en el link',
  PRIMARY KEY (`sc2_id`),
  KEY `subclase_nivel2_47f0b682` (`id_subclase`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `subclase_nivel3`
--

DROP TABLE IF EXISTS `subclase_nivel3`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `subclase_nivel3` (
  `sc3_id` int(11) NOT NULL AUTO_INCREMENT,
  `id_subclase3` varchar(5) COLLATE utf8_spanish_ci NOT NULL,
  `nombre_subclase3` varchar(100) COLLATE utf8_spanish_ci NOT NULL,
  `id_subclase2` int(5) NOT NULL,
  PRIMARY KEY (`sc3_id`)
) ENGINE=MyISAM AUTO_INCREMENT=909 DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `subclase_terapeutica`
--

DROP TABLE IF EXISTS `subclase_terapeutica`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `subclase_terapeutica` (
  `sc_id` int(11) NOT NULL,
  `id_subclase` varchar(15) COLLATE utf8_spanish_ci NOT NULL,
  `nombre_subclase` varchar(300) COLLATE utf8_spanish_ci NOT NULL,
  `id_clase` varchar(15) COLLATE utf8_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`sc_id`),
  KEY `subclase_terapeutica_9226397` (`id_clase`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_diagnostico`
--

DROP TABLE IF EXISTS `tipo_diagnostico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_diagnostico` (
  `id_diagnostico` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_diagnostico` varchar(100) COLLATE utf8_spanish_ci DEFAULT NULL,
  `descripcion` varchar(500) COLLATE utf8_spanish_ci DEFAULT NULL,
  `img_diagnostico` varchar(15) COLLATE utf8_spanish_ci NOT NULL,
  `id_vademecum` varchar(200) COLLATE utf8_spanish_ci DEFAULT NULL,
  `keywords` varchar(1500) COLLATE utf8_spanish_ci DEFAULT NULL COMMENT 'Campo para agregar nombres claves por los cuales se quiere que salga en busquedas de google, se ponen separados con comas',
  PRIMARY KEY (`id_diagnostico`),
  UNIQUE KEY `id_vademecum` (`id_vademecum`)
) ENGINE=MyISAM AUTO_INCREMENT=12790 DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_diagnostico1`
--

DROP TABLE IF EXISTS `tipo_diagnostico1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_diagnostico1` (
  `id_diagnostico1` varchar(9) COLLATE utf8_spanish_ci NOT NULL,
  `nombre_tipo1` varchar(600) COLLATE utf8_spanish_ci NOT NULL,
  PRIMARY KEY (`id_diagnostico1`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_diagnostico2`
--

DROP TABLE IF EXISTS `tipo_diagnostico2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_diagnostico2` (
  `id` int(11) NOT NULL,
  `id_diagnostico2` varchar(12) COLLATE utf8_spanish_ci NOT NULL,
  `nombre_tipo2` varchar(600) COLLATE utf8_spanish_ci NOT NULL,
  `id_diagnostico1` varchar(9) COLLATE utf8_spanish_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tipo_diagnostico2_5d7ead69` (`id_diagnostico1`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_diagnosticorelacion`
--

DROP TABLE IF EXISTS `tipo_diagnosticorelacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_diagnosticorelacion` (
  `id_relacion` int(11) NOT NULL,
  `id_diagnostico` int(11) NOT NULL,
  `id_diagnostico2` int(11) NOT NULL,
  PRIMARY KEY (`id_relacion`),
  KEY `tipo_diagnosticorelacion_46532395` (`id_diagnostico`),
  KEY `tipo_diagnosticorelacion_5d50e6a0` (`id_diagnostico2`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-11-12 11:14:08
