import time

import dropbox
import os
from constants import ROOT_DIR, conn

try:
    access_token = conn.execute('SELECT AuthToken FROM Dropbox').fetchone()[0]
    client = dropbox.client.DropboxClient(access_token)
except ValueError:
    print 'No account added'
    client = None

updated_files = []


def copy_dropbox_folder():
    if client:
        copy_folder('/')
        for f in conn.execute('SELECT * FROM Files').fetchall():
            if f[0] not in updated_files:
                conn.execute('DELETE FROM Files WHERE FilePath=?', (f[0],))
                conn.commit()
                os.remove(os.path.join(ROOT_DIR, 'static/public/data/dropbox_files', f[0][1:]))
                print 'WARNING: The file with the path: ' + f[0] + ' was removed.'


def copy_folder(path):
    for f in list_files(path):
        if f['is_dir']:
            download_folder(f['path'])
        else:
            download_file(f['path'])


def download_folder(path):
    if not os.path.isdir(os.path.join(ROOT_DIR, 'static/public/data/dropbox_files', path[1:])):
        os.mkdir(os.path.join(ROOT_DIR, 'static/public/data/dropbox_files', path[1:]))
    copy_folder(path)


def list_files(path):
    folder_files = client.metadata(path)['contents']
    return folder_files


def download_file(path):
    f, metadata = client.get_file_and_metadata(path)
    last_mod_date = metadata['modified'][0:3] + metadata['modified'][7:11] + metadata['modified'][4:7] \
                    + metadata['modified'][16:25] + metadata['modified'][11:16]
    file_type = metadata['mime_type'].split('/')[0]

    # Check if it an image/video
    if file_type == 'image' or file_type == 'video':
        # Check if it was changed
        if os.path.isfile(os.path.join(ROOT_DIR, 'static/public/data/dropbox_files', path[1:])):
            info = os.stat(os.path.join(ROOT_DIR, 'static/public/data/dropbox_files', path[1:]))
            if not time.asctime(time.localtime(info.st_mtime)) == last_mod_date:
                save_file(path, f, file_type, 'updated')
        else:
            save_file(path, f, file_type, 'saved')
    else:
        print 'WARNING: The file with the path: ' + path + ' is neither an image or a video. NOT copied.'


def save_file(path, f, file_type, message):
    out = open(os.path.join(ROOT_DIR, 'static/public/data/dropbox_files', path[1:]), 'w')
    out.write(f.read())
    out.close()
    conn.execute('INSERT OR REPLACE INTO Files (FilePath, ToDisplay, FileOrder, Type) VALUES '
                 '(?, COALESCE((SELECT ToDisplay FROM Files WHERE FilePath=?), 0),'
                 'COALESCE((SELECT FileOrder FROM Files WHERE FilePath=?), 0), ?)',
                 (os.path.join(ROOT_DIR, 'static/public/data/dropbox_files', path), '1', -1, file_type))
    conn.commit()
    updated_files.append(path)
    print 'SUCCESS: ' + path + ' was ' + message + '.'
