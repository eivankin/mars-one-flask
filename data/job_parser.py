import datetime as dt
from flask_restful import reqparse
from .jobs_api import DATE_FORMAT


def decode_date(date_string: str) -> dt.datetime:
    return dt.datetime.strptime(date_string, DATE_FORMAT)


parser = reqparse.RequestParser()
parser.add_argument('team_leader_id', required=True, type=int)
parser.add_argument('job', required=True)
parser.add_argument('work_size', required=True, type=int)
parser.add_argument('collaborators', required=True)
parser.add_argument('start_date', required=True, type=decode_date)
parser.add_argument('end_date', required=True, type=decode_date)
parser.add_argument('is_finished', required=True, type=bool)
parser.add_argument('categories', required=True)
