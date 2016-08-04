import argparse
import multiprocessing
import sqlalchemy
import sqlalchemy.engine.url
from collections import namedtuple
from functools import partial
import os


import record
import roster
import team

ConnectionOptions = namedtuple('ConnectionOptions',
                               ('host', 'port', 'database',
                                'username', 'password'))


def main():
    args = parse_args()
    connection_options = ConnectionOptions(
        **{field: getattr(args, field) for field in ConnectionOptions._fields})
    engine = get_engine(connection_options)

    dir_path = args.retrosheet_dir
    file_paths = [os.path.join(dir_path, file_path)
                  for file_path in os.listdir(dir_path)]
    team_paths = (p for p in file_paths
                  if team.is_team_path(os.path.split(p)[1]))
    roster_paths = (p for p in file_paths
                    if roster.is_roster_path(os.path.split(p)[1]))
    record_paths = (p for p in file_paths
                    if record.is_record_path(os.path.split(p)[1]))
    go(engine, team.load_teams, team_paths)
    go(engine, roster.load_players, roster_paths)
    go(engine, record.load_records, record_paths)


def parse_args():
    arg_parser = argparse.ArgumentParser(
        description='read Retrosheet roster files into a database')

    arg_parser.add_argument('retrosheet_dir')

    # connection options
    arg_parser.add_argument('--host', default='127.0.0.1', dest='host')
    arg_parser.add_argument('--port', type=int, default=3306, dest='port')
    arg_parser.add_argument('--database', '-db',
                            default='retrosheet_event_raw', dest='database')
    arg_parser.add_argument('--username', '-u', required=True, dest='username')
    arg_parser.add_argument('--password', '-p', required=True, dest='password')

    return arg_parser.parse_args()


def get_engine(connection_options):
    url = sqlalchemy.engine.url.URL('mysql', **connection_options._asdict())
    return sqlalchemy.create_engine(url)


def go(engine, loader, file_paths):
    parse_pool = multiprocessing.Pool()
    parse_file = partial(load_retrosheet_file, loader)
    try:
        parsed_data = parse_pool.imap_unordered(parse_file, file_paths, 10)
        for data_frames in parsed_data:
            write_retrosheet_dfs(engine, data_frames)
    finally:
        parse_pool.close()
        parse_pool.join()


def load_retrosheet_file(loader, file_path):
    file_name = os.path.split(file_path)[1]
    with open(file_path) as f:
        data = loader(f, file_name)
    return data


def write_retrosheet_dfs(engine, data_frames):
    for table_name, data_frame in data_frames.items():
        data_frame.to_sql(table_name, engine, index=False, if_exists='append')


if __name__ == '__main__':
    main()
