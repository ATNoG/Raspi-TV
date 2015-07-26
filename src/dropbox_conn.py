import dropbox
import os


def list_files(access_token, path):
    client = dropbox.client.DropboxClient(access_token)

    folder_files = client.metadata(path)['contents']
    return folder_files


def download_file(access_token, path):
    client = dropbox.client.DropboxClient(access_token)

    f, metadata = client.get_file_and_metadata(path)
    out = open('dropbox_files/' + access_token + '/' + path, 'wb')
    out.write(f.read())
    out.close()


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
