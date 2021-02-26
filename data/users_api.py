from flask import jsonify, Blueprint, abort, request
from . import db_session
from .models import User

users_attrs = ('id', 'surname', 'name', 'age', 'position', 'speciality',
               'address', 'email', 'modified_date', 'city_from')
users_fields = ('surname', 'name', 'age', 'position', 'speciality',
                'address', 'email', 'modified_date', 'password', 'city_from')
db_session.global_init('db/mars_explorer.sqlite')
session = db_session.create_session()
blueprint = Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users', methods=['GET'])
def get_users():
    return jsonify({'jobs': [user.to_dict(only=users_attrs)
                             for user in session.query(User).all()]})


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    user = session.query(User).get(user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict(only=users_attrs))


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json or any(key not in request.json for key in users_fields):
        abort(400)
    tmp = request.json.copy()
    del tmp['password']
    user = User(**tmp)
    user.set_password(request.json['password'])
    session.add(user)
    session.commit()
    return jsonify({'status': 'ok'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = session.query(User).get(user_id)
    if not user:
        abort(404)
    session.delete(user)
    session.commit()
    return jsonify({'status': 'ok'})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    user = session.query(User).get(user_id)
    if not user:
        abort(404)
    if not request.json or any(key not in request.json for key in users_fields):
        abort(400)
    tmp = request.json.copy()
    del tmp['password']
    for key, value in tmp.items():
        setattr(user, key, value)
    user.set_password(request.json['password'])
    session.commit()
    return jsonify({'status': 'ok'})
