import glob
import json
import subprocess
import sys

import cherrypy
import os
import pytube
import requests
from constants import conn, ROOT_DIR


class Youtube:
    def __init__(self):
        pass

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def save_link(self, link):

        videoUrl = link
        videoJson = 'http://www.youtube.com/oembed?url=' + videoUrl + '&format=json'

        response = requests.get(videoJson)
        if response.status_code == 404:
            return json.dumps({'status': 404})

        find_id = conn.execute('SELECT * FROM YouTube WHERE VideoId = (?);', (link,)).fetchall()

        # check if the URL wasn't added
        if len(find_id):
            return json.dumps({'status': 500})

        try:
            subprocess.Popen(['python', os.path.join(ROOT_DIR, __file__), link])
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


# from https://github.com/nficano/pytube

def download(link):
    yt = pytube.YouTube()

    # Set the video URL.
    yt.from_url(link)

    # Once set, you can see all the codec and quality options YouTube has made
    # available for the particular video by printing videos.

    # pprint(yt.get_videos())

    # [<Video: MPEG-4 Visual (.3gp) - 144p>,
    # <Video: MPEG-4 Visual (.3gp) - 240p>,
    # <Video: Sorenson H.263 (.flv) - 240p>,
    # <Video: H.264 (.flv) - 360p>,
    # <Video: H.264 (.flv) - 480p>,
    # <Video: H.264 (.mp4) - 360p>,
    # <Video: H.264 (.mp4) - 720p>,
    # <Video: VP8 (.webm) - 360p>,
    # <Video: VP8 (.webm) - 480p>]

    # The filename is automatically generated based on the video title.
    # You can override this by manually setting the filename.

    # view the auto generated filename:
    # print(yt.filename)

    # Pulp Fiction - Dancing Scene [HD]

    # set the filename:
    # yt.set_filename('example')

    # You can also filter the criteria by filetype.

    # pprint(yt.filter('flv'))

    # [<Video: Sorenson H.263 (.flv) - 240p>,
    # <Video: H.264 (.flv) - 360p>,
    # <Video: H.264 (.flv) - 480p>]

    # notice that the list is ordered by lowest resolution to highest. If you
    # wanted the highest resolution available for a specific file type, you
    # can simply do:
    # print(yt.filter('mp4')[-1])
    # <Video: H.264 (.mp4) - 720p>

    # you can also get all videos for a given resolution
    mp4_videos = yt.filter(extension='mp4')

    if not len(mp4_videos):
        webm_videos = yt.filter(extension='webm')
        if not len(webm_videos):
            return json.dumps({'status': 400})
            # error message to the user, can't get the video, missing mp4 videos
        else:
            best_video = webm_videos[len(webm_videos) - 1]
    else:
        best_video = mp4_videos[len(mp4_videos) - 1]

    # [<Video: H.264 (.flv) - 480p>,
    # <Video: VP8 (.webm) - 480p>]

    # to select a video by a specific resolution and filetype you can use the get
    # method.

    video = yt.get(best_video.extension, best_video.resolution, best_video.profile)

    # NOTE: get() can only be used if and only if one object matches your criteria.
    # for example:

    # pprint(yt.videos)

    # [<Video: MPEG-4 Visual (.3gp) - 144p>,
    # <Video: MPEG-4 Visual (.3gp) - 240p>,
    # <Video: Sorenson H.263 (.flv) - 240p>,
    # <Video: H.264 (.flv) - 360p>,
    # <Video: H.264 (.flv) - 480p>,
    # <Video: H.264 (.mp4) - 360p>,
    # <Video: H.264 (.mp4) - 720p>,
    # <Video: VP8 (.webm) - 360p>,
    # <Video: VP8 (.webm) - 480p>]

    # Notice we have two H.264 (.mp4) available to us.. now if we try to call get()
    # on mp4..

    # video = yt.get('mp4')
    # MultipleObjectsReturned: get() returned more than one object -- it returned 2!

    # In this case, we'll need to specify both the codec (mp4) and resolution
    # (either 360p or 720p).

    # Okay, let's download it!
    # try:
    video.download(os.path.join(ROOT_DIR, 'static/public/data/videos/'))
    # except Exception:
    #    return json.dumps({'status': 400})
    # Downloading: Pulp Fiction - Dancing Scene.mp4 Bytes: 37561829
    # 37561829  [100.00%]

    # Note: If you wanted to choose the output directory, simply pass it as an
    # argument to the download method.
    # video.download('/tmp/')

    conn.execute('INSERT INTO YouTube VALUES (?,?,?);',
                 (link, os.path.join(ROOT_DIR, 'static/public/data/videos/' + yt.filename + '.mp4'), yt.filename))
    conn.commit()


def delete_video(name):
    # in case of mp4
    files = glob.glob(os.path.join(ROOT_DIR, 'static/public/data/videos/' + name + '.mp4'))
    for f in files:
        os.remove(f)

    # in case of webm
    files = glob.glob(os.path.join(ROOT_DIR, 'static/public/data/videos/' + name + '.webm'))
    for f in files:
        os.remove(f)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        download(sys.argv[1])
