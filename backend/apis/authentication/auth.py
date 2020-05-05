from flask import request, jsonify, Blueprint
from datetime import datetime, timedelta
import bcrypt
import jwt
from ..db import mongo
from functools import wraps
bp = Blueprint('auth', __name__, url_prefix='/api')


@bp.route('/login', methods=('POST',))
def login():
    try:

        if request.method == 'OPTIONS':
            return jsonify({}), 204
        print(request.authorization)
        client = mongo.Database()
        user_col = client.user_col
        auth = request.authorization


        if not auth:
            context = {
                "status": False,
                "res": 1,
                "message": "Authorization Required",
            }

            return jsonify(context), 401

        if not auth.username:
            context = {
                "status": False,
                "res": 1,
                "message": "Username missing",
            }
            return jsonify(context), 401

        if not auth.password:
            context = {
                "status": False,
                "res": 1,
                "message": "Password missing",
            }

            return jsonify(context), 401
        user = user_col.find_one({"username": auth.username})


        if not user:
            context = {"status": False, "res": 1, "message": "User not exists"}
            return jsonify(context), 401

        hashed_password = user.get("hash", "")

        is_authenticated = bcrypt.checkpw(auth.password.encode('utf8'),
                                          hashed_password.encode('utf-8'))

        if not is_authenticated:
            context = {"status": False, "res": 1, "message": "Wrong password"}
            return jsonify(context), 401


        user['exp'] = datetime.utcnow() + timedelta(days=1)

        del user['hash']
        del user['_id']

        token = jwt.encode(
            user, 'skuDnaQu7oC01dy').decode('utf-8')

        print(token)

        return jsonify(data=user,
                       access_token=token), 200
    except Exception as e:
        print(e)
        context = {
            "status": False,
            "res": 1,
            "message": "Something went wrong",
            "result": []
        }
        return jsonify(context), 500





def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        try:
            token = request.headers.get('Authorization').split()[-1]
        except Exception as e:
            print(e)
            context = {
                "status": False,
                "res": 1,
                "message": "Token missing",
            }

            return jsonify(context), 403

        try:
            jwt.decode(
                token, 'skuDnaQu7oC01dy', verify=True)
        except jwt.exceptions.ExpiredSignatureError:
            # print(e)
            context = {
                "status": False,
                "res": 1,
                "message": "Token Expired",
            }

            return jsonify(context), 403

        except jwt.exceptions.DecodeError:
            # print(e)
            context = {
                "status": False,
                "res": 1,
                "message": "Invalid Token",
            }

            return jsonify(context), 403

        return f(*args, **kwargs)

    return decorated


def is_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        try:
            token = request.headers.get('Authorization').split()[-1]
        except Exception as e:
            print(e)
            context = {
                "status": False,
                "res": 1,
                "message": "Token missing",
            }

            return jsonify(context), 403

        try:
            data = jwt.decode(
                token, 'skuDnaQu7oC01dy', verify=True)

            if data.get('priviledge', '') == "admin":
                context = {
                    "status": False,
                    "res": 1,
                    "message": "Not authorized to add lock",
                }

                return jsonify(context), 403

        except jwt.exceptions.ExpiredSignatureError:
            # print(e)
            context = {
                "status": False,
                "res": 1,
                "message": "Token Expired",
            }

            return jsonify(context), 403

        except jwt.exceptions.DecodeError:
            # print(e)
            context = {
                "status": False,
                "res": 1,
                "message": "Invalid Token",
            }

            return jsonify(context), 403

        return f(*args, **kwargs)

    return decorated


def decode_token(token=None):

    if not token:
        token = request.headers.get('Authorization').split()[-1]
    try:
        data = jwt.decode(
            token, 'skuDnaQu7oC01dy', verify=True)
        return data
    except Exception as e:
        print(e)
        return


def generate_token(data):
    data['exp'] = datetime.utcnow() + timedelta(days=1)
    token = jwt.encode(
        data, 'skuDnaQu7oC01dy').decode('utf-8')
    return token