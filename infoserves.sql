-- phpMyAdmin SQL Dump
-- version 3.3.2deb1
-- http://www.phpmyadmin.net
--
-- Serveur: localhost
-- Généré le : Dim 26 Septembre 2010 à 19:02
-- Version du serveur: 5.1.41
-- Version de PHP: 5.3.2-1ubuntu4.5

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de données: `b31`
--

-- --------------------------------------------------------

--
-- Structure de la table `server`
--

CREATE TABLE IF NOT EXISTS `server` (
  `id` int(10) NOT NULL,
  `game` varchar(32) NOT NULL,
  `adress` varchar(32) NOT NULL,
  `gametype` varchar(10) NOT NULL,
  UNIQUE KEY `id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Contenu de la table `server`
--

