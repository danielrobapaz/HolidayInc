from datetime import datetime
import sys
sys.path.append('../')
from . import UnitTestClass
from http.cookies import SimpleCookie
from flask import session
import unittest
from app.db import get_db
from .test_unitRegisterTests import *

class unitLoginTests(UnitTestClass):

    def test_loginNonExistentUser(self):
        print("loginNonExistentUser\n\n")
        res = self.client.post('/auth/login', data={
            'username':'joje',
            'password':'123',
        }, follow_redirects=True)
        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "User doesn&#39;t exist." in html
        
        with self.app.app_context():
            try:
                db = get_db()
                assert db.execute("select * from user where username = 'joje'",).fetchone() is None
            except db.IntegrityError:
                pass
    
    def test_loginAuthorizedWrongPassword(self):
        print("loginAuthorizedWrongPassword\n\n")
        unitRegisterTests.test_registerUserAuthorize(self)
        res = self.client.post('/auth/login', data={
            'username':'joje',
            'password':'1234',
        }, follow_redirects=True)
        assert res.status_code == 200

        html = res.get_data(as_text=True)

        assert "Incorrect password." in html

    def test_loginNonAuthorizedWrongPassword(self):
        print("loginNonAuthorizedWrongPassword\n\n")
        unitRegisterTests.test_registerUser(self)
        res = self.client.post('/auth/login', data={
            'username':'joje',
            'password':'1234',
        }, follow_redirects=True)
        assert res.status_code == 200
        
        html = res.get_data(as_text=True)

        assert "User &#39;joje&#39; needs autentication from admin" in html
    
    def test_loginAuthorized(self):
        print("loginAuthorized\n\n")
        unitRegisterTests.test_registerUserAuthorize(self)
        with self.app.app_context():
            assert get_db().execute("select auth from user where username = 'joje'").fetchone()[0] == 1
        res = self.client.post('/auth/login', data={
            'username':'joje',
            'password':'123',
        }, follow_redirects=True)
        assert res.status_code == 200
        
        html = res.get_data(as_text=True)
        
        assert "Welcome, joje" in html
    
    def test_loginNonAuthorized(self):
        print("loginNonAuthorized\n\n")
        unitRegisterTests.test_registerUser(self)
        res = self.client.post('/auth/login', data={
            'username':'joje',
            'password':'123',
        }, follow_redirects=True)

        assert res.status_code == 200

        html = res.get_data(as_text=True)

        assert "User &#39;joje&#39; needs autentication from admin." in html
    
    def test_logout(self):
        print("logout\n\n")
        self.test_loginAuthorized()
        res = self.client.get('/auth/logout',follow_redirects=True)
        html = res.get_data(as_text=True)

        assert res.request.path == '/auth/login'

        assert 'Log In' in html

    def test_loginRoot(self):
        print("loginRoot\n\n")
        res = self.client.post('/auth/login', data={
            'username':'root',
            'password':'root',
        }, follow_redirects=True)

        assert res.status_code == 200

        html = res.get_data(as_text=True)
        assert "Welcome, root" in html

    def test_loginEmptyAll(self):
        print("loginEmptyAll\n\n")
        res = self.client.post('/auth/login', data={
            'username':None,
            'password':None,
        },follow_redirects=True)
        assert res.status_code == 400

    def test_loginEmptyUser(self):
        print("loginEmptyUser\n\n")
        res = self.client.post('/auth/login', data={
            'username':None,
            'password':'123',
        },follow_redirects=True)
        assert res.status_code == 400

    def test_loginEmptyPassword(self):
        print("loginEmptyPassword\n\n")
        res = self.client.post('/auth/login', data={
            'username':'joje',
            'password':None,
        },follow_redirects=True)
        
        assert res.status_code == 400

if __name__ == "__main__":
    unittest.main(verbosity=3)