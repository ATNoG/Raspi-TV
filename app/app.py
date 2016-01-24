import admin
import auth
import cherrypy
import os
from constants import ROOT_DIR


class Root(object):
    def __init__(self):
        self.admin = admin.Admin()
        self.auth = auth

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
            'tools.sessions.on': True,
            # 'tools.sessions.storage_type': "file",
            # 'tools.sessions.storage_path': os.path.join(ROOT_DIR, 'sessions'),
            # 'tools.sessions.timeout': 60,
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
    cherrypy.quickstart(Root(), '/', config)
