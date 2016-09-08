CREATE DATABASE IF NOT EXISTS `lioness`;
USE `lioness`;

DROP TABLE IF EXISTS `Reviews`;

DROP TABLE IF EXISTS `Users`;

DROP TABLE IF EXISTS `ObjectTypes`;
DROP TABLE IF EXISTS `Restaurants`;

CREATE TABLE IF NOT EXISTS `Users`(
	`userID` INT NOT NULL UNIQUE AUTO_INCREMENT,
	`name` VARCHAR(255) NOT NULL,
	`title` VARCHAR(255),
	`phone` BIGINT,
	`address` VARCHAR(255),
	PRIMARY KEY(`userID`)
);

CREATE TABLE IF NOT EXISTS `Restaurants`(
	`restaurantID` INT NOT NULL UNIQUE AUTO_INCREMENT,
	`name` VARCHAR(255),
	`phone` BIGINT,
	`address` VARCHAR(255),
	`description` TEXT,
	`hours` VARCHAR(255),
	PRIMARY KEY(`restaurantID`)

);

CREATE TABLE IF NOT EXISTS `ObjectTypes`(
	`typeID` INT NOT NULL UNIQUE AUTO_INCREMENT,
	`Type` VARCHAR(255) NOT NULL,
	PRIMARY KEY(`typeID`)
);

CREATE TABLE IF NOT EXISTS `Reviews`(
	`reviewID` INT NOT NULL UNIQUE AUTO_INCREMENT,
	`reviewerID` INT NOT NULL,
	`reviewType` INT NOT NULL,
	`reviewedID` INT NOT NULL,
	`review` TEXT,
	`rating` SMALLINT,
	PRIMARY KEY(`reviewID`),
	CONSTRAINT FOREIGN KEY(`reviewerID`) REFERENCES `Users`(`userID`),
	CONSTRAINT FOREIGN KEY(`reviewType`) REFERENCES `ObjectTypes`(`typeID`)
);

INSERT INTO `Users`(`name`, `title`) VALUES('jai', 'botmaster');
INSERT INTO `Restaurants`(`name`) VALUES('Safeway');
INSERT INTO `Restaurants`(`name`) VALUES('Lucy\'s Dumplings');
INSERT INTO `Restaurants`(`name`) VALUES('The Korean Place');
INSERT INTO `Restaurants`(`name`) VALUES('Spud bar');
INSERT INTO `Restaurants`(`name`) VALUES('Shuji Sushi');
INSERT INTO `Restaurants`(`name`) VALUES('Kebabji');
INSERT INTO `Restaurants`(`name`) VALUES('Rolls');
INSERT INTO `Restaurants`(`name`) VALUES('Bay City Burrito');
INSERT INTO `Restaurants`(`name`) VALUES('Samurai');
INSERT INTO `Restaurants`(`name`) VALUES('Schnitz');
INSERT INTO `Restaurants`(`name`) VALUES('Le Resistance');
INSERT INTO `Restaurants`(`name`) VALUES('Subway');
INSERT INTO `Restaurants`(`name`) VALUES('Beer Deluxe');
INSERT INTO `Restaurants`(`name`) VALUES('The Hawthorn');
INSERT INTO `Restaurants`(`name`) VALUES('The Nevermind');
INSERT INTO `Restaurants`(`name`) VALUES('Santorini');
INSERT INTO `Restaurants`(`name`) VALUES('Zen');
INSERT INTO `Restaurants`(`name`) VALUES('Haddons');