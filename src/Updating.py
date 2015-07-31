import cherrypy
import json
import os
import sqlite3 as sql

conn = sql.connect('../db/raspi-tv.sqlite', check_same_thread=False)

class Updating:

    def retrieveUpdates(self):
        #images
        background= conn.execute('SELECT * FROM Mods WHERE idName=?', ('background',)).fetchone()[0].decode('base64')

        #text
        title= conn.execute('SELECT * FROM Mods WHERE idName=?', ('title',)).fetchone()[0]
        description= conn.execute('SELECT * FROM Mods WHERE idName=?', ('description',)).fetchone()[0]

        return [{'background':background,'title':title,'description':description}]


