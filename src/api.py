import cherrypy
import json
from ua_news import deti_news


class Api:

    @cherrypy.expose
    def get_deti_news(self):
        feed_news = deti_news()
        print feed_news
        news = {}
        news["title"] = feed_news["feed"]["title"]
        news["news"] = []

        for entry in feed_news["feed"]["entry"]:
            news["news"] += [{"author": entry["author"],
                              "summary": entry["summary"]["#text"],
                              "title": entry["title"],
                              "date": entry["updated"]}]


        return json.dumps({"status": 200, "content": news})