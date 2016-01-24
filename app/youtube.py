import json
import subprocess

import cherrypy
import os
import requests
from constants import conn, ROOT_DIR
from download_videos import delete_video


class Youtube:
    def __init__(self):
        pass

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def save_link(self, link):

        videoUrl = link
        videoJson = 'http://www.youtube.com/oembed?url=' + videoUrl + "&format=json"

        response = requests.get(videoJson)
        if response.status_code == 404:
            return json.dumps({'status': 404})

        find_id = conn.execute('SELECT * FROM YouTube WHERE VideoId = (?);', (link,)).fetchall()

        # check if the URL wasn't added
        if len(find_id):
            return json.dumps({'status': 500})

        try:
            subprocess.Popen(["python", os.path.join(ROOT_DIR, 'download_videos.py'), link])
        except cherrypy.TimeoutError:
            pass

        return json.dumps({'status': 200})

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def delete_link(self, link):
        find_id = conn.execute('SELECT * FROM YouTube WHERE VideoId = (?);', (link,)).fetchone()
        find_name = conn.execute('SELECT VideoName FROM YouTube WHERE VideoId = (?);', (link,)).fetchone()

        delete_video(find_name[0])

        conn.execute('DELETE FROM YouTube WHERE VideoId = (?);', (find_id[0],))
        conn.commit()
