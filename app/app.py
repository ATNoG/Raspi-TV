import admin
import api
import auth
import cherrypy
import os
import youtube
from constants import ROOT_DIR


class Root(object):
    def __init__(self):
        self.admin = admin.Admin()
        self.auth = auth
        self.api = api.Api()
        self.youtube = youtube.Youtube()

    def cors(self):
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"

    @cherrypy.expose
    def index(self):
        """
        Basic method to redirect the user to the public frontend
        """
        raise cherrypy.HTTPRedirect('/public')


if __name__ == '__main__':
    config = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 8080
        },
        '/': {
            'tools.CORS.on': True,
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.join(ROOT_DIR, 'static'),
        },
        '/public': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'public',
            'tools.staticdir.index': 'index.html'
        },
        '/admin': {
            'tools.auth_basic.on': True,
            'tools.auth_basic.realm': 'admin',
            'tools.auth_basic.checkpassword': auth.checkpassword,
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'admin',
            'tools.staticdir.index': 'index.html'
        }
    }
    cherrypy.tools.CORS = cherrypy.Tool('before_handler', Root().cors)
    cherrypy.quickstart(Root(), '/', config)
