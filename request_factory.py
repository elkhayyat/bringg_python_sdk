import requests

from responses import GetTokenResponse, AssignDriverResponse


class BringgRequest:
    def __init__(self, url, data, response_class):
        self.url = url
        self.data = data
        self.response_class = response_class
        self._response = None
        self.response = None

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
        }

    def serialize_response(self):
        self.response = self.response_class(self._response)

    def post(self):
        self._response = requests.post(self.url, headers=self.get_headers(), json=self.data)
        self.serialize_response()
        return self.response


class AuthorizedBringgRequest(BringgRequest):
    def __init__(self, url, data, token, response_class):
        super().__init__(url, data, response_class)
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}',
        }


class GetTokenRequest(BringgRequest):
    def __init__(self, url, client_id, secret_key):
        data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': secret_key,
        }
        super().__init__(url, data, GetTokenResponse)


class AssignDriverRequest(AuthorizedBringgRequest):
    def __init__(self, url, data, token):
        super().__init__(url, data, token, AssignDriverResponse)
