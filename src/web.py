# encoding:utf-8

import cherrypy

from api import Api
from idp import Login
from admin import Admin
from auth import AuthController, SESSION_KEY


class Root:
    def __init__(self):
        self.idp = Login()
        self.api = Api()
        self.admin = Admin()
        self.auth = AuthController()

    _cp_config = {
        'tools.sessions.on': True,
        'tools.auth.on': True
    }


if __name__ == '__main__':
    cherrypy.quickstart(Root(), '/', 'app.conf')
