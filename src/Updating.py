import cherrypy
import json
import os
import sqlite3 as sql

conn = sql.connect('../db/raspi-tv.sqlite', check_same_thread=False)

class Updating:

    def retrieveUpdates(self):
        response=[]

        background= conn.execute('SELECT * FROM Mods WHERE idName=?', ('background',)).fetchone()[0].decode('base64')
        response.append({id:'background','type':'image', 'content':background})

        title= conn.execute('SELECT * FROM Mods WHERE idName=?', ('title',)).fetchone()[0]
        response.append({id:'title','type':'text', 'content':title})

        description= conn.execute('SELECT * FROM Mods WHERE idName=?', ('description',)).fetchone()[0]
        response.append({id:'background','type':'text', 'content':description})

        return json.dumps(response)


