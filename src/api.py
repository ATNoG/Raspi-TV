import cherrypy
import json
import sqlite3 as sql
from ua_news import deti_news
from weather import get_weather as get_w


class Api:
    @cherrypy.expose
    def get_deti_news(self):
        return json.dumps({"status": 200, "content": deti_news()})

    @cherrypy.expose
    def get_weather(self):
        return json.dumps({"status": 200, "content": get_w()})

    @cherrypy.expose
    def list_of_ids(self):
        db = sql.connect('../db/raspi-tv.sqlite')
        ids = db.execute("SELECT * FROM YouTube;")
        ids = ids.fetchall()
        list = []
        for i in ids:
            list.append(i[0])
        db.close()
        return json.dumps({"status": 200, "content": list})
