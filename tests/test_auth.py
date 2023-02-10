from . import BaseTestsClass
from app.db import get_db

class LoginTest(BaseTestsClass):

    '''def test_loadHome(self):
        res = self.client.get('/')
        self.assertEqual(200, res.status_code)
        html = res.get_data(as_text=True)
        assert 'Welcome' in html
        #self.assertIn(b'Welcome', res.data)'''

    def test_loginNonExistentUser(self):
        ## falta qeury a db
        res = self.client.post('/auth/login', data={
            'username':'joje',
            'password':'123',
        }, follow_redirects=True)
        assert res.status_code == 200
        html = res.get_data(as_text=True)
        #self.assertIn(b"User doesn&#39;t exist.", res.data)
        assert "User doesn&#39;t exist." in html
        with self.app.app_context():
            try:
                assert get_db().execute("select * from user where username = 'joje'",).fetchone() is None
            except db.ntegrityError:
                print("uwu")
    
    def test_registerUser(self):
        res = self.client.post('/auth/register', data={
            'username':'joje',
            'password':'123'
        }, follow_redirects=True)
        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert res.request.path == '/auth/login'
        with self.app.app_context():
            assert get_db().execute("select * from user where username = 'joje'",).fetchone() is not None
      
    def test_registerAlreadyRegisteredUser(self):
        self.test_registerUser()
        username = 'joje'
        res = self.client.post('/auth/register', data={
            'username':username,
            'password':'123'
        }, follow_redirects=True)
        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert f'User &#39;{username}&#39; is already registered' in html
        with self.app.app_context():
            assert get_db().execute("select * from user where username = 'joje'",).fetchone() is not None

    def test_registerUserAuthorize(self):
        self.test_registerUser()
        with self.app.app_context():
            get_db().execute("update user set auth=1 where username = 'joje'",).fetchone()
            get_db().commit()
            assert get_db().execute("select auth from user where username = 'joje'").fetchone()[0] == 1
    
    
    def test_loginAuthorizedWrongPassword(self):
        ## falta qeury a db hasheando la clave
        self.test_registerUserAuthorize()
        res = self.client.post('/auth/login', data={
            'username':'joje',
            'password':'1234',
        }, follow_redirects=True)
        assert res.status_code == 200
        html = res.get_data(as_text=True)
        #self.assertIn(b"User doesn&#39;t exist.", res.data)
        assert "Incorrect password." in html
    
    def test_loginNonAuthorizedWrongPassword(self):
        ## falta qeury a db hasheando la clave
        self.test_registerUser()
        res = self.client.post('/auth/login', data={
            'username':'joje',
            'password':'1234',
        }, follow_redirects=True)
        assert res.status_code == 200
        html = res.get_data(as_text=True)
        #self.assertIn(b"User doesn&#39;t exist.", res.data)
        assert "User &#39;joje&#39; needs autentication from admin" in html
    
    def test_loginAuthorized(self):
        ## falta qeury a db con el hash (?)
        self.test_registerUserAuthorize()
        with self.app.app_context():
            assert get_db().execute("select auth from user where username = 'joje'").fetchone()[0] == 1
        res = self.client.post('/auth/login', data={
            'username':'joje',
            'password':'123',
        }, follow_redirects=True)
        assert res.status_code == 200
        html = res.get_data(as_text=True)
        #print(html)
        #self.assertIn(b"User doesn&#39;t exist.", res.data)
        assert "Welcome, user" in html
    
    def test_loginNonAuthorized(self):
        ## falta qeury a db con el hash (?)
        self.test_registerUser()
        res = self.client.post('/auth/login', data={
            'username':'joje',
            'password':'123',
        }, follow_redirects=True)
        assert res.status_code == 200
        html = res.get_data(as_text=True)
        #print(html)
        #self.assertIn(b"User doesn&#39;t exist.", res.data)
        assert "User &#39;joje&#39; needs autentication from admin." in html
    
    def test_logout(self):
        self.test_loginAuthorized()
        res = self.client.get('/auth/logout',follow_redirects=True)
        html = res.get_data(as_text=True)
        assert res.request.path == '/auth/login'
        assert 'Log In' in html

        ## ver session vacio user_id -> assert 'user_id' not in session
    def test_registerRoot(self):
        username = 'root'
        res = self.client.post('/auth/register', data={
            'username':username,
            'password':'root'
        }, follow_redirects=True)
        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert f'User &#39;{username}&#39; is already registered' in html
        with self.app.app_context():
            assert get_db().execute("select * from user where username = 'root'",).fetchone() is not None
        
    def test_loginRoot(self):
        res = self.client.post('/auth/login', data={
            'username':'root',
            'password':'root',
        }, follow_redirects=True)
        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Welcome, admin" in html

    def test_rootCreateUser(self):
        self.test_loginRoot()
        res = self.client.post('/createUser', data={
            'username':'joje',
            'password':'joje',
        }, follow_redirects=True)
        assert res.status_code == 200
        assert res.request.path == '/'
     
    def test_rootCreateUserAlreadyRegistered(self):
        self.test_registerUserAuthorize()
        self.test_loginRoot()
        res = self.client.post('/createUser', data={
            'username':'joje',
            'password':'joje',
        }, follow_redirects=True)
        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert f'User &#39;joje&#39; is already registered.' in html

    '''def test_rootApproveUser(self):
        self.test_registerUser()
        self.test_loginRoot()
        with self.app.app_context():
            assert get_db().execute("select * from user where auth = 0").fetchone() is not None
        
        res = self.client.post('/', data={
            'aprove':'aprove',
        }, follow_redirects=True)
        with self.app.app_context():
            assert get_db().execute("select * from user where auth = 1").fetchone() is not None
        assert res.status_code == 200
        assert res.request.path == '/'
        '''

    def test_loginEmptyAll(self):
        res = self.client.post('/auth/login', data={
            'username':None,
            'password':None,
        },follow_redirects=True)
        assert res.status_code == 400

    def test_loginEmptyUser(self):
        res = self.client.post('/auth/login', data={
            'username':None,
            'password':'123',
        },follow_redirects=True)
        assert res.status_code == 400

    def test_loginEmptyPassword(self):
        res = self.client.post('/auth/login', data={
            'username':'joje',
            'password':None,
        },follow_redirects=True)
        assert res.status_code == 400

    def test_registerEmptyAll(self):
        res = self.client.post('/auth/register', data={
            'username':None,
            'password':None,
        },follow_redirects=True)
        assert res.status_code == 400

    def test_registerEmptyUser(self):
        res = self.client.post('/auth/register', data={
            'username':None,
            'password':'123',
        },follow_redirects=True)
        assert res.status_code == 400

    def test_registerEmptyPassword(self):
        res = self.client.post('/auth/register', data={
            'username':'joje',
            'password':None,
        },follow_redirects=True)
        assert res.status_code == 400