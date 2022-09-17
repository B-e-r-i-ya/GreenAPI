CREATE SCHEMA `whatsapp` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin ;
CREATE TABLE `whatsapp`.`messages` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `id_message` VARCHAR(100) NOT NULL DEFAULT 'idmessage получается от api',
  `timestamp` TIMESTAMP(6) NULL,
  `sender_chatid` VARCHAR(45) NULL DEFAULT 'id чата пользователя который пишет',
  `sender_name` VARCHAR(45) NULL DEFAULT 'имя пользователя',
  `type_message` VARCHAR(45) NULL DEFAULT 'тип сообщения',
  PRIMARY KEY (`id`, `id_messages`))
COMMENT = 'Хранение обшей информации о сообщениях';
CREATE TABLE `whatsapp`.`text_message` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `id_message` VARCHAR(45) NOT NULL,
  `text_message` VARCHAR(1000) NULL DEFAULT 'само сообщение',
  PRIMARY KEY (`id`, `id_message`))
COMMENT = 'сообщения типа textmessage';
CREATE TABLE `whatsapp`.`quote_message` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `id_message` VARCHAR(45) NULL,
  `stanza_id` VARCHAR(45) NULL,
  `text` VARCHAR(45) NULL,
  `participant` VARCHAR(45) NULL,
  PRIMARY KEY (`id`));
