
CREATE TABLE IF NOT EXISTS `nn_publish`(
    `id` INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,

    `name` VARCHAR(32) NOT NULL DEFAULT '',
    `city` VARCHAR(32) NOT NULL DEFAULT '',
    `email` VARCHAR(64) NOT NULL DEFAULT ''
);


--ALTER TABLE `nn_publish` ADD COLUMN `operator_id` INT NOT NULL DEFAULT -1;


CREATE TABLE IF NOT EXISTS `nn_album`(
    `id` INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,

    `album_name` VARCHAR(128) NOT NULL DEFAULT '',
    `artist` VARCHAR(128) NOT NULL DEFAULT ''
);


CREATE TABLE IF NOT EXISTS `nn_track`(
    `id` INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,

    `album_id` INTEGER NOT NULL DEFAULT -1,
    `order` INTEGER NOT NULL DEFAULT 1,
    `title` VARCHAR(128) NOT NULL DEFAULT '',
    `duration` VARCHAR(128) NOT NULL DEFAULT ''

);


CREATE TABLE IF NOT EXISTS `nn_user_info`(
    `id` INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_type` INTEGER NOT NULL DEFAULT 1,
    `username` VARCHAR(32) NOT NULL DEFAULT '',
    `password` VARCHAR(64) NOT NULL DEFAULT ''
);


CREATE TABLE IF NOT EXISTS `nn_user_token`(
    `id` INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` INTEGER NOT NULL DEFAULT -1,
    `token` VARCHAR(64) NOT NULL DEFAULT ''
);