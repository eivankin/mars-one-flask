import json
from flask import jsonify
from flask_restful import Resource
from .models import Jobs, get_or_404
from .jobs_api import job_attrs, get_categories
from .job_parser import parser
from . import db_session

session = db_session.create_session()


class JobsResource(Resource):
    def get(self, job_id):
        job = get_or_404(job_id, Jobs, session)
        return jsonify(job.to_dict(only=job_attrs))

    def delete(self, job_id):
        job = get_or_404(job_id, Jobs, session)
        session.delete(job)
        session.commit()
        return jsonify({'status': 'ok'})


class JobsListResource(Resource):
    def get(self):
        return jsonify({'jobs': [job.to_dict(only=job_attrs)
                                 for job in session.query(Jobs).all()]})

    def post(self):
        args = parser.parse_args()
        categories = get_categories(json.loads(args.pop('categories')), session)
        job = Jobs(**args)
        job.categories = categories
        session.add(job)
        session.commit()
        return jsonify({'status': 'ok'})
