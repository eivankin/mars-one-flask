import datetime as dt
from flask import jsonify, Blueprint, abort, request
from . import db_session
from .models import Jobs, Category

job_attrs = ('id', 'job', 'team_leader_id', 'work_size', 'collaborators',
             'is_finished', 'start_date', 'end_date', 'categories.id')
job_fields = ('job', 'team_leader_id', 'work_size', 'collaborators',
              'is_finished', 'start_date', 'end_date', 'categories')
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
db_session.global_init('db/mars_explorer.sqlite')
session = db_session.create_session()
blueprint = Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    return jsonify({'jobs': [job.to_dict(only=job_attrs)
                             for job in session.query(Jobs).all()]})


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404)
    return jsonify(job.to_dict(only=job_attrs))


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json or any(key not in request.json for key in job_fields):
        abort(400)
    tmp = request.json.copy()
    del tmp['categories'], tmp['end_date'], tmp['start_date']
    job = Jobs(**tmp, categories=session.query(Category).filter(
        Category.id.in_(request.json['categories'])).all(),
               start_date=dt.datetime.strptime(request.json['start_date'], DATE_FORMAT),
               end_date=dt.datetime.strptime(request.json['end_date'], DATE_FORMAT))
    session.add(job)
    session.commit()
    return jsonify({'status': 'ok'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404)
    session.delete(job)
    session.commit()
    return jsonify({'status': 'ok'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def edit_job(job_id):
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404)
    if not request.json or any(key not in request.json for key in job_fields):
        abort(400)
    tmp = request.json.copy()
    del tmp['categories'], tmp['end_date'], tmp['start_date']
    for key, value in tmp.items():
        setattr(job, key, value)
    job.categories = session.query(Category).filter(
        Category.id.in_(request.json['categories'])).all()
    job.start_date = dt.datetime.strptime(request.json['start_date'], DATE_FORMAT)
    job.end_date = dt.datetime.strptime(request.json['end_date'], DATE_FORMAT)
    session.commit()
    return jsonify({'status': 'ok'})
