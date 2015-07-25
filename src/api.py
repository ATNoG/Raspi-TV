import cherrypy
import json
import os
from ua_news import deti_news
from weather import get_weather as get_w
from dropbox2 import login as dropbox_login, list_files


class Api:
    @cherrypy.expose
    def get_deti_news(self):
        return json.dumps({"status": 200, "content": deti_news()})

    @cherrypy.expose
    def get_weather(self):
        return json.dumps({"status": 200, "content": get_w()})


    @cherrypy.expose
    def dropbox_new_account(self, code):
        client_info = dropbox_login(code)
        # Add info to database using client info

    @cherrypy.expose
    def get_dropbox_files(self):
        pass
        # Query to database to get all accounts linked
        # all_files = []
        # for account in accounts:
        #     files = list_files(account_access_token)
        #     all_files.append('account_id': account_id, 'files': files)
        # return json.dumps({"status": 200, "content": all_files})
