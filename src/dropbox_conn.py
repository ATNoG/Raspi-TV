import dropbox
import os
import sys
import time
import sqlite3 as sql
from settings import *

conn = sql.connect(os.path.join(BASE_DIR, 'db/raspi-tv.sqlite'), check_same_thread=False)
try:
    access_token = conn.execute('SELECT AuthToken FROM Dropbox').fetchone()[0]
    client = dropbox.client.DropboxClient(access_token)
except ValueError:
    print 'No account added'
    sys.exit()


def list_files(path):
    folder_files = client.metadata(path)['contents']
    return folder_files


def save_file(path, f):
    out = open(os.path.join(BASE_DIR, 'src/static/dropbox_files', path[1:]), 'w')
    out.write(f.read())
    out.close()
    conn.execute('INSERT OR REPLACE INTO Files (FilePath, ToDisplay, FileOrder) VALUES '
                 '(?, COALESCE((SELECT ToDisplay FROM Files WHERE FilePath=?), 0),'
                 'COALESCE((SELECT FileOrder FROM Files WHERE FilePath=?), 0))', (path, '0', '-1',))
    conn.commit()
    print 'SUCCESS: ' + path + ' was saved.'


def download_file(path):
    f, metadata = client.get_file_and_metadata(path)
    last_mod_date = metadata['modified'][0:3] + metadata['modified'][7:11] + metadata['modified'][4:7] \
                    + metadata['modified'][16:25] + metadata['modified'][11:16]
    file_type = metadata['mime_type'].split('/')[0]

    # Check if it an image/video
    if file_type == 'image' or file_type == 'video':
        # Check if it was changed
        if os.path.isfile(os.path.join(BASE_DIR, 'src/static/dropbox_files', path[1:])):
            # saved_f = open(), os.O_RDONLY)
            info = os.stat(os.path.join(BASE_DIR, 'src/static/dropbox_files', path[1:]))
            if not time.asctime(time.localtime(info.st_mtime)) == last_mod_date:
                save_file(path, f)
        else:
            save_file(path, f)
    else:
        print 'WARNING: The file with the path: ' + path + ' is neither a image or a video. NOT copied.'


def download_folder(path):
    if not os.path.isdir(os.path.join(BASE_DIR, 'src/static/dropbox_files', path[1:])):
        os.mkdir(os.path.join(BASE_DIR, 'src/static/dropbox_files', path[1:]))
    copy_folder(path)


def copy_folder(path):
    for f in list_files(path):
        if f['is_dir']:
            download_folder(f['path'])
        else:
            download_file(f['path'])


def copy_dropbox_folder():
    copy_folder('/')


if __name__ == '__main__':
    copy_dropbox_folder()
