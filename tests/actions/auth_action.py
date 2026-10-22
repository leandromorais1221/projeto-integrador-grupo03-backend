

class AuthAction:
    def __init__(self, client):
        self.client = client
        self.token = self._get_token()
        
    def _get_token(self):
        response = self.client.post(
            '/auth/login',
            json={
                'email': 'usuarioteste@gmail.com',
                'password': 'teste123456'
            }
        )
        return response.json['access_token']

    def get(self, url):
        return self.client.get(
            url,
            headers={'Authorization': f'Bearer {self.token}'}
        )

    def post(self, url, body):
        return self.client.post(
            url,
            json=body,
            headers={'Authorization': f'Bearer {self.token}'}
        )

    def put(self, url, body):
        return self.client.put(
            url,
            json=body,
            headers={'Authorization': f'Bearer {self.token}'}
        )

    def delete(self, url, body):
        return self.client.delete(
            url,
            json=body,
            headers={'Authorization': f'Bearer {self.token}'}
        )
