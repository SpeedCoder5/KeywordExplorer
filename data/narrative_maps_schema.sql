-- MariaDB dump 10.19  Distrib 10.4.19-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: narrative_maps
-- ------------------------------------------------------
-- Server version	10.4.19-MariaDB

SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT;
SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS;
SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION;
SET NAMES utf8mb4;
SET @OLD_TIME_ZONE=@@TIME_ZONE;
SET TIME_ZONE='+00:00';
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO';
SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0;

--
-- Temporary table structure for view `index_view`
--

DROP TABLE IF EXISTS `index_view`;
DROP VIEW IF EXISTS `index_view`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `index_view` (
  `experiment_id` tinyint NOT NULL,
  `run_id` tinyint NOT NULL,
  `parsed_text_id` tinyint NOT NULL,
  `gen_id` tinyint NOT NULL,
  `emb_id` tinyint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `parsed_view`
--

DROP TABLE IF EXISTS `parsed_view`;
DROP VIEW IF EXISTS `parsed_view`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `parsed_view` (
  `experiment_id` tinyint NOT NULL,
  `run_id` tinyint NOT NULL,
  `cluster_name` tinyint NOT NULL,
  `id` tinyint NOT NULL,
  `run_index` tinyint NOT NULL,
  `parsed_text` tinyint NOT NULL,
  `moderation` tinyint NOT NULL,
  `embedding` tinyint NOT NULL,
  `mapped` tinyint NOT NULL,
  `cluster_id` tinyint NOT NULL,
  `embedding_model` tinyint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `run_params_view`
--

DROP TABLE IF EXISTS `run_params_view`;
DROP VIEW IF EXISTS `run_params_view`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `run_params_view` (
  `experiment_id` tinyint NOT NULL,
  `id` tinyint NOT NULL,
  `run_id` tinyint NOT NULL,
  `prompt` tinyint NOT NULL,
  `response` tinyint NOT NULL,
  `generate_model` tinyint NOT NULL,
  `tokens` tinyint NOT NULL,
  `temp` tinyint NOT NULL,
  `presence_penalty` tinyint NOT NULL,
  `frequency_penalty` tinyint NOT NULL,
  `automated_runs` tinyint NOT NULL,
  `embedding_model` tinyint NOT NULL,
  `PCA_dim` tinyint NOT NULL,
  `EPS` tinyint NOT NULL,
  `min_samples` tinyint NOT NULL,
  `perplexity` tinyint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `run_parsed_view`
--

DROP TABLE IF EXISTS `run_parsed_view`;
DROP VIEW IF EXISTS `run_parsed_view`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `run_parsed_view` (
  `experiment_id` tinyint NOT NULL,
  `id` tinyint NOT NULL,
  `run_id` tinyint NOT NULL,
  `prompt` tinyint NOT NULL,
  `response` tinyint NOT NULL,
  `generate_model` tinyint NOT NULL,
  `embedding_model` tinyint NOT NULL,
  `line_index` tinyint NOT NULL,
  `parsed_text` tinyint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `table_embedding_params`
--

DROP TABLE IF EXISTS `table_embedding_params`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `table_embedding_params` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `model` varchar(255) DEFAULT NULL,
  `PCA_dim` int(11) DEFAULT NULL,
  `EPS` float DEFAULT NULL,
  `min_samples` int(11) DEFAULT NULL,
  `perplexity` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `table_experiment`
--

DROP TABLE IF EXISTS `table_experiment`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `table_experiment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `notes` text DEFAULT NULL COMMENT 'Notes related to experement such as sources for prompts',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `table_generate_params`
--

DROP TABLE IF EXISTS `table_generate_params`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `table_generate_params` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tokens` int(11) DEFAULT NULL,
  `temp` float DEFAULT NULL,
  `presence_penalty` float DEFAULT NULL,
  `frequency_penalty` float DEFAULT NULL,
  `model` varchar(255) DEFAULT NULL,
  `automated_runs` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `table_parsed_text`
--

DROP TABLE IF EXISTS `table_parsed_text`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `table_parsed_text` (
  `cluster_name` varchar(512) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `run_index` int(11) DEFAULT NULL,
  `parsed_text` text DEFAULT NULL,
  `moderation` text DEFAULT NULL,
  `embedding` blob DEFAULT NULL,
  `mapped` blob DEFAULT NULL,
  `cluster_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `table_run`
--

DROP TABLE IF EXISTS `table_run`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `table_run` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `experiment_id` int(11) DEFAULT NULL,
  `run_id` int(11) DEFAULT NULL,
  `prompt` text DEFAULT NULL,
  `response` text DEFAULT NULL,
  `generator_params` int(11) DEFAULT NULL,
  `embedding_params` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `index_view`
--

DROP TABLE IF EXISTS `index_view`;
DROP VIEW IF EXISTS `index_view`;
SET @saved_cs_client          = @@character_set_client;
SET @saved_cs_results         = @@character_set_results;
SET @saved_col_connection     = @@collation_connection;
SET character_set_client      = utf8mb4;
SET character_set_results     = utf8mb4;
SET collation_connection      = utf8mb4_unicode_ci;
CREATE ALGORITHM=UNDEFINED
VIEW `index_view` AS select `e`.`id` AS `experiment_id`,`r`.`id` AS `run_id`,`p`.`id` AS `parsed_text_id`,`g`.`id` AS `gen_id`,`ep`.`id` AS `emb_id` from ((((`table_experiment` `e` join `table_run` `r` on(`e`.`id` = `r`.`experiment_id`)) join `table_parsed_text` `p` on(`r`.`run_id` = `p`.`run_index`)) join `table_generate_params` `g` on(`r`.`embedding_params` = `g`.`id`)) join `table_embedding_params` `ep` on(`r`.`embedding_params` <> 0));
SET character_set_client      = @saved_cs_client;
SET character_set_results     = @saved_cs_results;
SET collation_connection      = @saved_col_connection;

--
-- Final view structure for view `parsed_view`
--

DROP TABLE IF EXISTS `parsed_view`;
DROP VIEW IF EXISTS `parsed_view`;
SET @saved_cs_client          = @@character_set_client;
SET @saved_cs_results         = @@character_set_results;
SET @saved_col_connection     = @@collation_connection;
SET character_set_client      = utf8mb4;
SET character_set_results     = utf8mb4;
SET collation_connection      = utf8mb4_unicode_ci;
CREATE ALGORITHM=UNDEFINED
VIEW `parsed_view` AS select `tr`.`experiment_id` AS `experiment_id`,`tr`.`id` AS `run_id`,`pt`.`cluster_name` AS `cluster_name`,`pt`.`id` AS `id`,`pt`.`run_index` AS `run_index`,`pt`.`parsed_text` AS `parsed_text`,`pt`.`moderation` AS `moderation`,`pt`.`embedding` AS `embedding`,`pt`.`mapped` AS `mapped`,`pt`.`cluster_id` AS `cluster_id`,`ep`.`model` AS `embedding_model` from ((`table_parsed_text` `pt` join `table_run` `tr` on(`pt`.`run_index` = `tr`.`id`)) join `table_embedding_params` `ep` on(`tr`.`embedding_params` = `ep`.`id`));
SET character_set_client      = @saved_cs_client;
SET character_set_results     = @saved_cs_results;
SET collation_connection      = @saved_col_connection;

--
-- Final view structure for view `run_params_view`
--

DROP TABLE IF EXISTS `run_params_view`;
DROP VIEW IF EXISTS `run_params_view`;
SET @saved_cs_client          = @@character_set_client;
SET @saved_cs_results         = @@character_set_results;
SET @saved_col_connection     = @@collation_connection;
SET character_set_client      = utf8mb4;
SET character_set_results     = utf8mb4;
SET collation_connection      = utf8mb4_unicode_ci;
CREATE ALGORITHM=UNDEFINED
VIEW `run_params_view` AS select `r`.`experiment_id` AS `experiment_id`,`r`.`id` AS `id`,`r`.`run_id` AS `run_id`,`r`.`prompt` AS `prompt`,`r`.`response` AS `response`,`gp`.`model` AS `generate_model`,`gp`.`tokens` AS `tokens`,`gp`.`temp` AS `temp`,`gp`.`presence_penalty` AS `presence_penalty`,`gp`.`frequency_penalty` AS `frequency_penalty`,`gp`.`automated_runs` AS `automated_runs`,`ep`.`model` AS `embedding_model`,`ep`.`PCA_dim` AS `PCA_dim`,`ep`.`EPS` AS `EPS`,`ep`.`min_samples` AS `min_samples`,`ep`.`perplexity` AS `perplexity` from ((`table_run` `r` join `table_generate_params` `gp` on(`r`.`generator_params` = `gp`.`id`)) join `table_embedding_params` `ep` on(`r`.`generator_params` = `ep`.`id`));
SET character_set_client      = @saved_cs_client;
SET character_set_results     = @saved_cs_results;
SET collation_connection      = @saved_col_connection;

--
-- Final view structure for view `run_parsed_view`
--

DROP TABLE IF EXISTS `run_parsed_view`;
DROP VIEW IF EXISTS `run_parsed_view`;
SET @saved_cs_client          = @@character_set_client;
SET @saved_cs_results         = @@character_set_results;
SET @saved_col_connection     = @@collation_connection;
SET character_set_client      = utf8mb4;
SET character_set_results     = utf8mb4;
SET collation_connection      = utf8mb4_unicode_ci;
CREATE ALGORITHM=UNDEFINED
VIEW `run_parsed_view` AS select `r`.`experiment_id` AS `experiment_id`,`r`.`id` AS `id`,`r`.`run_id` AS `run_id`,`r`.`prompt` AS `prompt`,`r`.`response` AS `response`,`gp`.`model` AS `generate_model`,`ep`.`model` AS `embedding_model`,`pt`.`id` AS `line_index`,`pt`.`parsed_text` AS `parsed_text` from (((`table_run` `r` join `table_parsed_text` `pt` on(`r`.`id` = `pt`.`run_index`)) join `table_generate_params` `gp` on(`r`.`generator_params` = `gp`.`id`)) join `table_embedding_params` `ep` on(`r`.`embedding_params` = `ep`.`id`));
SET character_set_client      = @saved_cs_client;
SET character_set_results     = @saved_cs_results;
SET collation_connection      = @saved_col_connection;
SET TIME_ZONE=@OLD_TIME_ZONE;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT;
SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS;
SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION;
SET SQL_NOTES=@OLD_SQL_NOTES;

-- Dump completed on 2023-04-28  9:43:32
