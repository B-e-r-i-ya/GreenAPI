CREATE SCHEMA `whatsapp` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin ;
CREATE TABLE `whatsapp`.`messages` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `id_message` VARCHAR(100) NOT NULL DEFAULT 'idmessage получается от api',
  `timestamp` VARCHAR(45) NULL DEFAULT 'время сообщения',
  `sender_chatid` VARCHAR(45) NULL DEFAULT 'id чата пользователя который пишет',
  `sender_name` VARCHAR(45) NULL DEFAULT 'имя пользователя',
  `type_message` VARCHAR(45) NULL DEFAULT 'тип сообщения',
  PRIMARY KEY (`id`, `id_message`))
COMMENT = 'Хранение обшей информации о сообщениях';
CREATE TABLE `whatsapp`.`text_message` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `id_message` VARCHAR(45) NOT NULL,
  `text_message` VARCHAR(1000) NULL DEFAULT 'само сообщение',
  PRIMARY KEY (`id`, `id_message`))
COMMENT = 'сообщения типа textmessage';
CREATE TABLE `whatsapp`.`extended_text_message` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `id_message` VARCHAR(45) NOT NULL,
  `text` VARCHAR(1000) NULL DEFAULT 'ссылка',
  `description` VARCHAR(1000) NULL DEFAULT 'заголовок ссылки',
  `title` VARCHAR(1000) NULL DEFAULT 'заголовок ссылки',
  `jpegThumbnail` VARCHAR(1000) NULL DEFAULT 'ссылка на картинку',
  PRIMARY KEY (`id`, `id_message`))
COMMENT = 'сообщения типа extendedTextMessage';
CREATE TABLE `whatsapp`.`mediaMessage` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `id_message` VARCHAR(45) NOT NULL,
  `downloadUrl` VARCHAR(1000) NULL DEFAULT 'ссылка для скачивания файла',
  `caption` VARCHAR(1000) NULL DEFAULT 'подпись',
  `path` VARCHAR(1000) NULL DEFAULT 'путь для сохранения файла',
  PRIMARY KEY (`id`, `id_message`))
COMMENT = 'сообщения типа imageMessage';
CREATE TABLE `whatsapp`.`buttonsResponseMessage` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `id_message` VARCHAR(45) NOT NULL,
  `stanzaId` VARCHAR(1000) NULL DEFAULT 'stanzaId',
  `selectedButtonId` VARCHAR(1000) NULL DEFAULT 'selectedButtonId',
  `selectedButtonText` VARCHAR(1000) NULL DEFAULT 'текст кнопки',
  PRIMARY KEY (`id`, `id_message`))
COMMENT = 'сообщения типа buttonsResponseMessage, посути нажатие кнопки';
CREATE TABLE `whatsapp`.`quote_message` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `id_message` VARCHAR(45) NULL,
  `stanza_id` VARCHAR(45) NULL,
  `text` VARCHAR(45) NULL,
  `participant` VARCHAR(45) NULL,
  PRIMARY KEY (`id`));
CREATE TABLE `whatsapp`.`log` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `id_message` VARCHAR(45) NOT NULL,
  `timestamp` VARCHAR(45) NULL DEFAULT 'время сообщения',
  `json` VARCHAR(1000) NULL DEFAULT 'stanzaId',
  PRIMARY KEY (`id`, `id_message`))
COMMENT = 'все что не обрабатывается';
CREATE TABLE `whatsapp`.`stage` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `chatid` VARCHAR(45) NOT NULL,
  `timestamp` VARCHAR(45) NOT NULL,
  `stage` VARCHAR(1000) NULL DEFAULT 'Этап общения с клиентом',
  PRIMARY KEY (`id`, `chatid`))
COMMENT = 'все что не обрабатывается';
CREATE TABLE `whatsapp`.`stage_error` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `chatid` VARCHAR(45) NOT NULL,
  `timestamp` VARCHAR(45) NOT NULL,
  `stage` VARCHAR(1000) NULL DEFAULT 'Колличество ошибок',
  PRIMARY KEY (`id`, `chatid`))
COMMENT = 'все что не обрабатывается';
