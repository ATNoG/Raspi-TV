import sqlite3 as sql
import cherrypy
import json

class Youtube:
    
    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def saveId(self, id):
        db = sql.connect('../db/raspi-tv.sqlite')
        find_id = db.execute("SELECT * FROM YouTube WHERE VideoId = (?);", (id,)).fetchall()

        if not find_id:
            db.execute("INSERT INTO YouTube VALUES (?);", (id,))
            db.commit()
        db.close()

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def deleteId(self, id):
        db = sql.connect("raspi-tv.db")
        find_id = db.execute("SELECT * FROM YouTube WHERE VideoId = (?);", (id,)).fetchall()

        if find_id:
            db.execute("DELETE FROM YouTube WHERE VideoId = (?);", (id,))



