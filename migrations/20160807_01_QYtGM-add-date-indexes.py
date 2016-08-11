"""
Use date as the first element of unique indexes instead of home team code,
since arrange by date is much more common.
"""

from yoyo import step

__depends__ = {'20160804_01_TcYzR-initial-database-configuration'}

steps = [
    step("""
CREATE UNIQUE INDEX `game_date_home_team_code_game_no_uindex`
  ON `game` (`date`, `home_team_code`, `game_no`);
""", """
DROP INDEX `game_date_home_team_code_game_no_uindex` ON `game`;
"""),

    step("""
CREATE UNIQUE INDEX `player_year_retrosheet_team_code_uindex`
  ON `player` (`year`, `retrosheet_id`, `team_code`);
""", """
DROP INDEX `player_year_retrosheet_team_code_uindex` ON `player`;
"""),

    step("""
CREATE UNIQUE INDEX `record_game_date_game_home_team_code_game_game_no_seq_no_uindex`
  ON `record` (`game_date`, `game_home_team_code`, `game_no`, `seq_no`);
""", """
DROP INDEX `record_game_date_game_home_team_code_game_game_no_seq_no_uindex`
  ON `record`;
"""),

    step("""
CREATE UNIQUE INDEX `id_game_date_record_id_uindex`
  ON `id` (`game_date`, `game_home_team_code`, `game_no`, `seq_no`);
""", """
DROP INDEX `id_game_date_record_id_uindex` ON `id`);
"""),

    step("""
CREATE UNIQUE INDEX `version_game_date_record_id_uindex`
  ON `version` (`game_date`, `game_home_team_code`, `game_no`, `seq_no`);
""", """
DROP INDEX `version_game_date_record_id_uindex` ON `version`);
"""),

    step("""
CREATE UNIQUE INDEX `info_game_date_record_id_uindex`
  ON `info` (`game_date`, `game_home_team_code`, `game_no`, `seq_no`);
""", """
DROP INDEX `info_game_date_record_id_uindex` ON `info`;
"""),

    step("""
CREATE UNIQUE INDEX `start_game_date_record_id_uindex`
  ON `start` (`game_date`, `game_home_team_code`, `game_no`, `seq_no`);
""", """
DROP INDEX `start_game_date_record_id_uindex` ON `start`;
"""),

    step("""
CREATE UNIQUE INDEX `sub_game_date_record_id_uindex`
  ON `sub` (`game_date`, `game_home_team_code`, `game_no`, `seq_no`);
""", """
DROP INDEX `sub_game_date_record_id_uindex` ON `sub`;
"""),

    step("""
CREATE UNIQUE INDEX `play_game_date_record_id_uindex`
  ON `play` (`game_date`, `game_home_team_code`, `game_no`, `seq_no`);
""", """
DROP INDEX `play_game_date_record_id_uindex` ON `play`;
"""),

    step("""
CREATE UNIQUE INDEX `badj_game_date_record_id_uindex`
  ON `badj` (`game_date`, `game_home_team_code`, `game_no`, `seq_no`);
""", """
DROP INDEX `badj_game_date_record_id_uindex` ON `badj`;
"""),

    step("""
CREATE UNIQUE INDEX `padj_game_date_record_id_uindex`
  ON `padj` (`game_date`, `game_home_team_code`, `game_no`, `seq_no`);
""", """
DROP INDEX `padj_game_date_record_id_uindex` ON `padj`;
"""),

    step("""
CREATE UNIQUE INDEX `ladj_game_date_record_id_uindex`
  ON `ladj` (`game_date`, `game_home_team_code`, `game_no`, `seq_no`);
""", """
DROP INDEX `ladj_game_date_record_id_uindex` ON `ladj`;
"""),

    step("""
CREATE UNIQUE INDEX `data_game_date_record_id_uindex`
  ON `data` (`game_date`, `game_home_team_code`, `game_no`, `seq_no`);
""", """
DROP INDEX `data_game_date_record_id_uindex` ON `data`;
"""),

    step("""
CREATE UNIQUE INDEX `com_game_date_record_id_uindex`
  ON `com` (`game_date`, `game_home_team_code`, `game_no`, `seq_no`);
""", """
DROP INDEX `com_game_date_record_id_uindex` ON `com`;
"""),
]
