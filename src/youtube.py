import sqlite3 as sql
import cherrypy
import json
import requests

class Youtube:
    
    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def save_link(self, link):

        try:

            videoUrl = link
            videoJson = "http://www.youtube.com/oembed?url="+videoUrl+"&format=json"
            response = requests.get(videoJson)

            if response.status_code == 404:
                return json.dumps({'status': 404})

            db = sql.connect('../db/raspi-tv.sqlite')
            find_id = db.execute("SELECT * FROM YouTube WHERE VideoId = (?);", (link,)).fetchall()

            if not find_id:
                db.execute("INSERT INTO YouTube VALUES (?);", (link,))
                db.commit()
            db.close()
            return json.dumps({'status': 200})
        except Exception:
            return json.dumps({'status': 500})


    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def delete_link(self, link):
        db = sql.connect('../db/raspi-tv.sqlite')
        find_id = db.execute("SELECT * FROM YouTube WHERE VideoId = (?);", (link,)).fetchone()

        db.execute("DELETE FROM YouTube WHERE VideoId = (?);", (find_id[0],))
        db.commit()
        db.close()



