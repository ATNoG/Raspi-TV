import dropbox

# app_key = 'rbfnah947b3iobb'
# app_secret = 'l4r9iivgz4onshk'
#
# flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
#
#
# def login(auth_code):
#     authorize_url = flow.start()
#     code = auth_code.strip()
#
#     # This will fail if the user enters an invalid authorization code
#     access_token, user_id = flow.finish(code)
#
#     client = dropbox.client.DropboxClient(access_token)
#     client_data = {'account_id': client.account_info()['uid'], 'name': client.account_info()['display_name'],
#                    'email': client.account_info()['email'], 'access_token': access_token}
#     return client_data
#
def list_files(access_token):
    client = dropbox.client.DropboxClient(access_token)

    rasp_folder_files = client.metadata('/')['contents']
    return rasp_folder_files

# from dropbox.client import DropboxOAuth2Flow, DropboxClient
#
#
# def get_dropbox_auth_flow(web_app_session):
#     redirect_uri = "http://localhost:63342/Raspi-TV/src/static/admin/pages/accounts/accounts.html#dropbox"
#     return DropboxOAuth2Flow('rbfnah947b3iobb', 'l4r9iivgz4onshk', redirect_uri,
#                              web_app_session, "dropbox-auth-csrf-token")
#
# # URL handler for /dropbox-auth-start
# def dropbox_auth_start(web_app_session, request):
#     authorize_url = get_dropbox_auth_flow(web_app_session).start()
#     redirect_to(authorize_url)
#
#
# # URL handler for /dropbox-auth-finish
# def dropbox_auth_finish(web_app_session, request):
#     try:
#         access_token, user_id, url_state = \
#                 get_dropbox_auth_flow(web_app_session).finish(request.query_params)
#     except DropboxOAuth2Flow.BadRequestException:
#         http_status(400)
#     except DropboxOAuth2Flow.BadStateException:
#         # Start the auth flow again.
#         redirect_to("/dropbox-auth-start")
#     except DropboxOAuth2Flow.CsrfException:
#         http_status(403)
#     except DropboxOAuth2Flow.NotApprovedException:
#         return home()
#     except DropboxOAuth2Flow.ProviderException, e:
#         logger.log("Auth error: %s" % (e,))
#         http_status(403)


# import webbrowser
# import dropbox
#
#
# def connect():
#     """
#     Connect and authenticate with dropbox
#     """
#     app_key = 'rbfnah947b3iobb'
#     app_secret = 'l4r9iivgz4onshk'
#
#     access_type = "dropbox"
#     session = dropbox.session.DropboxSession(app_key,
#                                              app_secret,
#                                              access_type)
#
#     request_token = session.obtain_request_token()
#
#     url = session.build_authorize_url(request_token)
#     msg = "Opening %s. Please make sure this application is allowed before continuing."
#     print msg % url
#     webbrowser.open(url)
#     raw_input("Press enter to continue")
#     access_token = session.obtain_access_token(request_token)
#
#     client = dropbox.client.DropboxClient(session)
#     client_data = {'account_id': client.account_info()['uid'], 'name': client.account_info()['display_name'],
#                    'email': client.account_info()['email'], 'access_token': access_token}
#
#     print client_data
#
# connect()
