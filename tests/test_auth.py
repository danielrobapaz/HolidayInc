from . import BaseTestsClass

class LoginTest(BaseTestsClass):

    def test_loadHome(self):
        res = self.client.get('/')
        self.assertEqual(200, res.status_code)
        html = res.get_data(as_text=True)
        assert 'Welcome' in html
        #self.assertIn(b'Welcome', res.data)

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

    def test_registerUser(self):
        res = self.client.post('/auth/register', data={
            'username':'joje',
            'password':'123'
        }, follow_redirects=True)
        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert res.request.path == '/auth/login'
        #assert self.app.get_db().execute(
        #        "SELECT * FROM user where username = 'joje'").fetchone() is not None

    def test_registerAlreadyRegisteredUser(self):

        ## falta qeury a db
        self.test_registerUser()
        username = 'joje'
        res = self.client.post('/auth/register', data={
            'username':username,
            'password':'123'
        }, follow_redirects=True)
        assert res.status_code == 200
        html = res.get_data(as_text=True)
        #print(html)
        assert f'User {username} is already registered' in html
        #assert res.request.path == '/auth/login'
       
    
    def test_loginWrongPassword(self):
        ## falta qeury a db hasheando la clave
        self.test_registerUser()
        res = self.client.post('/auth/login', data={
            'username':'joje',
            'password':'1234',
        }, follow_redirects=True)
        assert res.status_code == 200
        html = res.get_data(as_text=True)
        #self.assertIn(b"User doesn&#39;t exist.", res.data)
        assert "Incorrect password." in html

    def test_loginCorrectPassword(self):
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
        assert "Welcome" in html

    def test_logout(self):
        self.test_loginCorrectPassword()
        res = self.client.get('/auth/logout',follow_redirects=True)
        html = res.get_data(as_text=True)
        assert res.request.path == '/auth/login'
        assert 'Log In' in html

        ## ver session vacio user_id -> assert 'user_id' not in session


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
        #print(html)