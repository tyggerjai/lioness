CREATE DATABASE IF NOT EXISTS `lioness`;
USE `lioness`;

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
	`review` TEXT,
	`rating` SMALLINT,
	PRIMARY KEY(`reviewID`,`reviewType`),
	CONSTRAINT FOREIGN KEY(`reviewerID`) REFERENCES `Users`(`userID`),
	CONSTRAINT FOREIGN KEY(`reviewType`) REFERENCES `ObjectTypes`(`typeID`)
);

