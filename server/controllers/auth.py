# -*- coding: utf-8 -*-
from flask import current_app
from flask import Flask, Blueprint, request, jsonify, render_template
from mongoengine.queryset import DoesNotExist
from jose import jwt

from server.common.utils import get_request_data
from server.models.user import User

url_prefix = '/auth'
app = Blueprint('auth', __name__)


@app.route('/login', methods=['POST'])
def login():
    try:
        data = get_request_data(request)
        current_app.logger.debug(f'REQUEST : {data}')
        if data is None:
            return jsonify({'ERROR': 'please enter login data...'})

        user = User.objects(user_id=data['user_id']).get()
        current_app.logger.debug(f'DATABASE : {user.to_json()}')

        if data['password'] != user.password:
            return jsonify({"ERROR": 'check the user_id or password...'})

        token = jwt.encode({'user_id': str(user.user_id)}, str(current_app.config['SECRET_KEY']), algorithm='HS256')
        current_app.logger.debug(f'TOKEN : {token}')

        return jsonify({'AUTH-TOKEN': token})
    except DoesNotExist as e:
        current_app.logger.debug(e)
        return jsonify({'ERROR': str(e)})

    except Exception as e:
        current_app.logger.exception(e)
        return jsonify({'ERROR': 'Unknown error occurred.'})
