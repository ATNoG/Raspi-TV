import datetime
import sqlite3 as sql

import cherrypy
from auth import SESSION_USER, SESSION_LOGIN
from constants import conn
from dropbox.client import *
from requests_oauthlib import OAuth1Session


class Admin:
    def __init__(self):
        self.create = Create()
        self.get = Get()
        self.update = Update()

    @cherrypy.expose
    def user(self):
        if cherrypy.session[SESSION_LOGIN]:
            return json.dumps(cherrypy.session[SESSION_USER], separators=(',', ':'))

    @cherrypy.expose
    def reload(self):
        os.system('xte "key F5" -x:0')
        raise cherrypy.HTTPRedirect(cherrypy.request.headers.get('Referer'))


class Create:
    def __init__(self):
        # Twitter #
        self.REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
        self.ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
        self.AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
        self.SIGNIN_URL = 'https://api.twitter.com/oauth/authenticate'
        self.resp = None

    @cherrypy.expose
    def dropbox(self, auth=0, pincode=None, note=None):
        date = datetime.datetime.now().strftime('%I:%M%p on %B %d, %Y')

        (app_key, app_secret) = conn.execute('SELECT AppKey, AppSecret FROM Dropbox').fetchone()

        auth_flow = DropboxOAuth2FlowNoRedirect(app_key, app_secret)

        if not auth:
            return auth_flow.start()

        if pincode:
            try:
                access_token, user_id = auth_flow.finish(pincode)
            except ErrorResponse, e:
                print('Error: %s' % (e,))
                return 'Unsuccessful.'

            print access_token
            if conn.execute('SELECT COUNT(*) FROM Dropbox WHERE AuthToken=?', (access_token,)).fetchone()[0]:
                rtn = 'Unsuccessful. Account already exists.'
            else:
                conn.execute('UPDATE Dropbox SET AuthToken=?, Note=?, DateAdded=? WHERE AppKey=?',
                             (access_token, note, date, app_key))
                conn.commit()
                rtn = 'Successful.'
            return rtn
        else:
            return 'Error reading parameters'

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
                        '/admin/pages/accounts.html#error=Invalid response from Twitter requesting temp token: %s' % e)

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
                    '/admin/pages/accounts.html#error=Invalid respond from Twitter requesting access token: %s' % e)

        return 'Successful'


class Get:
    def __init__(self):
        pass

    @cherrypy.expose
    def dropbox(self):
        cherrypy.response.headers['Content-Type'] = "application/json"
        dropbox = conn.execute('SELECT AuthToken, Note, DateAdded FROM Dropbox').fetchone()
        try:
            return json.dumps({'AuthToken': 'X' * len(dropbox[0][:-4]) + dropbox[0][-4:], 'Note': dropbox[1],
                               'DateAdded': dropbox[2]}, separators=(',', ':'))
        except TypeError:
            return 'No account added.'

    @cherrypy.expose
    def twitter(self):
        cherrypy.response.headers['Content-Type'] = "application/json"
        twitter = conn.execute('SELECT AccessKey, AccessSecret, Note, DateAdded FROM Twitter').fetchone()
        try:
            return json.dumps({'AccessKey': 'X' * len(twitter[0][:-4]) + twitter[0][-4:],
                               'AccessSecret': 'X' * len(twitter[1][:-4]) + twitter[1][-4:], 'Note': twitter[2],
                               'DateAdded': twitter[3]}, separators=(',', ':'))
        except TypeError:
            return 'No account added.'

    @cherrypy.expose
    def dropbox_files(self, file_type):
        cherrypy.response.headers['Content-Type'] = "application/json"
        all_files = []
        for f in conn.execute('SELECT * FROM Files WHERE Type=? ORDER BY FileOrder ASC', (file_type,)).fetchall():
            all_files.append({'filepath': f[0], 'todisplay': f[1], 'order': f[2], 'type': f[3]})

        return json.dumps(all_files, separators=(',', ':'))

    @cherrypy.expose
    def tweets(self):
        cherrypy.response.headers['Content-Type'] = "application/json"
        all_tweets = []
        for tweet in conn.execute('SELECT * FROM Tweets ORDER BY TweetOrder ASC'):
            all_tweets.append({'tweetid': str(tweet[0]), 'author': tweet[1], 'tweet': tweet[2], 'todisplay': tweet[3],
                               'order': tweet[4]})

        return json.dumps(all_tweets, separators=(',', ':'))

    @cherrypy.expose
    def services(self):
        cherrypy.response.headers['Content-Type'] = "application/json"
        all_services = []
        for service in conn.execute('SELECT * FROM FrontEndOrder ORDER BY ServicesOrder ASC').fetchall():
            all_services.append({'name': service[0], 'todisplay': service[1], 'order': service[2]})

        return json.dumps(all_services, separators=(',', ':'))


class Update:
    def __init__(self):
        pass

    @cherrypy.expose
    def user(self, current_password=None, new_password=None, first_name=None, last_name=None, email=None):
        if not ((current_password and new_password) or first_name or last_name or email):
            raise cherrypy.HTTPRedirect('/admin/pages/profile.html#error=No parameters received')
        username = cherrypy.session[SESSION_USER]['UserId']
        date = datetime.datetime.now().strftime('%B %d, %Y')
        if current_password and new_password:
            if current_password == conn.execute('SELECT Password FROM Users WHERE UserId=?', (username,)).fetchone()[0]:
                conn.execute('UPDATE Users SET Password=?, Date=? WHERE UserId=?',
                             (new_password, date, username))
            else:
                raise cherrypy.HTTPRedirect('/admin/pages/profile.html#error=Wrong password')
        if first_name:
            conn.execute('UPDATE Users SET FirstName=?, Date=? WHERE UserId=?', (first_name, date, username))
            cherrypy.session[SESSION_USER]['FirstName'] = first_name
        if last_name:
            conn.execute('UPDATE Users SET LastName=?, Date=? WHERE UserId=?', (last_name, date, username))
            cherrypy.session[SESSION_USER]['LastName'] = last_name
        if email:
            conn.execute('UPDATE Users SET Email=?, Date=? WHERE UserId=?', (email, date, username))
            cherrypy.session[SESSION_USER]['Email'] = email
        conn.commit()
        raise cherrypy.HTTPRedirect('/admin/pages/profile.html')

    @staticmethod
    def dropbox_db(files):
        try:
            for f in json.loads(files):
                conn.execute('UPDATE Files SET ToDisplay=?, FileOrder=? WHERE FilePath=?',
                             (f['todisplay'], f['order'], f['filepath'],))
            conn.commit()
            return 'Successful.'
        except sql.Error:
                return 'Unsuccessful.'


    @cherrypy.expose
    def dropbox_files(self, images, videos):
        if self.dropbox_db(images) == 'Successful.' and self.dropbox_db(videos) == 'Successful.':
            return 'Successful.'
        else:
            return 'Unsuccessful.'

    @cherrypy.expose
    def tweets(self, tweetlist):
        try:
            for tweet in json.loads(tweetlist):
                conn.execute('UPDATE Tweets SET ToDisplay=?, TweetOrder=? WHERE TweetId=?',
                             (tweet['todisplay'], tweet['order'], tweet['tweetid'],))
            conn.commit()
            return 'Successful.'
        except sql.Error:
            return 'Unsuccessful.'

    @cherrypy.expose
    def services(self, servicelist):
        try:
            for service in json.loads(servicelist):
                conn.execute('UPDATE FrontEndOrder SET ToDisplay=?, ServicesOrder=? WHERE Service=?',
                             (service['todisplay'], service['order'], service['name'],))
            conn.commit()
            return 'Successful.'
        except sql.Error:
            return 'Unsuccessful.'


    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def updateDB(self, location=None, locationDescription=None, background=None, twitterQuery=None, feed=None):
        if location:
            conn.execute('UPDATE HTMLSettings SET content=? WHERE idName=? ', (location, 'location',))
        if locationDescription:
            conn.execute('UPDATE HTMLSettings SET content=? WHERE idName=? ',
                         (locationDescription, 'locationDescription',))
        if twitterQuery:
            conn.execute('UPDATE HTMLSettings SET content=? WHERE idName=? ', (twitterQuery, 'twitterQuery'))
        if feed:
            conn.execute('UPDATE HTMLSettings SET content=? WHERE idName=? ', (feed, 'feed',))
        conn.commit()
