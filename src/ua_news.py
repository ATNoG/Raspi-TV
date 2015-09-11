import feedparser
import urllib
import sqlite3 as sql
import re
import wget
import os
import glob
from settings import *

conn = sql.connect(os.path.join(BASE_DIR, 'db/raspi-tv.sqlite'), check_same_thread=False)


def deti_news():
    try:
        feed_source = conn.execute('SELECT * FROM HTMLSettings WHERE idName=?', ('feed',)).fetchone()[1]
        feed_content = feedparser.parse(feed_source)

        news = {"title": feed_content.feed.title, "news": [], "videos": []}

        #delete all the images

        files = glob.glob('static/img/feed_imgs/*')
        for f in files:
            os.remove(f)

        conn.execute("DELETE FROM News;")

        for entry in feed_content.entries:
            news["news"] += [{"author": parse_author(entry.author),
                            "summary": entry.summary,
                            "title": entry.title,
                            "date": parse_date(str(entry.updated))}]

        for i in range(0, len(news["news"])):
            tmp = news["news"][i]["summary"]
            new_tmp = download_photo(tmp)

            # try to clean...
            new_tmp = new_tmp.replace("<p class=\"MsoNormal\"></p>", "")
            new_tmp = new_tmp.replace("<p></p>", "")
            new_tmp = new_tmp.replace("<br>", "")
            new_tmp = new_tmp.replace("<br />", "")
            new_tmp = new_tmp.replace("<p>&nbsp;</p>", "")

            # news without images

            tmp = tmp.replace("<p class=\"MsoNormal\"></p>", "")
            tmp = tmp.replace("<p></p>", "")
            tmp = tmp.replace("<br>", "")
            tmp = tmp.replace("<br />", "")
            tmp = tmp.replace("<p>&nbsp;</p>", "")

            spaces = re.findall('(<p[^>]*><p[^>]*>.</p></p>&#13;)', new_tmp)
            for space in spaces:
                new_tmp = new_tmp.replace(space, "")
                tmp = tmp.replace(space, "")

            if new_tmp:
                conn.execute("INSERT INTO News VALUES (?,?,?,?);",
                        (news["news"][i]["title"], news["news"][i]["date"], news["news"][i]["author"], new_tmp))
                conn.commit()
            else:
                conn.execute("INSERT INTO News VALUES (?,?,?,?);",
                        (news["news"][i]["title"], news["news"][i]["date"], news["news"][i]["author"], tmp))
                conn.commit()
    except Exception, e:
        print e.message

    news_db = {"title": "", "news": [], "videos": []}

    for i in conn.execute("SELECT * FROM News;").fetchall():
        news_db["news"] += [{"author": i[2],
                        "summary": i[3],
                        "title": i[0],
                        "date": i[1]}]

    for j in conn.execute("SELECT * FROM YouTube;").fetchall():
        news_db["videos"] += [{'link': j[0], 'name': j[1]}]

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

        if "cid" in url:
            tmp = tmp.replace(image, "")
        else:
            name = url.split("=")
            name = name[1]
            if not os.path.exists("static/img/feed_imgs"):
                os.makedirs("static/img/feed_imgs")

            filename = wget.download(url, "static/img/feed_imgs/" + name + ".jpg")

            new_path_url = ["img/feed_imgs/" + name + ".jpg", url]
            tmp = tmp.replace(new_path_url[1], new_path_url[0])

    return tmp

if __name__ == '__main__':
    resp = deti_news()