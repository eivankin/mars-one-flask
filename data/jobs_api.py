from flask import jsonify, Blueprint, abort
from . import db_session
from .models import Jobs

db_session.global_init('db/mars_explorer.sqlite')
session = db_session.create_session()
blueprint = Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    return jsonify({'news': [job.to_dict(
        only=('job', 'team_leader_id', 'work_size', 'collaborators',
              'is_finished', 'start_date', 'end_date'))
        for job in session.query(Jobs).all()]})


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404)
    return jsonify(job.to_dict(
        only=('job', 'team_leader_id', 'work_size', 'collaborators',
              'is_finished', 'start_date', 'end_date')))
