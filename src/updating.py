import cherrypy
import json
import sqlite3 as sql

conn = sql.connect('../db/raspi-tv.sqlite', check_same_thread=False)


class Updating:

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def updateDB(self, location= None, locationDescription= None, background= None):
        if location:
            conn.execute('UPDATE HTMLSettings SET content=? WHERE idName=? ', (location, 'location',))
        if locationDescription:
            conn.execute('UPDATE HTMLSettings SET content=? WHERE idName=? ',(locationDescription, 'locationDescription',))
        if background:
            conn.execute('UPDATE HTMLSettings SET content=? WHERE idName=? ', (background, 'background',))
        conn.commit()