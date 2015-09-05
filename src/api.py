import cherrypy
import json
import os
import sqlite3 as sql
from ua_news import deti_news
from weather import get_weather as get_w

conn = sql.connect('../db/raspi-tv.sqlite', check_same_thread=False)

class Api:
    @cherrypy.expose
    def get_deti_news(self):
        return json.dumps({"status": 200, "content": deti_news()})

    @cherrypy.expose
    def get_weather(self):
        return json.dumps({"status": 200, "content": get_w()})

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['GET'])
    def get_HTMLChanges(self):
        cherrypy.response.headers['Content-Type'] = 'text/json'
        response = []

        background = conn.execute('SELECT * FROM HTMLSettings WHERE idName=?', ('background',)).fetchone()[1]
        response.append({'id': 'background', 'type': 'image', 'content': background})

        location = conn.execute('SELECT * FROM HTMLSettings WHERE idName=?', ('location',)).fetchone()[1]
        response.append({'id': 'location', 'type': 'text', 'content': location})

        locationDescription = conn.execute('SELECT * FROM HTMLSettings WHERE idName=?', ('locationDescription',)).fetchone()[1]
        response.append({'id': 'location_description', 'type': 'text', 'content': locationDescription})

        weather = conn.execute('SELECT * FROM HTMLSettings WHERE idName=?', ('weather',)).fetchone()[1]
        response.append({'id': 'weather', 'type': 'text', 'content': weather})

        feed = conn.execute('SELECT * FROM HTMLSettings WHERE idName=?', ('feed',)).fetchone()[1]
        response.append({'id': 'feed', 'type': 'text', 'content': feed})

        return json.dumps(response)

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['GET'])
    def list_of_links(self):
        ids = conn.execute("SELECT * FROM YouTube;")
        ids = ids.fetchall()
        list = []
        for i in ids:
            list.append(i[0])
        return json.dumps({"status": 200, "content": list})

