#encoding=utf-8

import cherrypy
import os
import json

class Login :

    users=["Diogo","Daniela","Ricardo","Pedro"]

    @cherrypy.expose
    def index(self):
        return open("static/index.html", "r").read()

    def get_admin_page(selfs):
        return open("static/admin.html", "r").read()

    def check_credentials(self,user,pw):
        if user in self.users and pw!=None:
            return True
        else:
            return False


    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def login(self, user, pw):
        if self.check_credentials(self,user,pw):
            response = {'status': 400, 'response': 'Wrong Username'}
            return json.dumps(response)

        response = {'status': 200, 'response': 'Wellcome'}
        #cherrypy.session[SESSION_KEY] = cherrypy.request.login = username
        self.get_admin_page()
        return json.dumps(response)


if __name__ == '__main__':
    conf = {'/static': {'tools.staticdir.on': True,
                        'tools.staticdir.dir': os.path.realpath("static")}}

    cherrypy.tree.mount(Login(), "/", config=conf)
    cherrypy.server.start()