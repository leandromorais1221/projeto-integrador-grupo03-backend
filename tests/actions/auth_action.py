from api_organiza_ai.config.extensions import db
from api_organiza_ai.models import User
from sqlalchemy import select


class AuthAction:
    def __init__(self, client):
        self._email = 'usuarioteste@gmail.com'
        self._password = 'teste123456'
        self.client = client
        self.token = self._get_token()

    def _get_token(self):
        response = self.client.post(
            '/auth/login',
            json={
                'email': self._email,
                'password': self._password
            }
        )
        return response.json.get('access_token')

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

    def delete(self, url):
        return self.client.delete(
            url,
            headers={'Authorization': f'Bearer {self.token}'}
        )

    def get_user(self):
        stmt = select(User).where(
            User.email == self._email
        )
        return db.session.execute(stmt).scalar()


