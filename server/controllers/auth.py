# -*- coding: utf-8 -*-
import functools
from jose import jwt
from flask import current_app
from flask import Blueprint, request, jsonify, session
from mongoengine.queryset import DoesNotExist

from server.common.utils import get_request_data, sha256_encode
from server.models.user import User

url_prefix = '/auth'
app = Blueprint('auth', __name__)


def verify_token(func):
    @functools.wraps(func)
    def wrappers(*args, **kwargs):
        if 'AUTH-TOKEN' not in request.headers or 'RID' not in request.headers:
            return jsonify({'ERROR': 'does not exists AUTH-TOKEN'})

        user_id = request.headers['RID']

        if 'AUTH-TOKEN' not in session or user_id not in session['AUTH-TOKEN']:
            return jsonify({'ERROR': 'check AUTH-TOKEN'})

        token = jwt.encode({'user_id': str(user_id)}, str(current_app.config['SECRET_KEY']), algorithm='HS256')
        if token != request.headers['AUTH-TOKEN'] and session['AUTH-TOKEN'][user_id] != token:
            return jsonify({'ERROR': 'does not match AUTH-TOKEN'})

        return func(*args, **kwargs)

    return wrappers


@app.route('/token', methods=['POST'])
def get_token():
    try:
        data = get_request_data(request)
        current_app.logger.debug(f'REQUEST : {data}')
        if data is None:
            return jsonify({'ERROR': 'please enter login data...'})

        user = User.objects(_id=data['user_id']).get()
        current_app.logger.debug(f'DATABASE : {user.to_json()}')

        if sha256_encode(data['password']) != user.password:
            return jsonify({"ERROR": 'check the user_id or password...'})

        token = jwt.encode({'user_id': str(user._id)}, str(current_app.config['SECRET_KEY']), algorithm='HS256')
        current_app.logger.debug(f'TOKEN : {token}')
        session['AUTH-TOKEN'] = {data['user_id']: token}

        return jsonify({'AUTH-TOKEN': token})
    except DoesNotExist as e:
        current_app.logger.debug(e)
        return jsonify({'ERROR': str(e)})

    except Exception as e:
        current_app.logger.exception(e)
        return jsonify({'ERROR': 'Unknown error occurred.'})


@app.route('/token', methods=['DELETE'])
@verify_token
def del_token():
    try:
        user_id = request.headers['RID']
        auth = session['AUTH-TOKEN']
        del(auth[user_id])
        session['AUTH-TOKEN'] = auth
        return jsonify({'SUCCESS': 'delete token.'})
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify({'ERROR': str(e)})


@app.route('/token_check', methods=['GET'])
@verify_token
def test():
    return jsonify({'status': 'success'})

# test insert code...
@app.route('/user', methods=['PUT'])
def insert_user():
    current_app.logger.debug(f'REQUEST JSON : {request.json}')
    User(_id=request.json['userid'], name=request.json['name'], password=sha256_encode(request.json['password'])).save()
    return jsonify({'status': 'success'})














