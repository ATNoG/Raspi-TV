# encoding: utf-8
import datetime
import json

import netifaces
import cherrypy
import requests
from constants import conn
from ua_news import deti_news


class Api:
    def __init__(self):
        self.get = Get()


class Get:
    def __init__(self):
        pass

    @cherrypy.expose
    def all_info(self):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        array_info = []
        services_order = self.front_order()
        for service in services_order:
            print service['name']
            if service['name'] == 'News':
                array_info.append({'name': 'News', 'content': deti_news()})
            elif service['name'] == 'Youtube':
                array_info.append({'name': 'Youtube', 'content': self.youtube()})
            elif service['name'] == 'Dropbox Photos':
                array_info.append({'name': 'Dropbox Photos', 'content': self.dropbox_files('image')})
            else:
                array_info.append({'name': 'Dropbox Videos', 'content': self.dropbox_files('video')})

        return json.dumps(array_info)

    @staticmethod
    def front_order():
        all_services = []
        for service in conn.execute('SELECT * FROM FrontEndOrder WHERE ToDisplay=? ORDER BY ServicesOrder ASC',
                                    ('1',)).fetchall():
            all_services.append({'name': service[0], 'order': service[2]})

        return all_services

    @staticmethod
    def youtube():
        all_videos = []
        for video in conn.execute('SELECT * FROM YouTube').fetchall():
            all_videos.append({'link': video[0], 'filepath': video[1].split("/static")[1], 'name': video[2]})

        return all_videos

    @staticmethod
    def dropbox_files(file_type):
        all_files = []
        for f in conn.execute('SELECT * FROM Files WHERE Type=? AND ToDisplay=? ORDER BY FileOrder ASC',
                              (file_type, '1',)).fetchall():
            all_files.append({'filepath': f[0], 'todisplay': f[1], 'order': f[2], 'type': f[3]})

        return all_files

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['GET'])
    def cantina_menus(self):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        menus = json.loads(requests.get('http://services.web.ua.pt/sas/ementas?format=json').content)
        parsed_menus = []
        now = datetime.datetime.now()

        for menu in menus['menus']['menu']:
            if menu['@attributes']['disabled'] == '0' and not menu['@attributes']['canteen'] == u'Snack-Bar/Self':
                info = {'info': {'canteen': menu['@attributes']['canteen'], 'extrainfo': menu['@attributes']['meal']},
                        'meal': menu['items']['item']}

                if (now.hour < 15 and menu['@attributes']['meal'] == u'Almoço') \
                        or (now.hour >= 15 and menu['@attributes']['meal'] == u'Jantar'):
                    parsed_menus.append(info)

        return json.dumps(parsed_menus)

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['GET'])
    def HTMLChanges(self):
        cherrypy.response.headers['Content-Type'] = 'text/json'
        response = []

        location = conn.execute('SELECT * FROM HTMLSettings WHERE idName=?', ('location',)).fetchone()[1]
        response.append({'id': 'location', 'type': 'text', 'content': location})

        locationDescription = conn.execute('SELECT * FROM HTMLSettings WHERE idName=?',
                                           ('locationDescription',)).fetchone()[1]
        response.append({'id': 'location_description', 'type': 'text', 'content': locationDescription})

        twitter_query = conn.execute('SELECT * FROM HTMLSettings WHERE idName=?', ('twitterQuery',)).fetchone()[1]
        response.append({'id': 'twitter_query', 'type': 'text', 'content': twitter_query})

        feed = conn.execute('SELECT * FROM HTMLSettings WHERE idName=?', ('feed',)).fetchone()[1]
        response.append({'id': 'feed', 'type': 'text', 'content': feed})

        socket_port = cherrypy.config.get('server.socket_port')

        addresses = 'No IP address'
        ifaces = ['eth0', 'wlan0']
        for iface in ifaces:
            try:
                addresses = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr'] + ':' + str(socket_port)
            except (ValueError, KeyError):
                continue
            break
        response.append({'id': 'ip', 'type': 'text', 'content': addresses})
        return json.dumps(response)

    @cherrypy.expose
    def tweets(self):
        all_tweets = []

        for tweet in conn.execute('SELECT * FROM Tweets ORDER BY TweetOrder ASC').fetchall():
            if tweet[3] == 0:
                all_tweets.append({'tweetid': tweet[0], 'author': tweet[1],
                                   'tweet': tweet[2], 'order': tweet[4]})

        for tweet in conn.execute('SELECT * FROM Tweets WHERE TweetOrder=? ORDER BY TweetOrder DESC',
                                  ('1',)).fetchall():
            all_tweets.append({'tweetid': tweet[0], 'author': tweet[1], 'tweet': tweet[2], 'order': tweet[4]})

        return json.dumps(all_tweets, separators=(',', ':'))

    # @cherrypy.expose
    # def weather(self):
    #     return json.dumps({'content': get_w()})

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['GET'])
    def list_of_links(self):
        ids = conn.execute('SELECT * FROM YouTube;')
        ids = ids.fetchall()
        list_to_return = []
        for i in ids:
            list_to_return.append(i[0])
        return json.dumps({'status': 200, 'content': list_to_return})
