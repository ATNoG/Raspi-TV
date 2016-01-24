import cherrypy
from __init__ import conn

SESSION_USER = '_cp_user'
SESSION_LOGIN = '_cp_login'


def checkpassword(realm, username, password):
    """
    Check if 'username' can be authenticated. Works as a login would
    """
    if SESSION_LOGIN in cherrypy.session and not cherrypy.session[SESSION_LOGIN]:
        cherrypy.session[SESSION_LOGIN] = True
        return False
    user = conn.execute('SELECT * FROM Users WHERE UserId=?', (username,)).fetchone()
    if user and user[1] == password:
        cherrypy.session[SESSION_USER] = {
            'UserId': user[0],
            'FirstName': user[2],
            'LastName': user[3],
            'Email': user[4],
            'Date': user[5]
        }
        cherrypy.session[SESSION_LOGIN] = True
        return True
    return False


@cherrypy.expose
def logout():
    """
    Logs-out a user by simply saving that he is not logged-in
    """
    cherrypy.session[SESSION_LOGIN] = False
    raise cherrypy.HTTPRedirect('/public')
