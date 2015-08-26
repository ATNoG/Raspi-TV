# coding=utf-8
import datetime
import sqlite3 as sql
import json
import dropbox_conn
import cherrypy
from auth import require, SESSION_KEY
from Crypto.Hash import SHA256
from requests_oauthlib import OAuth1Session

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
        # Twitter #
        self.REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
        self.ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
        self.AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
        self.SIGNIN_URL = 'https://api.twitter.com/oauth/authenticate'
        self.resp = None

    @cherrypy.expose
    def dropbox(self, account, token, note):
        date = datetime.datetime.now().strftime('%I:%M%p on %B %d, %Y')
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
    def twitter(self, clear=0, pincode=None, note=None):
        date = datetime.datetime.now().strftime('%I:%M%p on %B %d, %Y')

        if clear:
            self.resp = None
            return 'Successful'

        (consumer_key, consumer_secret) = conn.execute('SELECT ConsumerKey, ConsumerSecret FROM Twitter').fetchone()
        oauth_client = OAuth1Session(consumer_key, client_secret=consumer_secret)

        if not self.resp:  # Else a temp token was already generated
            # Requesting a temp token from Twitter
            try:
                self.resp = oauth_client.fetch_request_token(self.REQUEST_TOKEN_URL)
            except ValueError, e:
                raise cherrypy.HTTPRedirect(
                    '/admin/accounts.html#error=Invalid response from Twitter requesting temp token: %s' % e)

        if not pincode:  # Else pin code is already known
            # URL to the pin code page (used to obtain an Authentication Token)

            return oauth_client.authorization_url(self.AUTHORIZATION_URL)

        # Generating and signing request for an access token

        oauth_client = OAuth1Session(consumer_key, client_secret=consumer_secret,
                                     resource_owner_key=self.resp.get('oauth_token'),
                                     resource_owner_secret=self.resp.get('oauth_token_secret'),
                                     verifier=pincode)
        try:
            resp = oauth_client.fetch_access_token(self.ACCESS_TOKEN_URL)
            conn.execute('UPDATE Twitter SET AccessKey=?, AccessSecret=?, Note=?, DateAdded=? WHERE ConsumerKey=?',
                         (resp.get('oauth_token'), resp.get('oauth_token_secret'), note, date, consumer_key))
            conn.commit()
        except ValueError, e:
            raise cherrypy.HTTPRedirect(
                '/admin/accounts.html#error=Invalid respond from Twitter requesting access token: %s' % e)

        return 'Successful'


@require()
class Get:
    def __init__(self):
        pass

    @cherrypy.expose
    def dropbox(self):
        return self.get('dropbox')

    @cherrypy.expose
    def twitter(self):
        twitter = conn.execute('SELECT AccessKey, AccessSecret, Note, DateAdded FROM Twitter').fetchone()
        return json.dumps({'AccessKey': 'X' * len(twitter[0][:-4]) + twitter[0][-4:],
                           'AccessSecret': 'X' * len(twitter[1][:-4]) + twitter[1][-4:], 'Note': twitter[2],
                           'DateAdded': twitter[3]}, separators=(',', ':'))

    def get(self, service):
        rtn = []
        accounts = conn.execute('SELECT * FROM Accounts WHERE Service=?', (service,))
        # Nao falta aqui um fetchall(), Ricardo?
        # Repara no ciclo for a baixo. Itera-se por todos os resultados
        # Nao sei se itera, ja testei isso uma vez e deu mal...
        # Quando criava as contas da forma antiga (e errada) experimentei assim. Lembro-me do que falas mas faziamos .fetchone()
        for account in accounts:
            rtn.append({'account': account[0], 'token': 'X' * len(account[1][:-4]) + account[1][-4:],
                        'date': account[2], 'note': account[3]})
        return json.dumps(rtn, separators=(',', ':'))

    def dropbox_files(self):
        all_files = []
        for f in conn.execute('SELECT * FROM Files ORDER BY FileOrder DESC').fetchall():  # se puderes experimenta retirar o .fetchall()
            # Revê o código que tinhas antes. Acho que o que querias era isto
            all_files.append({'accountid': f[3], 'filepath': f[0], 'todisplay': f[1], 'order': f[2]})

        return json.dumps(all_files, separators=(',', ':'))

    def tweets(self):
        all_tweets = []
        for tweet in conn.execute('SELECT * FROM Tweets ORDER BY TweetOrder DESC').fetchall():  # Idem caso acima resulte
            # Por favor revê também esta parte. Mais uma vez suponho que querias isto
            all_tweets.append({'tweetid': tweet[0], 'author': tweet[1],
                               'tweet': tweet[2], 'todisplay': tweet[3], 'order': tweet[4]})

        return json.dumps(all_tweets, separators=(',', ':'))


@require()
class Update:
    def __init__(self):
        pass

    @cherrypy.expose
    def user(self, current_password=None, new_password=None, first_name=None, last_name=None, email=None):
        username = cherrypy.session[SESSION_KEY]
        date = datetime.datetime.now().strftime('%B %d, %Y')
        if current_password and new_password:
            current_password = self.encrypt_password(current_password)
            if current_password == conn.execute('SELECT Password FROM Users WHERE UserId=?', (username,)).fetchone()[0]:
                conn.execute('UPDATE Users SET Password=?, Date=? WHERE UserId=?',
                             (self.encrypt_password(new_password), date, username))
                conn.commit()
                raise cherrypy.HTTPRedirect('/admin/profile.html')
            else:
                raise cherrypy.HTTPRedirect('/admin/profile.html#error=Wrong password')
        if first_name:
            conn.execute('UPDATE Users SET FirstName=?, Date=? WHERE UserId=?', (first_name, date, username))
            conn.commit()
            raise cherrypy.HTTPRedirect('/admin/profile.html')
        if last_name:
            conn.execute('UPDATE Users SET LastName=?, Date=? WHERE UserId=?', (last_name, date, username))
            conn.commit()
            raise cherrypy.HTTPRedirect('/admin/profile.html')
        if email:
            conn.execute('UPDATE Users SET Email=?, Date=? WHERE UserId=?', (email, date, username))
            conn.commit()
            raise cherrypy.HTTPRedirect('/admin/profile.html')
        raise cherrypy.HTTPRedirect('/admin/profile.html#error=No parameters received')

    @staticmethod
    def encrypt_password(password):
        return SHA256.new(password).hexdigest()

    @cherrypy.expose
    def dropbox_files(self, files):
        outdated_files = self.get.dropbox_files()
        i = 0
        while True:
            if not files[i] or not outdated_files[i]:
                break
            if not files[i]['todisplay'] == outdated_files[i]['todisplay']:
                try:
                    conn.execute('UPDATE Files SET ToDisplay = ? WHERE FilePath = ?',
                                 (files[i]['todisplay'], files[i]['filepath']))
                    conn.commit()
                except sql.Error:
                    return 'Unsuccessful.'
            if not files[i]['order'] == outdated_files[i]['order']:
                try:
                    conn.execute('UPDATE Files SET FileOrder = ? WHERE FilePath = ?',
                                 (files[i]['order'], files[i]['filepath']))
                    conn.commit()
                except sql.Error:
                    return 'Unsuccessful.'
            i += 1

        return 'Successful.'

    @cherrypy.expose
    def tweets(self, tweetlist):
        outdated_tweets = self.get.tweets()
        i = 0
        while True:
            if not tweetlist[i] or not outdated_tweets[i]:
                break
            if not tweetlist[i]['todisplay'] == outdated_tweets[i]['todisplay']:
                try:
                    conn.execute('UPDATE Tweets SET ToDisplay = ? WHERE TweetId = ?',
                                 (tweetlist[i]['todisplay'], tweetlist[i]['tweetid']))
                    conn.commit()
                except sql.Error:
                    return 'Unsuccessful.'
            if not tweetlist[i]['order'] == outdated_tweets[i]['order']:
                try:
                    conn.execute('UPDATE Tweets SET TweetOrder = ? WHERE TweetId = ?',
                                 (tweetlist[i]['order'], tweetlist[i]['tweetid']))
                    conn.commit()
                except sql.Error:
                    return 'Unsuccessful.'
            i += 1

        return 'Successful.'

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def updateDB(self, location=None, locationDescription=None, background=None, weather=None):
        if location:
            conn.execute('UPDATE HTMLSettings SET content=? WHERE idName=? ', (location, 'location',))
        if locationDescription:
            conn.execute('UPDATE HTMLSettings SET content=? WHERE idName=? ', (locationDescription, 'locationDescription',))
        if background:
            conn.execute('UPDATE HTMLSettings SET content=? WHERE idName=? ', (background, 'background',))
        if weather:
            conn.execute('UPDATE HTMLSettings SET content=? WHERE idName=? ', (weather, 'weather',))
        conn.commit()