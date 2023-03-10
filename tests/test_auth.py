from datetime import datetime
from . import BaseTestsClass
from app.db import get_db
#from http.cookies import SimpleCookie
from flask import session
class LoginTest(BaseTestsClass):

    '''def test_loadHome(self):
        res = self.client.get('/')
        self.assertEqual(200, res.status_code)
        html = res.get_data(as_text=True)
        assert 'Welcome' in html
        #self.assertIn(b'Welcome', res.data)'''

    def test_loginNonExistentUser(self):
        print("loginNonExistetUser\n\n")

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
    
    
    def test_loginAuthorizedWrongPassword(self):
        print("loginAuthorizedWrongPassword\n\n")
        self.test_registerUserAuthorize()
        res = self.client.post('/auth/login', data={
            'username':'joje',
            'password':'1234',
        }, follow_redirects=True)
        assert res.status_code == 200

        html = res.get_data(as_text=True)

        assert "Incorrect password." in html

    def test_loginNonAuthorizedWrongPassword(self):
        print("loginNonAuthorizedWrongPassword\n\n")
        self.test_registerUser()
        res = self.client.post('/auth/login', data={
            'username':'joje',
            'password':'1234',
        }, follow_redirects=True)
        assert res.status_code == 200
        
        html = res.get_data(as_text=True)

        assert "User &#39;joje&#39; needs autentication from admin" in html
    
    def test_loginAuthorized(self):
        print("loginAuthorized\n\n")
        self.test_registerUserAuthorize()
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
        self.test_registerUser()
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
        
    def test_loginRoot(self):
        print("loginRoot\n\n")
        res = self.client.post('/auth/login', data={
            'username':'root',
            'password':'root',
        }, follow_redirects=True)

        assert res.status_code == 200

        html = res.get_data(as_text=True)
        assert "Welcome, root" in html

    def test_rootCreateProject(self,name='proyect1'):
        print("rootCreateProject\n\n")
        self.test_loginRoot()
        if name != 'proyect2':
            with self.app.app_context():
                db = get_db()
                assert db.execute("select * from proyect where description = 'proyect1' ").fetchone() is None
        res = self.client.post('/createProyect', data={
            'description':name,
            'starting-date':'2023-01-26',
            'end-date':'2023-02-26'
        }, follow_redirects=True)

        with self.app.app_context():
            db = get_db()
            data = db.execute("select * from proyect where description = 'proyect1'").fetchone()
            assert data['end'] == datetime(2023,2,26).date() and data['start'] == datetime(2023,1,26).date() and data['description'] == 'proyect1'
        assert res.status_code == 200
        assert res.request.path == '/user/root'

    def test_rootCreateUser(self):
        print("rootCreateUser\n\n")
        self.test_rootCreateProject()
        res = self.client.post('/createUser', data={
            'username':'joje',
            'password':'joje',
            'firstname':'jorge',
            'secondname':'correia',
            'role':'op_manager',
            'proyect':'1'
        }, follow_redirects=True)
        assert res.status_code == 200
        assert res.request.path == '/user/root'

    def test_rootCreateUserAlreadyRegistered(self):
        print("rootCreateUserAlreadyRegistered\n\n")
        self.test_registerUserAuthorize()
        self.test_loginRoot()
        res = self.client.post('/createUser', data={
            'username':'joje',
            'password':'joje',
            'firstname':'jorge',
            'secondname':'correia',
            'role':'op_manager',
            'proyect':'1'
        }, follow_redirects=True)
        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert f'User &#39;joje&#39; is already registered.' in html

    def test_rootApproveUser(self):
        print("rootApproveUser\n\n")
        self.test_registerUser()
        self.test_rootCreateProject()
        
        with self.app.app_context():
            id = get_db().execute("select id from user where auth = 0").fetchone()[0]
            assert get_db().execute("select * from user where auth = 0").fetchone() is not None
        with self.client.session_transaction() as session:
            session['aprove_user'] = id
        res = self.client.post('/aproveUser', data={
            'role':'op_manager',
            'proyect':'1',
            'aprove':'aprove',
        }, follow_redirects=True)
        with self.app.app_context():
            assert get_db().execute("select * from user where auth = 1").fetchone() is not None
        assert res.status_code == 200
        assert res.request.path == '/user/root'

    def test_rootRejectUser(self):
        print("rootRejectUser\n\n")
        self.test_registerUser()
        self.test_loginRoot()
        
        with self.app.app_context():
            db = get_db()
            id = db.execute("select id from user where auth = 0").fetchone()
            assert db.execute("select * from user where auth = 0").fetchone() is not None
        res = self.client.post('/user/root', data={
            'reject': id[0],
        }, follow_redirects=True)
        with self.app.app_context():
            db = get_db()
            data = db.execute("select * from user where auth = 1")
            
            #count how many user has auth = 1;
            count = 0
            for row in data:
                count = count + 1
            assert count == 1
        assert res.status_code == 200
        assert res.request.path == '/user/root'

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

    def test_rootEnableProject(self):
        print("rootEnableProject\n\n")
        self.test_rootCreateProject()
        with self.app.app_context():
            db = get_db()
            assert db.execute("select status from proyect where id = 1").fetchone()[0] == 0

        res = self.client.post('/user/root', data={
            'enable-proyect':'1',
        }, follow_redirects=True)

        with self.app.app_context():
            db = get_db()
            assert db.execute("select status from proyect where id = 1").fetchone()[0] == 1
        assert res.status_code == 200
        assert res.request.path == '/user/root'

    def test_rootDisableProject(self):
        print("rootDisableProject\n\n")
        self.test_rootEnableProject()
        with self.app.app_context():
            db = get_db()
            assert db.execute("select status from proyect where id = 1").fetchone()[0] == 1

        res = self.client.post('/user/root', data={
            'close-proyect':'1',
        }, follow_redirects=True)

        with self.app.app_context():
            db = get_db()
            assert db.execute("select status from proyect where id = 1").fetchone()[0] == 0
        assert res.status_code == 200
        assert res.request.path == '/user/root'

    def test_rootModifyProject(self):
        self.test_rootCreateProject()
        print("rootCreateProject\n\n")
        with self.app.app_context():
            db = get_db()
            assert db.execute("select * from proyect where id = 1").fetchone() is not None
        with self.client.session_transaction() as session:
            session['modify_proyect'] = '1'
        res = self.client.post('/changeDatesProyect', data={
            'starting-date':datetime(2023,4,26).date(),
            'end-date':datetime(2023,5,26).date(),
        }, follow_redirects=True)
        
        with self.app.app_context():
            db = get_db()
            data = db.execute("select * from proyect where description = 'proyect1'").fetchone()
            assert data['end'] == datetime(2023,5,26).date() and data['start'] == datetime(2023,4,26).date()
        assert res.status_code == 200
        assert res.request.path == '/user/root'

    def test_rootDeleteProject(self):
        self.test_rootCreateProject()
        print("rootDeleteProject\n\n")
        with self.app.app_context():
            db = get_db()
            assert db.execute("select * from proyect where id = 1").fetchone() is not None
        with self.client.session_transaction() as session:
            session['modify_proyect'] = '1'
        res = self.client.post('/modifyProyect', data={
            'delete':'delete'
        }, follow_redirects=True)
        
        with self.app.app_context():
            db = get_db()
            assert db.execute("select * from proyect where description = 'proyect1'").fetchone() is None
        assert res.status_code == 200
        assert res.request.path == '/user/root'


    def test_userChangeProyect(self):
        print("rootUserChangeProyect\n\n")
        self.test_rootCreateUser()
        self.test_rootCreateProject('proyect2')
        with self.app.app_context():    
            db = get_db()
            p1 = db.execute("select * from proyect where description = 'proyect1'").fetchone()
            p2 = db.execute("select * from proyect where description = 'proyect2'").fetchone()
            u1 = db.execute("select proyId from user where id = '2'").fetchone()
            assert p1 is not None and p2 is not None
            assert u1[0] == 1
        with self.client.session_transaction() as session:
            session['modify_user'] = '2'
        res = self.client.post('/modifyUser/changeProyect', data={
            'proyect':'2',
        }, follow_redirects=True)
        with self.app.app_context():    
            db = get_db()
            p1 = db.execute("select * from proyect where description = 'proyect1'").fetchone()
            p2 = db.execute("select * from proyect where description = 'proyect2'").fetchone()
            u1 = db.execute("select proyId from user where id = '2'").fetchone()
            assert p1 is not None and p2 is not None
            assert u1[0] == 2
        assert res.status_code == 200
        assert res.request.path == '/user/root'

    def test_userDeleteUser(self):
            print("rootUserDeleteUser\n")
            self.test_rootCreateUser()
            with self.app.app_context():    
                db = get_db()
                u1 = db.execute("select * from user where id = '2'").fetchone()
                assert u1 is not None
            with self.client.session_transaction() as session:
                session['modify_user'] = '2'
            res = self.client.post('/modifyUser', data={
                'delete':'delete',
            }, follow_redirects=True)
            with self.app.app_context():    
                db = get_db()
                u1 = db.execute("select * from user where id = '2'").fetchone()
                assert u1 is None
            assert res.status_code == 200
            assert res.request.path == '/user/root'

    def test_userChangeRole(self):
            print("rootUserChangeRole\n")
            self.test_rootCreateUser()
            with self.app.app_context():    
                db = get_db()
                u1 = db.execute("select * from user where id = 2").fetchone()
                # db.execute("INSERT INTO roles (name, description) VALUES ('mechanic_sup', 'Supervisor del area de mecanica')")
                # db.commit()
                # r1 = db.execute("select * from roles where id = 1").fetchone()
                # r2 = db.execute("select * from roles where id = 2").fetchone()
                assert u1 is not None
                assert u1['role'] == 'op_manager'
            with self.client.session_transaction() as session:
                session['modify_user'] = '2'
            res = self.client.post('/modifyUser/changeRole', data={
                'select':'mechanic_sup',
            }, follow_redirects=True)
            with self.app.app_context():    
                db = get_db()
                u1 = db.execute("select * from user where id = 2").fetchone()
                # r1 = db.execute("select * from roles where id = 1").fetchone()
                # r2 = db.execute("select * from roles where id = 2").fetchone()
                print(u1['role'])
                # assert u1 is not None and r1 is not None and r2 is not None
                assert u1 is not None
                assert u1['role'] == 'mechanic_sup'
            assert res.status_code == 200
            assert res.request.path == '/user/root'