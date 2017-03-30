import pandas

ROSTER_FILE_FIELDS = ('retrosheet_id', 'last_name', 'first_name', 'bats',
                      'throws', 'team_code', 'position')


def is_roster_path(path):
    return path.endswith('.ROS')


def load_players(file_object, file_name):
    print('loading players from {}'.format(file_name))
    year = roster_file_year(file_name)
    roster_df = pandas.read_csv(file_object, names=ROSTER_FILE_FIELDS)
    roster_df['year'] = pandas.Series([year for _ in range(len(roster_df.index))])
    return {'player': roster_df}


def roster_file_year(file_name):
    return int(file_name[3:7])
