import sqlite3 as sql
import cherrypy
import json
import requests
from download_videos import download
from download_videos import delete_video

class Youtube:
    
    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def save_link(self, link):

        videoUrl = link
        videoJson = "http://www.youtube.com/oembed?url="+videoUrl+"&format=json"

        try:
            response = requests.get(videoJson)
            if response.status_code == 404:
                return json.dumps({'status': 404})
        except Exception:
            return json.dumps({'status': 500})

        try:
            response = download(link)
        except cherrypy.TimeoutError:
            pass

        return response

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def delete_link(self, link):
        db = sql.connect('../db/raspi-tv.sqlite')
        find_id = db.execute("SELECT * FROM YouTube WHERE VideoId = (?);", (link,)).fetchone()
        find_name = db.execute("SELECT VideoName FROM YouTube WHERE VideoId = (?);", (link,)).fetchone()

        delete_video(find_name[0])

        db.execute("DELETE FROM YouTube WHERE VideoId = (?);", (find_id[0],))
        db.commit()
        db.close()



