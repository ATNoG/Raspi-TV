from twitter_conn import populate_db
from dropbox_conn import copy_dropbox_folder

if __name__ == '__main__':
    populate_db()
    copy_dropbox_folder()
