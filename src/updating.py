import cherrypy
import json
import sqlite3 as sql

conn = sql.connect('../db/raspi-tv.sqlite', check_same_thread=False)


class Updating:
    @cherrypy.expose
    @cherrypy.tools.allow(methods=['GET'])
    def retrieveUpdates(self):
        cherrypy.response.headers['Content-Type'] = 'text/json'
        response = []

        background = conn.execute('SELECT * FROM HTMLSettings WHERE idName=?', ('background',)).fetchone()[1]
        response.append({'id': 'background', 'type': 'image', 'content': background})

        location = conn.execute('SELECT * FROM HTMLSettings WHERE idName=?', ('location',)).fetchone()[1]
        response.append({'id': 'location', 'type': 'text', 'content': location})

        locationDescription = \
        conn.execute('SELECT * FROM HTMLSettings WHERE idName=?', ('locationDescription',)).fetchone()[1]
        response.append({'id': 'location_description', 'type': 'text', 'content': locationDescription})

        return json.dumps(response)

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def updateDB(self, location, locationDescription, background):
        if (location != "NaN"):
            conn.execute('UPDATE HTMLSettings SET content=? WHERE idName=? ', (location, 'location',))
        if (locationDescription != "NaN"):
            conn.execute('UPDATE HTMLSettings SET content=? WHERE idName=? ',
                         (locationDescription, 'locationDescription',))
        if (background != "NaN"):
            conn.execute('UPDATE HTMLSettings SET content=? WHERE idName=? ', (background, 'background',))
