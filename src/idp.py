import cherrypy
import json
from Crypto.Hash import SHA256
import sqlite3 as sql


class Login:
    def __init__(self):
        self.dbname = '../db/raspi-tv.sqlite'
        #self.c = self.conn.cursor()

    def encrypt_password(self, password):
        hash = SHA256.new()
        hash.update(password)
        return hash.hexdigest()

    def check_credentials(self, user, password):
        password = self.encrypt_password(password)
        with sql.connect(self.dbname) as c:
            user_and_pass= c.execute('SELECT COUNT(*) FROM Users WHERE UserId=? AND Password=?', (user, password)).fetchone()[0]
            just_user=c.execute('SELECT COUNT(*) FROM Users WHERE UserId=?', (user,)).fetchone()[0]

        if user_and_pass>0:
            #both user and password are correct
            return 1
        elif just_user>0:
            #password is wrong
            return 0
        else:
            #user doesnt exist
            return -1


    @cherrypy.expose
    def index(self):
        return open("static/login.html", "r").read()

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def login(self, user, pw):
        if self.check_credentials(user, pw) == 1:
            # cherrypy.session[SESSION_KEY] = cherrypy.request.login = user
            response = {'status': 200, 'response': 'Wellcome', 'location': '/admin'}
        elif self.check_credentials(user, pw) == 0:
            response = {'status': 400, 'response': 'Wrong Password', 'location': '/idp'}
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
