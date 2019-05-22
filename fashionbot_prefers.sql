-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: localhost    Database: fashionbot
-- ------------------------------------------------------
-- Server version	5.7.21-log

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
-- Table structure for table `prefers`
--

DROP TABLE IF EXISTS `prefers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `prefers` (
  `user_id` int(11) NOT NULL,
  `label_id` int(11) NOT NULL,
  `rating` double DEFAULT '0',
  PRIMARY KEY (`user_id`,`label_id`),
  KEY `label_id` (`label_id`),
  CONSTRAINT `prefers_ibfk_1` FOREIGN KEY (`label_id`) REFERENCES `label` (`id`),
  CONSTRAINT `prefers_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prefers`
--

LOCK TABLES `prefers` WRITE;
/*!40000 ALTER TABLE `prefers` DISABLE KEYS */;
INSERT INTO `prefers` VALUES (1,1,3.5),(1,2,4.5),(1,3,4),(1,4,0),(1,5,0),(1,6,4.8),(1,7,0),(2,1,0),(2,2,4),(2,3,3.5),(2,4,0),(2,5,0),(2,6,5),(2,7,3),(3,1,4),(3,2,0),(3,3,2),(3,4,3),(3,5,4),(3,6,3),(3,7,4.2),(4,1,3.6),(4,2,2.4),(4,3,4.5),(4,4,4),(4,5,5),(4,6,2),(4,7,2);
/*!40000 ALTER TABLE `prefers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-05-20  0:20:44
