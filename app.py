import logging
import sqlite3
import time

from flask_babel import Babel
from flask_mail import Mail, Message
from flask_restful import Api, Resource, reqparse

import config
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, url_for, render_template, request, session, redirect, make_response, abort, flash, g

app = Flask(__name__)
api = Api(app)
mail = Mail()
babel = Babel(app)
mail.init_app(app)

app.config.update(
    DEBUG=True,
    TESTING=True,
    BABEL_DEFAULT_LOCALE='zh',
    BABEL_DEFAULT_TIMEZONE='Asia/Shanghai',
    MAIL_SERVER='smtp.qq.com',
    MAIL_USERNAME='bjhee',
    MAIL_PASSWORD='example'
)

USER_LIST = {
    1: {'name': 'Michael'},
    2: {'name': 'Tom'},
}

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)


@app.route('/mail')
def send_mail():
    msg = Message('Hello',
                  sender=('Billy.J.Hee', 'bjhee@example.com'),
                  recipients=['you@example.com'])
    msg.html = '<h1>Hello World</h1>'
    mail.send(msg)
    return 'Successful'


class User(Resource):
    @staticmethod
    def abort_if_not_exit(user_id):
        if user_id not in USER_LIST:
            abort(404, message="User {} dosen't exist".format(user_id))

    def get(self, user_id):
        self.abort_if_not_exit(user_id)
        return USER_LIST[user_id]

    def delete(self, user_id):
        self.abort_if_not_exit(user_id)
        del USER_LIST[user_id]
        return f'delete {user_id} success', 204

    def put(self, user_id):
        args = parser.parse_args(strict=True)
        USER_LIST[user_id] = {'name': args['name']}
        return USER_LIST[user_id], 201


class UserList(Resource):
    def get(self):
        return USER_LIST

    def post(self):
        args = parser.parse_args(strict=True)
        user_id = int(max(USER_LIST.keys())) + 1
        USER_LIST[user_id] = {'name': args['name']}
        return USER_LIST[user_id], 201


api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<int:user_id>')
#
# app.config.from_object('config')
# app.config.from_envvar('FLASK_SETTINGS', silent=True)
#
# server_log = TimedRotatingFileHandler('server.log', 'D')
# server_log.setLevel(logging.DEBUG)
# server_log.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
#
# error_log = TimedRotatingFileHandler('error.log', 'D')
# error_log.setLevel(logging.ERROR)
# error_log.setFormatter(logging.Formatter('%(asctime)s: %(message)s [in %(pathname)s:%(lineno)d]'))
#
# app.logger.addHandler(server_log)
# app.logger.addHandler(error_log)
#
# app.secret_key = '123456'
#
#
# @app.before_request
# def before_request():
#     g.db = sqlite3.connect(app.config['DATABASE'])
#
#
# @app.teardown_request
# def teardown_request(exception):
#     db = getattr(g, 'db', None)
#     if db is not None:
#         db.close()
#
#
# @app.route('/')
# def index():
#     if 'user' in session:
#         return render_template('hello.html', name=session['user'])
#     else:
#         return redirect(url_for('login'))
#
#
# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         name = request.form['user']
#         passwd = request.form['passwd']
#         cursor = g.db.execute('select * from users where name=? and password=?', [name, passwd])
#         if cursor.fetchone() is not None:
#             session['user'] = name
#             flash('Login successfully!')
#             return redirect(url_for('index'))
#         else:
#             flash('No such user!', 'error')
#             return redirect(url_for('login'))
#     else:
#         return render_template('login.html')
#
#
# @app.route('/logout')
# def logout():
#     session.pop('user', None)
#     return redirect(url_for('login'), 302)
#
#
# @app.route('/error')
# def error():
#     app.logger.debug('Enter error method')
#     app.logger.error('404 error happened')
#     abort(404)
#
#
# @app.route('/exception')
# def exception():
#     app.logger.debug('Enter exception method')
#     app.logger.error('403 error happened')
#     raise InvalidUsage('No privilege to access the resource', status_code=403)
#
#
# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('404.html'), 404
#
#
# class InvalidUsage(Exception):
#     status_code = 400
#
#     def __init__(self, message, status_code=400):
#         Exception.__init__(self)
#         self.message = message
#         self.status_code = status_code
#
#
# @app.errorhandler(InvalidUsage)
# def invalid_usage(error):
#     response = make_response(error.message)
#     response.status_code = error.status_code
#     return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')
