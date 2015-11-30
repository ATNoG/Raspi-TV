from pytube import YouTube
import sqlite3 as sql
# not necessary, just for demo purposes
from pprint import pprint
import json
import os
import glob
import sys
from settings import *


# from https://github.com/nficano/pytube
def download(link):
    yt = YouTube()

    # Set the video URL.
    yt.from_url(link)

    # Once set, you can see all the codec and quality options YouTube has made
    # available for the perticular video by printing videos.

    pprint(yt.videos)

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
    print(yt.filename)

    # Pulp Fiction - Dancing Scene [HD]

    # set the filename:
    # yt.set_filename('example')

    # You can also filter the criteria by filetype.

    #pprint(yt.filter('flv'))

    #[<Video: Sorenson H.263 (.flv) - 240p>,
    # <Video: H.264 (.flv) - 360p>,
    # <Video: H.264 (.flv) - 480p>]

    # notice that the list is ordered by lowest resolution to highest. If you
    # wanted the highest resolution available for a specific file type, you
    # can simply do:
    #print(yt.filter('mp4')[-1])
    #<Video: H.264 (.mp4) - 720p>

    # you can also get all videos for a given resolution
    mp4_videos = yt.filter(extension='mp4')

    if len(mp4_videos) is 0:
        webm_videos = yt.filter(extension='webm')
        if len(webm_videos) is 0:
            return json.dumps({'status': 400})
            # error message to the user, can't get the video, missing mp4 videos
        else:
            best_video = webm_videos[len(webm_videos) - 1]
    else:
        best_video = mp4_videos[len(mp4_videos) - 1]

    #[<Video: H.264 (.flv) - 480p>,
    #<Video: VP8 (.webm) - 480p>]

    # to select a video by a specific resolution and filetype you can use the get
    # method.

    video = yt.get(best_video.extension, best_video.resolution, best_video.profile)

    # NOTE: get() can only be used if and only if one object matches your criteria.
    # for example:

    #pprint(yt.videos)

    #[<Video: MPEG-4 Visual (.3gp) - 144p>,
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

    #video = yt.get('mp4')
    # MultipleObjectsReturned: get() returned more than one object -- it returned 2!

    # In this case, we'll need to specify both the codec (mp4) and resolution
    # (either 360p or 720p).

    # Okay, let's download it!
    #try:
    video.download(os.path.join(BASE_DIR, 'src/videos/'))
    #except Exception:
    #    return json.dumps({'status': 400})
    # Downloading: Pulp Fiction - Dancing Scene.mp4 Bytes: 37561829
    # 37561829  [100.00%]

    # Note: If you wanted to choose the output directory, simply pass it as an
    # argument to the download method.
    # video.download('/tmp/')

    db = sql.connect(os.path.join(BASE_DIR, 'db/raspi-tv.sqlite'), check_same_thread=False)
    db.execute("INSERT INTO YouTube VALUES (?,?,?);",
               (link, os.path.join(BASE_DIR, 'src/videos/' + yt.filename + '.mp4'), yt.filename))
    db.commit()
    db.close()


def delete_video(name):
    # in case of mp4
    files = glob.glob(os.path.join(BASE_DIR, 'src/videos/' + name + '.mp4'))
    for f in files:
        os.remove(f)

    # in case of webm
    files = glob.glob(os.path.join(BASE_DIR, 'src/videos/' + name + '.webm'))
    for f in files:
        os.remove(f)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        download(sys.argv[1])