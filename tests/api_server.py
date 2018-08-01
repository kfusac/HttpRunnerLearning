import json
from functools import wraps

from flask import Flask, make_response, request

app = Flask(__name__)
''' storage user data
data structure:
    user_dict = {
        'uid1':{
            'name':'name1',
            'password':'pwd1
        },
        'uid2':{
            'name':'name2',
            'password':'pwd2'
        }
    }
'''
users_dict = {}
''' storage token data
data structure:
    token_dict = {
        'token1':'token1-str',
        'token2':'token2-str'
    }
'''
token_dict = {}


@app.route('/')
def index():
    return 'Hello world'


@app.route('/api/users')
def get_users():
    users_list = [user for uid, user in users_dict.items()]
    data = {'data': users_list, 'count': len(users_list)}
    result = make_result(True, data, 'suc')
    status_code = 200
    return create_response(result, status_code)


@app.route('/api/reset-all')
def clean_users():
    users_dict.clear()
    result = make_result(True, {}, 'suc')
    status_code = 200
    return create_response(result, status_code)


@app.route('/api/users/<int:uid>', methods=['POST'])
def create_user(uid):
    user = request.get_json() or json.loads(request.data)
    if uid not in users_dict:
        result = make_result(True, user, 'user created successful')
        status_code = 200
        users_dict[uid] = user
    else:
        result = make_result(False, {}, 'user already exist.')
        status_code = 500
    return create_response(result, status_code)


@app.route('/api/users/<int:uid>')
def get_user(uid):
    user = users_dict.get(uid, {})
    if user:
        result = make_result(True, user, 'suc')
        status_code = 200
    else:
        result = make_result(False, user, 'uid not exist.')
        status_code = 500
    return create_response(result, status_code)


@app.route('/api/users/<int:uid>', methods=['PUT'])
def update_user(uid):
    user = users_dict.get(uid, {})
    if user:
        user = request.get_json() or json.loads(request.data)
        success = True
        status_code = 200
        msg = 'updata success.'
        users_dict[uid] = user
    else:
        success = False
        status_code = 500
        msg = 'uid not exist.'
    result = make_result(success, user, msg)
    return create_response(result, status_code)


@app.route('/api/users/<int:uid>', methods=['DELETE'])
def delete_user(uid):
    user = users_dict.pop(uid, {})
    if user:
        success = True
        status_code = 200
        msg = 'delete success.'
    else:
        success = False
        status_code = 500
        msg = 'uid not exist.'
    result = make_result(success, user, msg)
    return create_response(result, status_code)


def make_result(success, data, msg):
    return {'success': success, 'data': data, 'msg': msg}


def create_response(result, status_code):
    response = make_response(json.dumps(result), status_code)
    response.headers['Content-Type'] = 'application/json'
    return response
