# encoding:utf-8

import cherrypy

from api import Api
from idp import Login
from admin import Admin
from auth import AuthController
from updating import Updating
import webbrowser


class Root:
    def __init__(self):
        self.idp = Login()
        self.api = Api()
        self.admin = Admin()
        self.auth = AuthController()
        self.updating = Updating()
        
    _cp_config = {
        'tools.sessions.on': True,
        'tools.auth.on': True
    }


if __name__ == '__main__':
    # webbrowser.get('firefox').open('localhost:8080/')  # Useful when auto starting on the Raspberry Pi
    cherrypy.quickstart(Root(), '/', 'app.conf')
