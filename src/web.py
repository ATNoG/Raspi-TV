# encoding:utf-8

import cherrypy

from api import Api
from idp import Login
from admin import Admin
from youtube import Youtube
from auth import AuthController
import webbrowser
import os
from settings import *


class Root:
    def __init__(self):
        self.idp = Login()
        self.api = Api()
        self.admin = Admin()
        self.auth = AuthController()
        self.youtube = Youtube()


    _cp_config = {
        'tools.sessions.on': True,
        'tools.auth.on': True
    }

    conf = {
        'global':
            {
                'server.socket_host': '0.0.0.0',
                'server.socket_port': 80
            },
        '/':
            {
                'tools.staticdir.root': os.path.abspath(os.path.join(return_base_dir(), 'src', 'static')),
                'tools.staticdir.on': True,
                'tools.staticdir.dir': '',
                'tools.staticdir.index': 'index.html'
            }
    }


if __name__ == '__main__':
    # webbrowser.get('firefox').open('localhost:8080/')  # Useful when auto starting on the Raspberry Pi
    cherrypy.quickstart(Root(), '/', Root.conf)
