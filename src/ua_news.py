import feedparser
import urllib
import sqlite3 as sql
import requests
import re
import wget


def deti_news():
    open("static/img/feed_imgs/156.jpg", "r")
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
            tmp = news["news"][i]["summary"]
            new_tmp = download_photo(tmp)

            if new_tmp:
                db.execute("INSERT INTO News VALUES (?,?,?,?);",
                        (news["news"][i]["title"], news["news"][i]["date"], news["news"][i]["author"], new_tmp))
                db.commit()
            else:
                db.execute("INSERT INTO News VALUES (?,?,?,?);",
                        (news["news"][i]["title"], news["news"][i]["date"], news["news"][i]["author"], tmp))
                db.commit()

        news_db = {"title": "", "news": []}
        for i in db.execute("SELECT * FROM News;").fetchall():
            news_db["news"] += [{"author": i[2],
                            "summary": i[3],
                            "title": i[0],
                            "date": i[1]}]

        db.close()


        return news_db
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

        if "cid" in url:
            return
        else:
            name = url.split("=")
            name = name[1]
            filename = wget.download(url, "static/img/feed_imgs/" + name + ".jpg")
            new_path_url = ["img/feed_imgs/" + name + ".jpg", url]

            return tmp.replace(new_path_url[1], new_path_url[0])

if __name__ == '__main__':
    resp = deti_news()