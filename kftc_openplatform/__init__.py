# -*- coding: utf-8 -*-
import requests
from requests.compat import urlencode

# ENDPOINT = 'https://openapi.open-platform.or.kr'
ENDPOINT = 'https://testapi.open-platform.or.kr'

CLIENT_ID = '{CLIENT-ID}'
CLIENT_SECRET = '{CLIENT-SECRET}'
REDIRECT_URI = 'http://localhost:5000/callback'


class KftcOpenAPI(object):

    def __init__(self, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def build_authorize_url(self, scope, redirect_uri=None, client_info='', auth_type=0):
        params = dict(
            response_type='code',
            client_id=self.client_id,
            redirect_uri=redirect_uri or self.redirect_uri,
            scope=scope,
            client_info=client_info,
            auth_type=auth_type,
        )

        url = '{endpoint}/oauth/2.0/authorize2?{encoded_params}'.format(
            endpoint=ENDPOINT,
            encoded_params=urlencode(params)
        )
        return url

    def get_token(self, code, redirect_uri=None):
        url = '{endpoint}/oauth/2.0/token'.format(endpoint=ENDPOINT)

        data = dict(
            code=code,
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=redirect_uri or self.redirect_uri,
            grant_type='authorization_code',
        )

        r = requests.post(url, data=data)
        # TODO: handle error
        res = r.json()
        return res
