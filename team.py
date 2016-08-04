import pandas

TEAM_FILE_FIELDS = ('code', 'league', 'location', 'name')


def is_team_path(file_name):
    return file_name.startswith('TEAM')


def load_teams(file_object, file_name):
    print('loading teams from {}'.format(file_name))
    year = team_file_year(file_name)
    team_df = pandas.read_csv(file_object, names=TEAM_FILE_FIELDS)
    team_df['year'] = pandas.Series([year for _ in range(len(team_df.index))])
    return {'team': team_df}


def team_file_year(team_file_name):
    return int(team_file_name[4:8])
