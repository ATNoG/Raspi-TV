import dropbox

app_key = 'rbfnah947b3iobb'
app_secret = 'l4r9iivgz4onshk'

flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)


def login(auth_code):
    authorize_url = flow.start()
    code = auth_code.strip()

    # This will fail if the user enters an invalid authorization code
    access_token, user_id = flow.finish(code)

    client = dropbox.client.DropboxClient(access_token)
    client_data = {'account_id': client.account_info()['uid'], 'name': client.account_info()['display_name'],
                   'email': client.account_info()['email'], 'access_token': access_token}
    return client_data

def list_files(access_token):
    client = dropbox.client.DropboxClient(access_token)

    raspfolder_files = client.metadata('/Apps/Raspi-TV/')['contents']
    return raspfolder_files
