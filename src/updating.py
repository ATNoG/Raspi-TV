import cherrypy
import json
import sqlite3 as sql

conn = sql.connect('../db/raspi-tv.sqlite', check_same_thread=False)


class Updating:

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def updateDB(self, location, locationDescription, background):
        if (len(location)>0):
            print "ZEEEEEEEEEEEEEEEEEEEEEEE"+str(location)
            conn.execute('UPDATE HTMLSettings SET content=? WHERE idName=? ', (location, 'location',))
        if (len(locationDescription)>0):
            conn.execute('UPDATE HTMLSettings SET content=? WHERE idName=? ',(locationDescription, 'locationDescription',))
        if (len(background)>0):
            conn.execute('UPDATE HTMLSettings SET content=? WHERE idName=? ', (background, 'background',))
