#encoding=utf-8

import cherrypy
import os
from api import Api
from idp import Login


class Root:

    def __init__(self):
        self.idp = Login()
        self.api = Api()

    @cherrypy.expose
    def index(self):
        return open("static/index.html", "r").read()

    @cherrypy.expose
    def admin(self):
        return open("static/admin.html", "r").read()


if __name__ == '__main__':
    conf = {'/static': {'tools.staticdir.on': True,
                        'tools.staticdir.dir': os.path.realpath("static")}}

    cherrypy.tree.mount(Root(), "/", config=conf)
    cherrypy.server.start()