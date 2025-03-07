-- MariaDB dump 10.19  Distrib 10.4.19-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: twitter_v2
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
-- Temporary table structure for view `keyword_tweet_view`
--

DROP TABLE IF EXISTS `keyword_tweet_view`;
DROP VIEW IF EXISTS `keyword_tweet_view`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `keyword_tweet_view` (
  `name` tinyint NOT NULL,
  `experiment_id` tinyint NOT NULL,
  `start` tinyint NOT NULL,
  `end` tinyint NOT NULL,
  `keywords` tinyint NOT NULL,
  `query` tinyint NOT NULL,
  `keyword` tinyint NOT NULL,
  `author_id` tinyint NOT NULL,
  `conversation_id` tinyint NOT NULL,
  `tweet_id` tinyint NOT NULL,
  `tweet_row` tinyint NOT NULL,
  `text` tinyint NOT NULL,
  `cluster_id` tinyint NOT NULL,
  `cluster_name` tinyint NOT NULL,
  `reduced` tinyint NOT NULL,
  `is_thread` tinyint NOT NULL,
  `embedding` tinyint NOT NULL,
  `moderation` tinyint NOT NULL
) ENGINE=InnoDB;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `subsample_tweet_view`
--

DROP TABLE IF EXISTS `subsample_tweet_view`;
DROP VIEW IF EXISTS `subsample_tweet_view`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `subsample_tweet_view` (
  `row_id` tinyint NOT NULL,
  `query_id` tinyint NOT NULL,
  `conversation_id` tinyint NOT NULL,
  `is_thread` tinyint NOT NULL,
  `author_id` tinyint NOT NULL,
  `created_at` tinyint NOT NULL,
  `in_reply_to_user_id` tinyint NOT NULL,
  `lang` tinyint NOT NULL,
  `id` tinyint NOT NULL,
  `text` tinyint NOT NULL,
  `topic_name` tinyint NOT NULL,
  `moderation` tinyint NOT NULL,
  `reduced` tinyint NOT NULL,
  `cluster_id` tinyint NOT NULL,
  `cluster_name` tinyint NOT NULL,
  `embedding` tinyint NOT NULL,
  `experiment_id` tinyint NOT NULL,
  `keyword` tinyint NOT NULL
) ENGINE=InnoDB;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `table_embedding_params`
--

DROP TABLE IF EXISTS `table_embedding_params`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `table_embedding_params` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `experiment_id` int(11) DEFAULT NULL,
  `keyword` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `model` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `PCA_dim` int(11) DEFAULT NULL,
  `EPS` float DEFAULT NULL,
  `min_samples` int(11) DEFAULT NULL,
  `perplexity` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `table_exclude`
--

DROP TABLE IF EXISTS `table_exclude`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `table_exclude` (
  `experiment_id` int(11) DEFAULT NULL,
  `cluster_id` int(11) DEFAULT NULL,
  `keyword` varchar(255) DEFAULT NULL
) ENGINE=InnoDB;
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
  `sample_start` datetime DEFAULT NULL,
  `sample_end` datetime DEFAULT NULL,
  `keywords` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `table_query`
--

DROP TABLE IF EXISTS `table_query`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `table_query` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `experiment_id` int(11) DEFAULT NULL,
  `query` text DEFAULT NULL,
  `keyword` varchar(255) DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `date_executed` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `table_subsampled`
--

DROP TABLE IF EXISTS `table_subsampled`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `table_subsampled` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `experiment_id` int(11) DEFAULT NULL,
  `tweet_row` int(11) DEFAULT NULL,
  `query_row` int(11) DEFAULT NULL,
  `keyword` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `table_tweet`
--

DROP TABLE IF EXISTS `table_tweet`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `table_tweet` (
  `row_id` int(11) NOT NULL AUTO_INCREMENT,
  `query_id` int(11) DEFAULT NULL,
  `conversation_id` bigint(20) DEFAULT NULL,
  `is_thread` tinyint(1) DEFAULT 0,
  `author_id` bigint(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `in_reply_to_user_id` bigint(20) DEFAULT NULL,
  `lang` varchar(255) DEFAULT NULL,
  `id` bigint(20) NOT NULL,
  `text` text DEFAULT NULL,
  `topic_name` varchar(255) DEFAULT NULL,
  `moderation` text DEFAULT NULL,
  `reduced` blob DEFAULT NULL,
  `cluster_id` int(11) DEFAULT NULL,
  `cluster_name` varchar(255) DEFAULT NULL,
  `embedding` blob DEFAULT NULL,
  PRIMARY KEY (`row_id`),
  UNIQUE KEY `value` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `table_user`
--

DROP TABLE IF EXISTS `table_user`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `table_user` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `location` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `username` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `verified` tinyint(1) DEFAULT NULL,
  UNIQUE KEY `table_user_id_uindex` (`id`)
) ENGINE=InnoDB;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `tweet_user_cluster_view`
--

DROP TABLE IF EXISTS `tweet_user_cluster_view`;
DROP VIEW IF EXISTS `tweet_user_cluster_view`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `tweet_user_cluster_view` (
  `experiment_id` tinyint NOT NULL,
  `keyword` tinyint NOT NULL,
  `text` tinyint NOT NULL,
  `created_at` tinyint NOT NULL,
  `is_thread` tinyint NOT NULL,
  `lang` tinyint NOT NULL,
  `cluster_id` tinyint NOT NULL,
  `exclude` tinyint NOT NULL,
  `name` tinyint NOT NULL,
  `username` tinyint NOT NULL,
  `location` tinyint NOT NULL,
  `description` tinyint NOT NULL
) ENGINE=InnoDB;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `keyword_tweet_view`
--

DROP TABLE IF EXISTS `keyword_tweet_view`;
DROP VIEW IF EXISTS `keyword_tweet_view`;
SET @saved_cs_client          = @@character_set_client;
SET @saved_cs_results         = @@character_set_results;
SET @saved_col_connection     = @@collation_connection;
SET character_set_client      = utf8mb4;
SET character_set_results     = utf8mb4;
SET collation_connection      = utf8mb4_unicode_ci;
CREATE ALGORITHM=UNDEFINED
VIEW `keyword_tweet_view` AS select `te`.`name` AS `name`,`te`.`id` AS `experiment_id`,`te`.`sample_start` AS `start`,`te`.`sample_end` AS `end`,`te`.`keywords` AS `keywords`,`tq`.`query` AS `query`,`tq`.`keyword` AS `keyword`,`tt`.`author_id` AS `author_id`,`tt`.`conversation_id` AS `conversation_id`,`tt`.`id` AS `tweet_id`,`tt`.`row_id` AS `tweet_row`,`tt`.`text` AS `text`,`tt`.`cluster_id` AS `cluster_id`,`tt`.`cluster_name` AS `cluster_name`,`tt`.`reduced` AS `reduced`,`tt`.`is_thread` AS `is_thread`,`tt`.`embedding` AS `embedding`,`tt`.`moderation` AS `moderation` from ((`table_experiment` `te` join `table_query` `tq` on(`te`.`id` = `tq`.`experiment_id`)) join `table_tweet` `tt` on(`tq`.`id` = `tt`.`query_id`));
SET character_set_client      = @saved_cs_client;
SET character_set_results     = @saved_cs_results;
SET collation_connection      = @saved_col_connection;

--
-- Final view structure for view `subsample_tweet_view`
--

DROP TABLE IF EXISTS `subsample_tweet_view`;
DROP VIEW IF EXISTS `subsample_tweet_view`;
SET @saved_cs_client          = @@character_set_client;
SET @saved_cs_results         = @@character_set_results;
SET @saved_col_connection     = @@collation_connection;
SET character_set_client      = utf8mb4;
SET character_set_results     = utf8mb4;
SET collation_connection      = utf8mb4_unicode_ci;
CREATE ALGORITHM=UNDEFINED
VIEW `subsample_tweet_view` AS select `tt`.`row_id` AS `row_id`,`tt`.`query_id` AS `query_id`,`tt`.`conversation_id` AS `conversation_id`,`tt`.`is_thread` AS `is_thread`,`tt`.`author_id` AS `author_id`,`tt`.`created_at` AS `created_at`,`tt`.`in_reply_to_user_id` AS `in_reply_to_user_id`,`tt`.`lang` AS `lang`,`tt`.`id` AS `id`,`tt`.`text` AS `text`,`tt`.`topic_name` AS `topic_name`,`tt`.`moderation` AS `moderation`,`tt`.`reduced` AS `reduced`,`tt`.`cluster_id` AS `cluster_id`,`tt`.`cluster_name` AS `cluster_name`,`tt`.`embedding` AS `embedding`,`ts`.`experiment_id` AS `experiment_id`,`ts`.`keyword` AS `keyword` from (`table_subsampled` `ts` join `table_tweet` `tt` on(`ts`.`tweet_row` = `tt`.`row_id`));
SET character_set_client      = @saved_cs_client;
SET character_set_results     = @saved_cs_results;
SET collation_connection      = @saved_col_connection;

--
-- Final view structure for view `tweet_user_cluster_view`
--

DROP TABLE IF EXISTS `tweet_user_cluster_view`;
DROP VIEW IF EXISTS `tweet_user_cluster_view`;
SET @saved_cs_client          = @@character_set_client;
SET @saved_cs_results         = @@character_set_results;
SET @saved_col_connection     = @@collation_connection;
SET character_set_client      = utf8mb4;
SET character_set_results     = utf8mb4;
SET collation_connection      = utf8mb4_unicode_ci;
CREATE ALGORITHM=UNDEFINED
VIEW `tweet_user_cluster_view` AS select `te`.`id` AS `experiment_id`,`tq`.`keyword` AS `keyword`,`tt`.`text` AS `text`,`tt`.`created_at` AS `created_at`,`tt`.`is_thread` AS `is_thread`,`tt`.`lang` AS `lang`,`tt`.`cluster_id` AS `cluster_id`,if(`tt`.`cluster_id` = `tex`.`cluster_id`,1,0) AS `exclude`,`tu`.`name` AS `name`,`tu`.`username` AS `username`,`tu`.`location` AS `location`,`tu`.`description` AS `description` from ((((`table_experiment` `te` join `table_query` `tq` on(`te`.`id` = `tq`.`experiment_id`)) join `table_tweet` `tt` on(`tq`.`id` = `tt`.`query_id`)) join `table_user` `tu` on(`tu`.`id` = `tt`.`author_id`)) left join `table_exclude` `tex` on(`tt`.`cluster_id` = `tex`.`cluster_id`));
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

-- Dump completed on 2023-04-28  9:43:47
