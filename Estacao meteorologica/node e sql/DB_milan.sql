-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema DB_Milan
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema DB_Milan
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `DB_Milan` DEFAULT CHARACTER SET utf8 ;
USE `DB_Milan` ;

-- -----------------------------------------------------
-- Table `DB_Milan`.`leituras`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `DB_Milan`.`leituras` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `pluviosidade` INT NOT NULL,
  `vento_vel` INT NOT NULL,
  `vento_dir` VARCHAR(45) NOT NULL,
  `hora` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `umidade` INT NOT NULL,
  `luminosidade` INT NOT NULL,
  `indice_uv` INT NOT NULL,
  `pressao` INT NOT NULL,
  `altitude` INT NOT NULL,
  `CO` INT NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
