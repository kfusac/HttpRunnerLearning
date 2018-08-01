import random
import requests

from tests.base import TestApiServerBase


class TestApiServer(TestApiServerBase):
    @classmethod
    def setup_class(cls):
        super().setup_class()

    @classmethod
    def teardown_class(cls):
        super().teardown_class()

    def setup_method(self):
        self.reset_all()

    def test_index(self):
        resp = self.api_client.get(self.host)
        assert 200 == resp.status_code
        assert 'Hello world' == resp.text

    def test_reset_all(self):
        resp = self.reset_all()
        assert 200 == resp.status_code
        assert resp.json()['success']

    def test_create_user_not_existed(self):
        resp = self.create_user(1000, 'user1', '123456')
        assert 200 == resp.status_code
        assert resp.json()['success']

    def test_create_user_existed(self):
        resp = self.create_user(1000, 'user1', '123456')
        resp = self.create_user(1000, 'user1', '123456')
        assert 500 == resp.status_code
        assert not resp.json()['success']

    def test_get_users_empty(self):
        resp = self.get_users()
        assert 200 == resp.status_code
        assert 0 == resp.json()['data']['count']

    def test_get_users_not_empty(self):
        resp = self.create_user(1000, 'user1', '123456')
        resp = self.get_users()
        assert 200 == resp.status_code
        assert 1 == resp.json()['data']['count']

        resp = self.create_user(1001, 'user2', '123456')
        resp = self.get_users()
        assert 200 == resp.status_code
        assert 2 == resp.json()['data']['count']

    def test_get_user_not_existed(self):
        resp = self.get_user(1000)
        assert 500 == resp.status_code
        assert not resp.json()['success']

    def test_get_user_existed(self):
        self.create_user(1000, 'user1', '123456')
        resp = self.get_user(1000)
        assert 200 == resp.status_code
        assert resp.json()['success']

    def test_updata_user_not_existed(self):
        resp = self.updata_user(1000, 'user1', '123456')
        assert 500 == resp.status_code
        assert not resp.json()['success']

    def test_updata_user_existed(self):
        self.create_user(1000, 'user1', '123456')
        resp = self.updata_user(1000, 'user2', '123456')
        assert 200 == resp.status_code
        assert 'user2' == resp.json()['data']['name']

    def test_delete_user_not_existed(self):
        resp = self.delete_user(1000)
        assert 500 == resp.status_code
        assert not resp.json()['success']

    def test_delete_user_existed(self):
        self.create_user(1000, 'zhang', '123456')
        resp = self.delete_user(1000)
        assert 200 == resp.status_code
        assert resp.json()['success']

    def reset_all(self):
        url = f'{self.host}/api/reset-all'
        return self.api_client.get(url)

    def get_users(self):
        url = f'{self.host}/api/users'
        return self.api_client.get(url)

    def create_user(self, uid, name, password):
        url = f'{self.host}/api/users/{uid}'
        data = {'name': name, 'password': password}
        return self.api_client.post(url, json=data)

    def get_user(self, uid):
        url = f'{self.host}/api/users/{uid}'
        return self.api_client.get(url)

    def updata_user(self, uid, name, password):
        url = f'{self.host}/api/users/{uid}'
        data = {'name': name, 'password': password}
        return self.api_client.put(url, json=data)

    def delete_user(self, uid):
        url = f'{self.host}/api/users/{uid}'
        return self.api_client.delete(url)
