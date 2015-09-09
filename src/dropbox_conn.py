import dropbox
import os
import sys
import time
import sqlite3 as sql

conn = sql.connect('../db/raspi-tv.sqlite', check_same_thread=False)
access_token = conn.execute('SELECT AuthToken FROM Dropbox').fetchone()[0]
client = dropbox.client.DropboxClient(access_token)


def list_files(path):
    folder_files = client.metadata(path)['contents']
    return folder_files


def save_file(path, f):
    out = open('dropbox_files/' + access_token + '/' + path, 'wb')
    out.write(f.read())
    out.close()
    account_id = conn.execute('SELECT AccountId FROM Dropbox WHERE AuthToken=?', (access_token,)).fetchone()[0]
    conn.execute('INSERT OR REPLACE INTO Files (FilePath, ToDisplay, FileOrder, AccountId) VALUES '
                 '(?, COALESCE((SELECT ToDisplay FROM Files WHERE FilePath=?), 0),'
                 'COALESCE((SELECT FileOrder FROM Files WHERE FilePath=?), 0), ?)',
                 (path, '0', '-1', account_id,))
    conn.commit()


def download_file(path):
    f, metadata = client.get_file_and_metadata(path)
    last_mod_date = metadata['modified'][0:3] + metadata['modified'][7:11] + metadata['modified'][4:7] \
                    + metadata['modified'][16:25] + metadata['modified'][11:16]
    # Check if it was changed
    if os.path.isfile('dropbox_files/' + access_token + '/' + path):
        saved_f = open('dropbox_files/' + access_token + '/' + path, os.O_RDWR|os.O_CREAT)
        info = os.fstat(saved_f)
        if not time.asctime(time.localtime(info.st_mtime)) == last_mod_date:
            save_file(path, f)
    else:
        save_file(path, f)


def download_folder(path):
    os.mkdir('dropbox_files/' + access_token + '/' + path)
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
