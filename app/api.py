import json

import cherrypy
from ua_news import deti_news

# from weather import get_weather as get_w
from netifaces import ifaddresses, AF_INET
from constants import conn


class Api:
    def __init__(self):
        pass

    @cherrypy.expose
    def get_all_info(self):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        array_info = []
        services_order = self.get_front_order()
        for service in services_order:
            print service['name']
            if service['name'] == 'News':
                array_info.append({'name': 'News', 'content': deti_news()})
            elif service['name'] == 'Youtube':
                array_info.append({'name': 'Youtube', 'content': self.get_youtube()})
            elif service['name'] == 'Dropbox Photos':
                array_info.append({'name': 'Dropbox Photos', 'content': self.get_dropbox_files('image')})
            else:
                array_info.append({'name': 'Dropbox Videos', 'content': self.get_dropbox_files('video')})

        return json.dumps(array_info)

    @staticmethod
    def get_front_order():
        all_services = []
        for service in conn.execute('SELECT * FROM FrontEndOrder WHERE ToDisplay=? ORDER BY ServicesOrder ASC',
                                    ('1',)).fetchall():
            all_services.append({'name': service[0], 'order': service[2]})

        return all_services

    @staticmethod
    def get_youtube():
        all_videos = []
        for video in conn.execute('SELECT * FROM YouTube').fetchall():
            print video
            all_videos.append({'link': video[0], 'filepath': video[1].split("/src/static/")[1], 'name': video[2]})

        return all_videos

    # @cherrypy.expose
    # def get_weather(self):
    #     return json.dumps({'content': get_w()})

    @staticmethod
    def get_dropbox_files(file_type):
        all_files = []
        for f in conn.execute('SELECT * FROM Files WHERE Type=? AND ToDisplay=? ORDER BY FileOrder ASC',
                              (file_type, '1',)).fetchall():
            all_files.append({'filepath': f[0], 'todisplay': f[1], 'order': f[2], 'type': f[3]})

        return all_files

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['GET'])
    def get_HTMLChanges(self):
        cherrypy.response.headers['Content-Type'] = 'text/json'
        response = []

        # background = conn.execute('SELECT * FROM HTMLSettings WHERE idName=?', ('background',)).fetchone()[1]
        # response.append({'id': 'background', 'type': 'image', 'content': background})

        location = conn.execute('SELECT * FROM HTMLSettings WHERE idName=?', ('location',)).fetchone()[1]
        response.append({'id': 'location', 'type': 'text', 'content': location})

        locationDescription = conn.execute('SELECT * FROM HTMLSettings WHERE idName=?',
                                           ('locationDescription',)).fetchone()[1]
        response.append({'id': 'location_description', 'type': 'text', 'content': locationDescription})

        weather = conn.execute('SELECT * FROM HTMLSettings WHERE idName=?', ('weather',)).fetchone()[1]
        response.append({'id': 'weatherR', 'type': 'text', 'content': weather})

        feed = conn.execute('SELECT * FROM HTMLSettings WHERE idName=?', ('feed',)).fetchone()[1]
        response.append({'id': 'feed', 'type': 'text', 'content': feed})

        addresses = [i['addr'] + ':8080' for i in ifaddresses('eth0').setdefault(AF_INET, [{'addr': 'No IP address'}])]
        response.append({'id': 'ip', 'type': 'text', 'content': addresses[0]})

        return json.dumps(response)

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['GET'])
    def list_of_links(self):
        ids = conn.execute('SELECT * FROM YouTube;')
        ids = ids.fetchall()
        list_to_return = []
        for i in ids:
            list_to_return.append(i[0])
        return json.dumps({'status': 200, 'content': list_to_return})

    @cherrypy.expose
    def get_tweets(self):
        all_tweets = []

        for tweet in conn.execute('SELECT * FROM Tweets ORDER BY TweetOrder ASC').fetchall():
            if tweet[3] == 0:
                all_tweets.append({'tweetid': tweet[0], 'author': tweet[1],
                                   'tweet': tweet[2], 'order': tweet[4]})

        for tweet in conn.execute('SELECT * FROM Tweets WHERE TweetOrder=? ORDER BY TweetOrder DESC',
                                  ('1',)).fetchall():
            all_tweets.append({'tweetid': tweet[0], 'author': tweet[1], 'tweet': tweet[2], 'order': tweet[4]})

        return json.dumps(all_tweets, separators=(',', ':'))
