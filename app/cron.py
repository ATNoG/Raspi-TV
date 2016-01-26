from twitter_conn import populate_db
from dropbox_conn import copy_dropbox_folder

if __name__ == '__main__':
    try:
        populate_db()
    except Exception:
        print "\nTwitter account not added."

    try:
        copy_dropbox_folder()
    except Exception:
        print "\nDropbox account not added."