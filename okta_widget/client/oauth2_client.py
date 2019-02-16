import requests
import json
import base64
import http.client
from django.conf import settings


class OAuth2Client(object):
    def __init__(self, base_url, client_id=None, client_secret=None):
        self.host = base_url.replace('https://', '').replace('http://', '')
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.basic = None
        if client_id is not None and client_secret is not None:
            enc = client_id + ':' + client_secret
            basic = base64.b64encode(enc.encode('ascii'))
            self.basic = str(basic, 'utf-8')

    def authorize(self, session_token, oauth_params, server_id='default'):
        url = '/oauth2/{0}/v1/authorize?client_id={1}' \
              '&response_type={2}' \
              '&scope={3}' \
              '&redirect_uri={4}' \
              '&state={5}' \
              '&nonce={6}' \
              '&sessionToken={7}' \
            .format(server_id,
                    oauth_params['client_id'],
                    'code',
                    'openid+email+profile',
                    oauth_params['redirect_uri'],
                    'foo',
                    'foo',
                    session_token
                    )
        # print(self.base_url + url)
        connection = http.client.HTTPSConnection(self.host)
        headers = {'Content-type': 'application/json'}
        connection.request(method='GET', url=url, body={}, headers=headers)
        response_headers = connection.getresponse().getheaders()
        redirect = None
        for h in response_headers:
            if 'Location' in h:
                redirect = h[1]
                print('Location={}'.format(redirect))
            if 'Set-Cookie' in h:
                if h[1].startswith('sid='):
                    sid = h[1][4:].split(';')[0]
                    print('sid={}'.format(sid))
        return redirect

    def token(self, code, redirect_uri, server_id=None):
        if server_id:
            server_id += '/'
        else:
            server_id = ''
        url = self.base_url + '/oauth2/{}v1/token'.format(server_id)
        payload = {
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri,
            'code': code
        }
        auth = {}
        if self.basic:
            auth = {'Authorization': 'Basic ' + self.basic}
        response = requests.post(url, data=payload, headers=auth)
        tokens = response.json()
        print('tokens = {}'.format(tokens))
        return tokens

    def profile(self, token):
        iss = 'https://{0}/oauth2/{1}'.format(settings.OKTA_ORG, settings.AUTH_SERVER_ID)
        #iss = _tokenIssuer(token)
        if iss:
            url = iss + '/v1/userinfo'
        else:
            url = self.base_url + '/oauth2/v1/userinfo'
        print('userinfo url={}'.format(url))

        headers = {'Authorization': 'Bearer ' + token}
        profile = {}
        try:
            response = requests.post(url, headers=headers, verify=False)
            print('response = {}'.format(response))
            if response.status_code == 200:
                profile = response.json()
        except Exception as e:
            print('exception: {}'.format(e))

        # IMPERSONATION Hack: Get the profile from the "Other" issuer
        if profile == {} and settings.IMPERSONATION_ORG and settings.IMPERSONATION_ORG != 'None'\
                and settings.IMPERSONATION_ORG_AUTH_SERVER_ID and settings.IMPERSONATION_ORG_AUTH_SERVER_ID != 'None':
            url = 'https://{0}/oauth2/{1}/v1/userinfo'.format(settings.IMPERSONATION_ORG, settings.IMPERSONATION_ORG_AUTH_SERVER_ID)
            print('userinfo url={}'.format(url))
            try:
                response = requests.post(url, headers=headers, verify=False)
                profile = response.json()
            except Exception as e2:
                print('exception2: {}'.format(e2))

        return profile


def _tokenIssuer(token):
    iss = None
    try:
        parts = token.split('.')
        payload = parts[1]
        payload += '=' * (-len(payload) % 4)
        decoded = base64.b64decode(payload)
        print('payload = {}'.format(decoded))
        iss = json.loads(decoded)['iss']
    except Exception as e:
        print('there was an exception: {}'.format(e))
        return None
    print('iss = {}'.format(iss))
    return iss


