from flask import request, jsonify, Blueprint, session, redirect, render_template
from datetime import datetime, timedelta
import bcrypt
import jwt
from ..db import mongo
from functools import wraps
bp = Blueprint('auth', __name__, url_prefix='/api')


@bp.route('/login', methods=('POST','GET'))
def login():
    try:

        if request.method == 'POST':
            client = mongo.Database()
            user_col = client.user_col
            auth = request.form


            if not auth:
                context = {
                    "status": False,
                    "res": 1,
                    "message": "Authorization Required",
                }

                return jsonify(context), 401

            if not auth.get('username'):
                context = {
                    "status": False,
                    "res": 1,
                    "message": "Username missing",
                }
                return jsonify(context), 401

            if not auth.get('password'):
                context = {
                    "status": False,
                    "res": 1,
                    "message": "Password missing",
                }

                return jsonify(context), 401

            user = user_col.find_one({"username": auth.get('username')})


            if not user:
                context = {"status": False, "res": 1, "message": "User not exists"}
                return jsonify(context), 401

            hashed_password = user.get("hash", "")

            is_authenticated = bcrypt.checkpw(auth.get('password').encode('utf8'),
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

            session['username'] = auth.get('username')
            session['access_token'] = token

            # return jsonify(data=user,
            #                access_token=token), 200
            return redirect('/')

        if 'username' in session:
                return redirect('/')
        return render_template('login.html')
    except Exception as e:
        print(e)
        context = {
            "status": False,
            "res": 1,
            "message": "Something went wrong",
            "result": []
        }
        return "500"



@bp.route('/logout', methods=['GET'])
def logout():

    if 'username' in session:
        del session['username']
        del session['access_token']
        return render_template('logout.html')

    return redirect('api/login')



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        try:
            token = session['access_token']
            print('access_token', token)
        except Exception as e:
            print(e)
            context = {
                "status": False,
                "res": 1,
                "message": "Token missing",
            }

            # return jsonify(context), 403
            print('111111111')
            return redirect('/api/login')

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

            # return jsonify(context), 403
            print(2222222222222)
            return redirect('/api/login')

        except jwt.exceptions.DecodeError:
            print(token)
            context = {
                "status": False,
                "res": 1,
                "message": "Invalid Token",
            }
            print(3)
            return redirect('/api/login')
        return f(*args, **kwargs)

    return decorated


def is_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        try:
            token = session['access_token']
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
        token = session['access_token']
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