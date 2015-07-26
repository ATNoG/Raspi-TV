import dropbox
import os
import sys
import time


def list_files(access_token, path):
    client = dropbox.client.DropboxClient(access_token)

    folder_files = client.metadata(path)['contents']
    return folder_files


def save_file(access_token, path, f):
    out = open('dropbox_files/' + access_token + '/' + path, 'wb')
    out.write(f.read())
    out.close()


def download_file(access_token, path):
    client = dropbox.client.DropboxClient(access_token)

    f, metadata = client.get_file_and_metadata(path)
    last_mod_date = metadata['modified'][0:3] + metadata['modified'][7:11] + metadata['modified'][4:7] \
                    + metadata['modified'][16:25] + metadata['modified'][11:16]
    # Check if it was changed
    if os.path.isfile('dropbox_files/' + access_token + '/' + path):
        saved_f = open('dropbox_files/' + access_token + '/' + path, os.O_RDWR|os.O_CREAT)
        info = os.fstat(saved_f)
        if not time.asctime(time.localtime(info.st_mtime)) == last_mod_date:
            save_file(access_token, path, f)
    else:
        save_file(access_token, path, f)


def download_folder(access_token, path):
    os.mkdir('dropbox_files/' + access_token + '/' + path)
    copy_folder(access_token, path)


def copy_folder(access_token, path):
    for f in list_files(access_token, path):
        if f['is_dir']:
            download_folder(access_token, f['path'])
        else:
            download_file(access_token, f['path'])


def copy_dropbox_folder(access_token):
    copy_folder(access_token, '/')
