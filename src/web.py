# encoding=utf-8

import cherrypy
import os
from api import Api
from idp import Login
from admin import Admin


class Root:
    def __init__(self):
        self.idp = Login()
        self.api = Api()
        self.admin = Admin()

    @cherrypy.expose
    def index(self):
        return open('static/index.html', 'r').read()


if __name__ == '__main__':
    cherrypy.quickstart(Root(), '/', 'app.conf')
