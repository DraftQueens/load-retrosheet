import datetime
import pandas

from collections import namedtuple, OrderedDict

Field = namedtuple('Field', ('name', 'field_type'))

KEY_FIELDS = ('game_home_team_code', 'game_date', 'game_no', 'seq_no')
GAME_FIELDS = ('home_team_code', 'date', 'game_no')
DATA_FIELDS = {
    'id': (Field('retrosheet_id', str),),
    'version': (Field('version', int),),
    'info': (Field('type', str), Field('data', str)),
    'start': (
        Field('retrosheet_player_id', str),
        Field('player_name', str),
        Field('is_home', int),
        Field('batting_pos', int),
        Field('fielding_pos', int)),
    'sub': (
        Field('retrosheet_player_id', str),
        Field('player_name', str),
        Field('is_home', int),
        Field('batting_pos', int),
        Field('fielding_pos', int)),
    'play': (
        Field('inning', int),
        Field('is_bottom_of_inning', int),
        Field('retrosheet_batter_id', str),
        Field('count', str),
        Field('pitches', str),
        Field('event', str)),
    'badj': (Field('retrosheet_player_id', str), Field('hand', str)),
    'padj': (Field('retrosheet_player_id', str), Field('hand', str)),
    'ladj': (),
    'data': (Field('type', str), Field('data', str)),
    'com': (Field('comment', str),)
}


def is_record_path(file_name):
    return any(map(file_name.endswith, ('.EVA', '.EVN', '.EDA', '.EDN')))


def load_records(file_object, file_path):
    print('loading records from {}'.format(file_path))
    # initialize data frames
    key_list = []
    game_list = []
    record_lists = {record_type: [] for record_type in DATA_FIELDS.keys()}

    game_info = None
    seq_no = None
    for line in file_object:
        raw_fields = parse_raw_fields(line)
        record_type = raw_fields[0]

        # start a new game if this is a game header
        if record_type == 'id':
            seq_no = 0
            game_info = parse_game_info(raw_fields[1])
            game_list.append(game_info)

        elif game_info is not None:
            # munge
            key_fields = game_info + (seq_no,)
            data_fields = parse_fields(raw_fields[1:],
                                       DATA_FIELDS[record_type])
            all_fields = key_fields + data_fields

            # add to relevant tables
            key_list.append(key_fields)
            record_lists[record_type].append(all_fields)
            seq_no += 1

    # build the data frames to return
    game_df = pandas.DataFrame(data=game_list, columns=GAME_FIELDS)
    key_df = pandas.DataFrame(data=key_list, columns=KEY_FIELDS)

    data_frames = OrderedDict()
    data_frames['game'] = game_df
    data_frames['record'] = key_df
    for record_type, data_fields in DATA_FIELDS.items():
        field_names = tuple([field.name for field in data_fields])
        data = record_lists[record_type]
        column_names = KEY_FIELDS + field_names
        data_frames[record_type] = pandas.DataFrame(data=data,
                                                    columns=column_names)

    return data_frames


def parse_raw_fields(line):
    line = line.strip()
    fields = []
    start_idx = 0
    current_idx = 0
    state = 'in_unquoted_field'
    for char in line:
        if state == 'in_unquoted_field':
            if char == ',':
                fields.append(line[start_idx:current_idx])
                start_idx = current_idx + 1
            if char == '"':
                fail_msg = 'line \'{}\' quotes a partial field ({})'
                assert start_idx == current_idx,\
                    fail_msg.format(line, current_idx)
                state = 'in_quoted_field'
                start_idx = current_idx + 1
        elif state == 'in_quoted_field':
            if char == '"':
                fields.append(line[start_idx:current_idx])
                state = 'exiting_quoted_field'
                start_idx = current_idx + 1
        elif state == 'exiting_quoted_field':
            fail_msg = 'line \'{}\' quotes a partial field ({})'
            assert char == ',', fail_msg.format(line, current_idx)
            state = 'in_unquoted_field'
            start_idx = current_idx + 1
        current_idx += 1
    if current_idx > start_idx:
        fields.append(line[start_idx:])

    return tuple(fields)


def parse_fields(field_values, field_declarations):
    values = []
    fields = zip(field_values, field_declarations)
    return tuple([declaration.field_type(value)
                  for value, declaration in fields])


def parse_game_info(game_id):
    home_team_code = game_id[:3]
    date = datetime.datetime.strptime(game_id[3:11], '%Y%m%d').date()
    game_no = int(game_id[11])
    return home_team_code, date, game_no
