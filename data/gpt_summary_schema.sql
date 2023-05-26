-- MariaDB dump 10.19  Distrib 10.4.19-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: gpt_summary
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
-- Temporary table structure for view `source_text_view`
--

DROP TABLE IF EXISTS `source_text_view`;
DROP VIEW IF EXISTS `source_text_view`;
SET @saved_cs_client = @@character_set_client;
SET character_set_client = utf8;
SELECT USER();
CREATE TABLE `source_text_view` (
  `source_id` tinyint NOT NULL,
  `text_name` tinyint NOT NULL,
  `group_name` tinyint NOT NULL,
  `text_id` tinyint NOT NULL,
  `summary_id` tinyint NOT NULL,
  `parsed_text` tinyint NOT NULL,
  `embedding` tinyint NOT NULL,
  `moderation` tinyint NOT NULL
) ENGINE=InnoDB;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `summary_text_view`
--

DROP TABLE IF EXISTS `summary_text_view`;
DROP VIEW IF EXISTS `summary_text_view`;
SET @saved_cs_client = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `summary_text_view` (
  `proj_id` tinyint NOT NULL,
  `text_name` tinyint NOT NULL,
  `group_name` tinyint NOT NULL,
  `text_id` tinyint NOT NULL,
  `summary_id` tinyint NOT NULL,
  `level` tinyint NOT NULL,
  `parsed_text` tinyint NOT NULL,
  `embedding` tinyint NOT NULL,
  `origins` tinyint NOT NULL,
  `moderation` tinyint NOT NULL
) ENGINE=InnoDB;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `table_parsed_text`
--

DROP TABLE IF EXISTS `table_parsed_text`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `table_parsed_text` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `source` int(11) DEFAULT NULL,
  `summary_id` int(11) DEFAULT -1,
  `parsed_text` text DEFAULT NULL,
  `embedding` blob DEFAULT NULL,
  `moderation` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `table_source`
--

DROP TABLE IF EXISTS `table_source`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `table_source` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text_name` varchar(255) DEFAULT NULL,
  `group_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 COMMENT='The source doc for the parsed text';
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `table_summary_text`
--

DROP TABLE IF EXISTS `table_summary_text`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `table_summary_text` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `source` int(11) DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  `summary_id` int(11) DEFAULT -1,
  `summary_text` text DEFAULT NULL,
  `embedding` blob DEFAULT NULL,
  `origins` text DEFAULT NULL,
  `moderation` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `source_text_view`
--

DROP TABLE IF EXISTS `source_text_view`;
DROP VIEW IF EXISTS `source_text_view`;
SET @saved_cs_client          = @@character_set_client;
SET @saved_cs_results         = @@character_set_results;
SET @saved_col_connection     = @@collation_connection;
SET character_set_client      = utf8mb4;
SET character_set_results     = utf8mb4;
SET collation_connection      = utf8mb4_unicode_ci;
CREATE ALGORITHM=UNDEFINED
VIEW `source_text_view` AS select `s`.`id` AS `source_id`,`s`.`text_name` AS `text_name`,`s`.`group_name` AS `group_name`,`p`.`id` AS `text_id`,`p`.`summary_id` AS `summary_id`,`p`.`parsed_text` AS `parsed_text`,`p`.`embedding` AS `embedding`,`p`.`moderation` AS `moderation` from (`table_source` `s` join `table_parsed_text` `p` on(`p`.`source` = `s`.`id`));
SET character_set_client      = @saved_cs_client;
SET character_set_results     = @saved_cs_results;
SET collation_connection      = @saved_col_connection;

--
-- Final view structure for view `summary_text_view`
--

DROP TABLE IF EXISTS `summary_text_view`;
DROP VIEW IF EXISTS `summary_text_view`;
SET @saved_cs_client          = @@character_set_client;
SET @saved_cs_results         = @@character_set_results;
SET @saved_col_connection     = @@collation_connection;
SET character_set_client      = utf8mb4;
SET character_set_results     = utf8mb4;
SET collation_connection      = utf8mb4_unicode_ci;
CREATE ALGORITHM=UNDEFINED
VIEW `summary_text_view` AS select `ts`.`id` AS `proj_id`,`ts`.`text_name` AS `text_name`,`ts`.`group_name` AS `group_name`,`tst`.`id` AS `text_id`,`tst`.`summary_id` AS `summary_id`,`tst`.`level` AS `level`,`tst`.`summary_text` AS `parsed_text`,`tst`.`embedding` AS `embedding`,`tst`.`origins` AS `origins`,`tst`.`moderation` AS `moderation` from (`table_summary_text` `tst` join `table_source` `ts` on(`tst`.`source` = `ts`.`id`));
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

-- Dump completed on 2023-05-05  9:49:24
