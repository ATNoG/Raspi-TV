import feedparser
import urllib
import sqlite3 as sql
import requests
import re
import wget


def deti_news():

    try:
        response = requests.get("https://www.google.pt")
        feed_content = feedparser.parse('http://services.web.ua.pt/deti/news/')

        news = {"title": feed_content.feed.title, "news": []}

        db = sql.connect('../db/raspi-tv.sqlite')
        db.execute("DELETE FROM News;")

        for entry in feed_content.entries:
            news["news"] += [{"author": parse_author(entry.author),
                            "summary": entry.summary,
                            "title": entry.title,
                            "date": parse_date(str(entry.updated))}]

        for i in range(0, len(news["news"])):
            db.execute("INSERT INTO News VALUES (?,?,?,?);",
                    (news["news"][i]["title"], news["news"][i]["date"], news["news"][i]["author"], news["news"][i]["summary"]))
            db.commit()

        for i in range(0, len(news["news"])):
            tmp = news["news"][i]["summary"]
            #print tmp
            download_photo(tmp)


        db.close()

        return news
    except Exception:
        news_db = {"title": "", "news": []}
        db = sql.connect('../db/raspi-tv.sqlite')

        for i in db.execute("SELECT * FROM News;").fetchall():
            news_db["news"] += [{"author": i[2],
                            "summary": i[3],
                            "title": i[0],
                            "date": i[1]}]

        return news_db


def parse_author(author):
    if "=?iso-8859-1?Q?" in author:
        slices = urllib.unquote(author.replace("=", "%").replace("\"", "")).replace("?%", "").split("%?iso-8859-1?Q?")
        author = ""
        for slice in slices:
            author += slice.strip().replace("_", " ")
    return author


def parse_date(date):

    date_time = date.split("T")
    tmp = date_time[1].split("+")
    return " Date: " + date_time[0] + " Hour: " + tmp[0]


def download_photo(tmp):
    images = re.findall('(<img[^>]*src="[^"]*"[^>]*>)', tmp)
    for image in images:
        url = re.search('(src="[^"]*")', image)
        url = url.group(0)
        url = url.split("\"")[1]

        print url

        if "cid" in url:
            pass
        else:
            name = url.split("=")
            name = name[1]
        filename = wget.download(url, "static/img/feed_imgs/" + name + ".jpg")

if __name__ == '__main__':
    resp = deti_news()