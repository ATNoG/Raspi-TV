import cherrypy
import json
from Crypto.Hash import SHA256
import sqlite3 as sql


class Login:
    def __init__(self):
        self.db = sql.connect('../db/raspi-tv.sqlite', check_same_thread=False)

    def encrypt_password(self, password):
        return SHA256.new(password).hexdigest()

    def check_credentials(self, user, password):
        password = self.encrypt_password(password)
        db_password = self.db.execute('SELECT Password FROM Users WHERE UserId=?', (user,)).fetchone()
        if db_password:
            if (password,) == db_password:
                # both user and password are correct
                return 1
            else:
                # password is wrong
                return 0
        else:
            # user doesnt exist
            return -1

    @cherrypy.expose
    def index(self):
        return open("static/html/login.html", "r").read()

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def login(self, user, pw):
        if self.check_credentials(user, pw) == 1:
            response = {'status': 200, 'response': 'Redirecting...', 'location': '/admin'}
        elif self.check_credentials(user, pw) == 0:
            response = {'status': 400, 'response': 'Wrong Password', 'location': '/idp'}
        else:
            response = {'status': 400, 'response': 'Wrong Username', 'location': '/idp'}

        return json.dumps(response)
