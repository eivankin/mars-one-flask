from flask import jsonify
from flask_restful import Resource
from .models import User, get_or_404
from .users_api import users_attrs
from .user_parser import parser
from . import db_session

session = db_session.create_session()


class UsersResource(Resource):
    def get(self, user_id):
        user = get_or_404(user_id, User, session)
        return jsonify(user.to_dict(only=users_attrs))

    def delete(self, user_id):
        user = get_or_404(user_id, User, session)
        session.delete(user)
        session.commit()
        return jsonify({'status': 'ok'})


class UsersListResource(Resource):
    def get(self):
        return jsonify({'users': [user.to_dict(only=users_attrs)
                                  for user in session.query(User).all()]})

    def post(self):
        args = parser.parse_args()
        password = args.pop('password')
        user = User(**args)
        user.set_password(password)
        session.add(user)
        session.commit()
        return jsonify({'status': 'ok'})
