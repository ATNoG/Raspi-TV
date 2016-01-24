import sqlite3 as sql

import os

###################
# Constants go here
###################
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
conn = sql.connect(os.path.join(ROOT_DIR, '../db/raspi-tv.sqlite'), check_same_thread=False)
# conn = sql.connect(os.path.join(ROOT_DIR, '../db/raspi-tv.sqlite'))


########################
# Useful implementations
########################
# class SQLMultiThread(Thread):
#     def __init__(self, db):
#         super(SQLMultiThread, self).__init__()
#         self.db = db
#         self.reqs = Queue()
#         self.start()
#
#     def run(self):
#         cnx = sql.Connection(self.db)
#         cursor = cnx.cursor()
#         while True:
#             req, arg, res = self.reqs.get()
#             if req == '--close--': break
#             cursor.execute(req, arg)
#             if res:
#                 for rec in cursor:
#                     res.put(rec)
#                 res.put('--no more--')
#         cnx.close()
#
#     def execute(self, req, arg=None, res=None):
#         self.reqs.put((req, arg or tuple(), res))
#
#     def select(self, req, arg=None):
#         res = Queue()
#         self.execute(req, arg, res)
#         while True:
#             rec = res.get()
#             if rec == '--no more--': break
#             yield rec
#
#     def close(self):
#         self.execute('--close--')


###########################################################
# Other constants (which require some implementation above)
###########################################################
# conn = SQLMultiThread(os.path.join(ROOT_DIR, '../db/raspi-tv.sqlite'))
