import datetime
import sqlite3 as sql
import json
import dropbox_conn
import cherrypy
from auth import require, SESSION_KEY
from Crypto.Hash import SHA256

conn = sql.connect('../db/raspi-tv.sqlite', check_same_thread=False)


class Admin:
    def __init__(self):
        self.create = Create()
        self.get = Get()
        self.update = Update()

    @cherrypy.expose
    def user(self):
        try:
            user_dict = {'user_id': cherrypy.session[SESSION_KEY]}
            user = conn.execute('SELECT * FROM Users WHERE UserId=?', (user_dict['user_id'],)).fetchone()[2:]
            user_dict['user_first'] = user[0]
            user_dict['user_last'] = user[1]
            user_dict['user_email'] = user[2]
            user_dict['user_date'] = user[3]
        except (KeyError, TypeError) as e:
            user_dict = {'user_id': None}
        return json.dumps(user_dict, separators=(',', ':'))


@require()
class Create:
    def __init__(self):
        pass

    @cherrypy.expose
    def dropbox(self, account, token, note):
        date = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        service = 'dropbox'
        if conn.execute('SELECT COUNT(*) FROM Accounts WHERE AccountId=? AND Service=?', (account, service)).fetchone()[
            0]:
            rtn = 'Unsuccessful. Account already exists.'
        else:
            conn.execute('INSERT INTO Accounts VALUES (?, ?, ?, ?, ?)', (account, token, date, note, service))
            conn.commit()
            dropbox_conn.copy_dropbox_folder(token)
            rtn = 'Successful.'
        return rtn

    @cherrypy.expose
    def twitter(self, account, token, note):
        date = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        service = 'twitter'
        rtn = ''
        if conn.execute('SELECT COUNT(*) FROM Accounts WHERE AccountId=? AND Service=?', (account, service)).fetchone()[
            0]:
            rtn = 'Unsuccessful. Account already exists.'
        else:
            if conn.execute('SELECT COUNT(*) FROM Accounts WHERE Service=?', (service,)).fetchone()[0]:
                rtn = 'Warning: Only the first Twitter account of the database will be used for authentication.\n'
            conn.execute('INSERT INTO Accounts VALUES (?, ?, ?, ?, ?)', (account, token, date, note, service))
            conn.commit()
            rtn += 'Successful.'
        return rtn


@require()
class Get:
    def __init__(self):
        pass

    @cherrypy.expose
    def dropbox(self):
        return self.get('dropbox')

    @cherrypy.expose
    def twitter(self):
        return self.get('twitter')

    def get(self, service):
        rtn = []
        accounts = conn.execute('SELECT * FROM Accounts WHERE Service=?',
                                (service,))  # Nao falta aqui um fetchall(), Ricardo?
        # Repara no ciclo for a baixo. Itera-se por todos os resultados
        # Nao sei se itera, ja testei isso uma vez e deu mal...
        for account in accounts:
            rtn.append({'account': account[0], 'token': 'X' * len(account[1][:-4]) + account[1][-4:],
                        'date': account[2], 'note': account[3]})
        return json.dumps(rtn, separators=(',', ':'))

    def dropbox_files(self):
        all_files = []
        for f in conn.execute('SELECT * FROM Files').fetchall():
            all_files.append({'accountid': f['AccountId'], 'filepath': f['FilePath'], 'todisplay': f['ToDisplay']})

        return json.dumps(all_files, separators=(',', ':'))

    def tweets(self):
        all_tweets = []
        for tweet in conn.execute('SELECT * FROM Tweets').fetchall():
            all_tweets.append({'tweetid': tweet['TweetId'], 'author': tweet['Author'],
                               'tweet': tweet['Tweet'], 'todisplay': tweet['ToDisplay']})

        return json.dumps(all_tweets, separators=(',', ':'))


@require()
class Update:
    def __init__(self):
        pass

    @cherrypy.expose
    def user(self, current_password=None, new_password=None, first_name=None, last_name=None, email=None):
        username = cherrypy.session[SESSION_KEY]
        date = datetime.datetime.now().strftime("%B %d, %Y")
        if current_password and new_password:
            current_password = self.encrypt_password(current_password)
            if current_password == conn.execute('SELECT Password FROM Users WHERE UserId=?', (username,)).fetchone()[0]:
                conn.execute('UPDATE Users SET Password=?, Date=? WHERE UserId=?',
                             (self.encrypt_password(new_password), date, username))
                conn.commit()
                raise cherrypy.HTTPRedirect("/admin/profile.html")
            else:
                raise cherrypy.HTTPRedirect("/admin/profile.html#error=Wrong password")
        if first_name:
            conn.execute('UPDATE Users SET FirstName=?, Date=? WHERE UserId=?', (first_name, date, username))
            conn.commit()
            raise cherrypy.HTTPRedirect("/admin/profile.html")
        if last_name:
            conn.execute('UPDATE Users SET LastName=?, Date=? WHERE UserId=?', (last_name, date, username))
            conn.commit()
            raise cherrypy.HTTPRedirect("/admin/profile.html")
        if email:
            conn.execute('UPDATE Users SET Email=?, Date=? WHERE UserId=?', (email, date, username))
            conn.commit()
            raise cherrypy.HTTPRedirect("/admin/profile.html")
        raise cherrypy.HTTPRedirect("/admin/profile.html#error=No parameters received")

    @staticmethod
    def encrypt_password(password):
        return SHA256.new(password).hexdigest()

    # def dropbox_files(self, files):
    #     outdated_files = self.get.dropbox_files()['']
    #     i = 0
    #     while True:
    #         if not files[i] or not outdated_files[i]:
    #             break
    #         if not files[i]['todisplay'] == outdated_files[i]['']
