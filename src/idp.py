import cherrypy
import json
import Crypto.Hash
import sqlite3 as sql


class Login:
    def __init__(self):
        self.conn = sql.connect('../db/raspi-tv.sqlite')
        self.c = self.conn.cursor()

    def encrypt_password(self, password):
        return Crypto.Hash.SHA256.new(password).hexdigest()

    def check_credentials(self, user, password):
        password = self.encrypt_password(password)
        return self.c.execute('SELECT COUNT(*) FROM Users WHERE UserId=? AND Password=?', (user, password)).fetchone()[0]

    @cherrypy.expose
    def index(self):
        return open("static/login.html", "r").read()

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def login(self, user, pw):
        if self.check_credentials(user, pw):
            # cherrypy.session[SESSION_KEY] = cherrypy.request.login = user
            response = {'status': 200, 'response': 'Welcome', 'location': '/admin'}
        else:
            response = {'status': 400, 'response': 'Wrong Username', 'location': '/idp'}

        return json.dumps(response)

    @cherrypy.expose
    def logout(self, from_page="/"):
        sess = cherrypy.session
        username = sess.get(SESSION_KEY, None)
        sess[SESSION_KEY] = None
        if username:
            cherrypy.request.login = None
        raise cherrypy.HTTPRedirect(from_page or "/")
