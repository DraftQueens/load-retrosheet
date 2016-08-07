"""
Initial database configuration
"""

from yoyo import step

__depends__ = {}

steps = [
    step("""
CREATE TABLE `team` (
  `id`   INTEGER(4) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `year` SMALLINT(2)         NOT NULL,
  `code` CHAR(3)             NOT NULL,
  `league` CHAR(1)           NOT NULL,
  `location` VARCHAR(63)     NOT NULL,
  `name` VARCHAR(63)         NOT NULL
);
CREATE UNIQUE INDEX `team_id_uindex` ON `team` (`id`);
CREATE UNIQUE INDEX `team_year_code_uindex` ON `team` (`year`, `code`);
""", "DROP TABLE `team`;"),
    step("""
CREATE TABLE `player`
(
  `id`            INT PRIMARY KEY      NOT NULL AUTO_INCREMENT,
  `retrosheet_id` CHAR(8)              NOT NULL,
  `team_code`     CHAR(3)              NOT NULL,
  `year`          SMALLINT(2)          NOT NULL,
  `last_name`     VARCHAR(255)         NOT NULL,
  `first_name`    VARCHAR(255)         NOT NULL,
  `position`      CHAR(2)              NOT NULL,
  `bats`          CHAR(1)              NOT NULL,
  `throws`        CHAR(1)              NOT NULL,
  CONSTRAINT FOREIGN KEY `player_id_team_year_code_fk` (`year`, `team_code`) REFERENCES `team` (`year`, `code`)
);
CREATE UNIQUE INDEX `player_retrosheet_team_code_year_uindex` ON `player` (`retrosheet_id`, `team_code`, `year`);
""", "DROP TABLE `player`;"),
    step("""
CREATE TABLE `game` (
  `id`             INTEGER(4)  UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `home_team_code` CHAR(3)              NOT NULL,
  `date`           DATE                 NOT NULL,
  `game_no`        TINYINT(1)  UNSIGNED NOT NULL,
  `year`           SMALLINT(2) AS (YEAR(`date`)) STORED,
  CONSTRAINT FOREIGN KEY `game_year_home_team_code_fk` (`year`, `home_team_code`) REFERENCES `team` (`year`, `code`)
);
CREATE UNIQUE INDEX `game_home_team_code_date_game_no_uindex` ON `game` (`home_team_code`, `date`, `game_no`);
""", "DROP TABLE `game`;"),
    step("""
CREATE TABLE `record` (
  `game_home_team_code` CHAR(3) NOT NULL,
  `game_date` DATE              NOT NULL,
  `game_no` TINYINT(1) UNSIGNED NOT NULL,
  `seq_no`  INTEGER(4) UNSIGNED NOT NULL,
  CONSTRAINT PRIMARY KEY (`game_home_team_code`, `game_date`, `game_no`, `seq_no`),
  CONSTRAINT FOREIGN KEY `record_game_home_team_code_game_date_game_no_fk`
    (`game_home_team_code`, `game_date`, `game_no`) REFERENCES `game` (`home_team_code`, `date`, `game_no`)
);""", "DROP TABLE `record`;"),
    step("""
CREATE TABLE `id` (
  `game_home_team_code` CHAR(3) NOT NULL,
  `game_date` DATE              NOT NULL,
  `game_no` TINYINT(1) UNSIGNED NOT NULL,
  `seq_no`  INTEGER(4) UNSIGNED NOT NULL,
  `retrosheet_id` CHAR(12)           NOT NULL,
  CONSTRAINT PRIMARY KEY (`game_home_team_code`, `game_date`, `game_no`, `seq_no`),
  CONSTRAINT FOREIGN KEY `id_record_id_fk` (`game_home_team_code`, `game_date`, `game_no`, `seq_no`) REFERENCES `record` (`game_home_team_code`, `game_date`, `game_no`, `seq_no`)
);""", "DROP TABLE `id`;"),
    step("""
CREATE TABLE `version` (
  `game_home_team_code` CHAR(3) NOT NULL,
  `game_date` DATE              NOT NULL,
  `game_no` TINYINT(1) UNSIGNED NOT NULL,
  `seq_no`  INTEGER(4) UNSIGNED NOT NULL,
  `version`   SMALLINT(2) UNSIGNED NOT NULL,
  CONSTRAINT PRIMARY KEY (`game_home_team_code`, `game_date`, `game_no`, `seq_no`),
  CONSTRAINT FOREIGN KEY `version_record_id_fk` (`game_home_team_code`, `game_date`, `game_no`, `seq_no`) REFERENCES `record` (`game_home_team_code`, `game_date`, `game_no`, `seq_no`)
);""", "DROP TABLE `version`;"),
    step("""
CREATE TABLE `info` (
  `game_home_team_code` CHAR(3) NOT NULL,
  `game_date` DATE              NOT NULL,
  `game_no` TINYINT(1) UNSIGNED NOT NULL,
  `seq_no`  INTEGER(4) UNSIGNED NOT NULL,
  `type`      VARCHAR(255)      NOT NULL,
  `data`      VARCHAR(255),
  CONSTRAINT PRIMARY KEY (`game_home_team_code`, `game_date`, `game_no`, `seq_no`),
  CONSTRAINT FOREIGN KEY `info_record_id_fk` (`game_home_team_code`, `game_date`, `game_no`, `seq_no`) REFERENCES `record` (`game_home_team_code`, `game_date`, `game_no`, `seq_no`)
);""", "DROP TABLE `info`;"),
    step("""
CREATE TABLE `start` (
  `game_home_team_code` CHAR(3) NOT NULL,
  `game_date` DATE              NOT NULL,
  `game_no` TINYINT(1) UNSIGNED NOT NULL,
  `seq_no`  INTEGER(4) UNSIGNED NOT NULL,
  `retrosheet_player_id` CHAR(8)             NOT NULL,
  `player_name`          VARCHAR(255)        NOT NULL,
  `is_home`              TINYINT(1) UNSIGNED NOT NULL,
  `batting_pos`          TINYINT(1) UNSIGNED NOT NULL,
  `fielding_pos`         TINYINT(1) UNSIGNED NOT NULL,
  CONSTRAINT PRIMARY KEY (`game_home_team_code`, `game_date`, `game_no`, `seq_no`),
  CONSTRAINT FOREIGN KEY `start_record_id_fk` (`game_home_team_code`, `game_date`, `game_no`, `seq_no`) REFERENCES `record` (`game_home_team_code`, `game_date`, `game_no`, `seq_no`)
);
CREATE INDEX `start_retrosheet_player_id_index` ON `start` (`retrosheet_player_id`);
""", "DROP TABLE `start`"),
    step("""
CREATE TABLE `sub` (
  `game_home_team_code` CHAR(3) NOT NULL,
  `game_date` DATE              NOT NULL,
  `game_no` TINYINT(1) UNSIGNED NOT NULL,
  `seq_no`  INTEGER(4) UNSIGNED NOT NULL,
  `retrosheet_player_id` CHAR(8)             NOT NULL,
  `player_name`          VARCHAR(255)        NOT NULL,
  `is_home`              TINYINT(1) UNSIGNED NOT NULL,
  `batting_pos`          TINYINT(1) UNSIGNED NOT NULL,
  `fielding_pos`         TINYINT(1) UNSIGNED NOT NULL,
  CONSTRAINT PRIMARY KEY (`game_home_team_code`, `game_date`, `game_no`, `seq_no`),
  CONSTRAINT FOREIGN KEY `sub_record_id_fk` (`game_home_team_code`, `game_date`, `game_no`, `seq_no`) REFERENCES `record` (`game_home_team_code`, `game_date`, `game_no`, `seq_no`)
);
CREATE INDEX `sub_retrosheet_player_id_index` ON `sub` (`retrosheet_player_id`);
""", "DROP TABLE `sub`;"),
    step("""
CREATE TABLE `play` (
  `game_home_team_code` CHAR(3) NOT NULL,
  `game_date` DATE              NOT NULL,
  `game_no` TINYINT(1) UNSIGNED NOT NULL,
  `seq_no`  INTEGER(4) UNSIGNED NOT NULL,
  `inning`               SMALLINT(2) UNSIGNED NOT NULL,
  `is_bottom_of_inning`  TINYINT(1) UNSIGNED  NOT NULL,
  `retrosheet_batter_id` CHAR(8)              NOT NULL,
  `count`                CHAR(2)              NOT NULL
  COMMENT '?? means missing',
  `pitches`              VARCHAR(255)         NOT NULL
  COMMENT 'empty string means missing',
  `event`                 VARCHAR(255)        NOT NULL,
  CONSTRAINT PRIMARY KEY (`game_home_team_code`, `game_date`, `game_no`, `seq_no`),
  CONSTRAINT FOREIGN KEY `play_record_id_fk` (`game_home_team_code`, `game_date`, `game_no`, `seq_no`) REFERENCES `record` (`game_home_team_code`, `game_date`, `game_no`, `seq_no`)
);
CREATE INDEX `play_retrosheet_batter_id_index` ON `play` (`retrosheet_batter_id`);
""", "DROP TABLE `play`;"),
    step("""
CREATE TABLE `badj` (
  `game_home_team_code` CHAR(3) NOT NULL,
  `game_date` DATE              NOT NULL,
  `game_no` TINYINT(1) UNSIGNED NOT NULL,
  `seq_no`  INTEGER(4) UNSIGNED NOT NULL,
  `retrosheet_player_id` CHAR(8)            NOT NULL,
  `hand`                 CHAR(1)            NOT NULL,
  CONSTRAINT PRIMARY KEY (`game_home_team_code`, `game_date`, `game_no`, `seq_no`),
  CONSTRAINT FOREIGN KEY `badj_record_id_fk` (`game_home_team_code`, `game_date`, `game_no`, `seq_no`) REFERENCES `record` (`game_home_team_code`, `game_date`, `game_no`, `seq_no`)
);""", "DROP TABLE `badj`;"),
    step("""
CREATE TABLE `padj` (
  `game_home_team_code` CHAR(3) NOT NULL,
  `game_date` DATE              NOT NULL,
  `game_no` TINYINT(1) UNSIGNED NOT NULL,
  `seq_no`  INTEGER(4) UNSIGNED NOT NULL,
  `retrosheet_player_id` CHAR(8)            NOT NULL,
  `hand`                 CHAR(1)            NOT NULL,
  CONSTRAINT PRIMARY KEY (`game_home_team_code`, `game_date`, `game_no`, `seq_no`),
  CONSTRAINT FOREIGN KEY `padj_record_id_fk` (`game_home_team_code`, `game_date`, `game_no`, `seq_no`) REFERENCES `record` (`game_home_team_code`, `game_date`, `game_no`, `seq_no`)
);
""", "DROP TABLE `padj`;"),
    step("""
CREATE TABLE `ladj` (
  `game_home_team_code` CHAR(3) NOT NULL,
  `game_date` DATE              NOT NULL,
  `game_no` TINYINT(1) UNSIGNED NOT NULL,
  `seq_no`  INTEGER(4) UNSIGNED NOT NULL,
  CONSTRAINT PRIMARY KEY (`game_home_team_code`, `game_date`, `game_no`, `seq_no`),
  CONSTRAINT FOREIGN KEY `ladj_record_id_fk` (`game_home_team_code`, `game_date`, `game_no`, `seq_no`) REFERENCES `record` (`game_home_team_code`, `game_date`, `game_no`, `seq_no`)
);
""", "DROP TABLE `ladj`;"),
    step("""
CREATE TABLE `data` (
  `game_home_team_code` CHAR(3) NOT NULL,
  `game_date` DATE              NOT NULL,
  `game_no` TINYINT(1) UNSIGNED NOT NULL,
  `seq_no`  INTEGER(4) UNSIGNED NOT NULL,
  `type`      VARCHAR(15)        NOT NULL,
  `data`      VARCHAR(255)       NOT NULL,
  CONSTRAINT PRIMARY KEY (`game_home_team_code`, `game_date`, `game_no`, `seq_no`),
  CONSTRAINT FOREIGN KEY `data_record_id_fk` (`game_home_team_code`, `game_date`, `game_no`, `seq_no`) REFERENCES `record` (`game_home_team_code`, `game_date`, `game_no`, `seq_no`)
);
""", "DROP TABLE `data`;"),
    step("""
CREATE TABLE `com` (
  `game_home_team_code` CHAR(3) NOT NULL,
  `game_date` DATE              NOT NULL,
  `game_no` TINYINT(1) UNSIGNED NOT NULL,
  `seq_no`  INTEGER(4) UNSIGNED NOT NULL,
  `comment`   TEXT               NOT NULL,
  CONSTRAINT PRIMARY KEY (`game_home_team_code`, `game_date`, `game_no`, `seq_no`),
  CONSTRAINT FOREIGN KEY `com_record_id_fk` (`game_home_team_code`, `game_date`, `game_no`, `seq_no`) REFERENCES `record` (`game_home_team_code`, `game_date`, `game_no`, `seq_no`)
);
""", "DROP TABLE `com`;")
]
