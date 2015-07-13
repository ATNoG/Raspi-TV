#encoding=utf-8

import cherrypy
import os
import json
from md5 import md5

class Root :


    def __init__(self):
        self.idp = Login()

    @cherrypy.expose
    def index(self):
        return open("static/index.html", "r").read()

    @cherrypy.expose
    def admin(self):
        return open("static/admin.html", "r").read()

class Login :

    users=["Diogo","Daniela","Ricardo","Pedro"]
    def get_users(self):
        #db =
        #curs = db.cursor()
        #curs.execute('select username,password from users')
        #return dict(curs.fetchall())
        pass

    def encrypt_password(pw):
        return md5(pw).hexdigest()

    def check_credentials(self,user,pw):
        if user in self.users and pw!=None:
            return True
        else:
            return False



    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def login(self, user, pw):
        if  self.check_credentials(user,pw):
            #cherrypy.session[SESSION_KEY] = cherrypy.request.login = user
            response = {'status': 200, 'response': 'Wellcome','location':'/admin'}
        else:
            response = {'status': 400, 'response': 'Wrong Username','location':'/idp'}

        return json.dumps(response)

    @cherrypy.expose
    def logout(self, from_page="/"):
        sess = cherrypy.session
        username = sess.get(SESSION_KEY, None)
        sess[SESSION_KEY] = None
        if username:
            cherrypy.request.login = None
        raise cherrypy.HTTPRedirect(from_page or "/")



if __name__ == '__main__':
    conf = {'/static': {'tools.staticdir.on': True,
                        'tools.staticdir.dir': os.path.realpath("static")}}

    cherrypy.tree.mount(Root(), "/", config=conf)
    cherrypy.server.start()