from datetime import datetime
from . import UnitTestClass
from app.db import get_db
from http.cookies import SimpleCookie
from flask import session


class unitRegisterTests(UnitTestClass):
    def test_registerUser(self):
        print("registerUser\n\n")
        res = self.client.post('/auth/register', data={
            'username':'joje',
            'password':'123',
            'firstname':'jorge',
            'secondname':'correia'
        }, follow_redirects=True)
        
        assert res.status_code == 200
        
        html = res.get_data(as_text=True)
        
        assert res.request.path == '/auth/login'
        
        with self.app.app_context():
            assert get_db().execute("select * from user where username = 'joje'",).fetchone() is not None
      
    def test_registerAlreadyRegisteredUser(self):
        print("registerAlreadyRegisteredUser\n\n")
        self.test_registerUser()
        username = 'joje'
        res = self.client.post('/auth/register', data={
            'username':username,
            'password':'123',
            'firstname':'jorge',
            'secondname':'correia'
        }, follow_redirects=True)
        assert res.status_code == 200
        
        html = res.get_data(as_text=True)
        
        assert f'User &#39;{username}&#39; is already registered' in html
        
        with self.app.app_context():
            assert get_db().execute("select * from user where username = 'joje'",).fetchone() is not None

    def test_registerUserAuthorize(self):
        print("registerUserAuthorize\n\n")
        self.test_registerUser()
        with self.app.app_context():
            get_db().execute("update user set auth=1 where username = 'joje'",).fetchone()
            get_db().commit()
            assert get_db().execute("select auth from user where username = 'joje'").fetchone()[0] == 1


    def test_registerRoot(self):
        print("registerRoot")
        username = 'root'
        res = self.client.post('/auth/register', data={
            'username':username,
            'password':'root',
            'firstname':'root',
            'secondname':'root'
        }, follow_redirects=True)

        assert res.status_code == 200

        html = res.get_data(as_text=True)

        assert f'User &#39;{username}&#39; is already registered' in html

        with self.app.app_context():
            assert get_db().execute("select * from user where username = 'root'",).fetchone() is not None

    def test_registerEmptyAll(self):
        print("registerEmptyAll\n\n")
        res = self.client.post('/auth/register', data={
            'username':None,
            'password':None,
        },follow_redirects=True)
        
        assert res.status_code == 400

    def test_registerEmptyUser(self):
        print("registerEmptyUser\n\n")
        res = self.client.post('/auth/register', data={
            'username':None,
            'password':'123',
        },follow_redirects=True)
        
        assert res.status_code == 400

    def test_registerEmptyPassword(self):
        print("registerEmptyPassword\n\n")
        res = self.client.post('/auth/register', data={
            'username':'joje',
            'password':None,
        },follow_redirects=True)
        
        assert res.status_code == 400
