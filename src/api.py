import cherrypy
import json
import os
from ua_news import deti_news


class Api:
    @cherrypy.expose
    def get_deti_news(self):

        return json.dumps({"status": 200, "content": deti_news()})
