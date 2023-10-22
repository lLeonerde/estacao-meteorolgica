-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema db_milan
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema db_milan
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `db_milan` DEFAULT CHARACTER SET utf8mb3 ;
USE `db_milan` ;

-- -----------------------------------------------------
-- Table `db_milan`.`leituras`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_milan`.`leituras` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Temperatura` INT NOT NULL,
  `Umidade` INT NOT NULL,
  `Pressao` INT NOT NULL,
  `Altitude` INT NOT NULL,
  `Indice_uv` INT NOT NULL,
  `CO` INT NOT NULL,
  `Vento_vel` INT NOT NULL,
  `Vento_dir` VARCHAR(45) NOT NULL,
  `Pluviosidade` INT NOT NULL,
  `Luminosidade` INT NOT NULL,
  `Hora` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 28
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
