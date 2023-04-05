from datetime import datetime
import sys
sys.path.append('../')
from . import UnitTestClass
from http.cookies import SimpleCookie
from flask import session
from .test_unitProjectTests import *
from .test_unitLoginTests import *
from .test_unitRegisterTests import *

class unitUserTests(UnitTestClass): 

    def test_rootCreateUser(self):
        print("rootCreateUser\n\n")
        unitProjectTests.test_rootCreateProject(self)
        res = self.client.post('/root/createUser', data={
            'username':'joje',
            'password':'joje',
            'firstname':'jorge',
            'secondname':'correia',
            'role':'3',
            'proyect':'1'
        }, follow_redirects=True)
        assert res.status_code == 200
        assert res.request.path == '/root/users'

    def test_rootCreateUserAlreadyRegistered(self):
        print("rootCreateUserAlreadyRegistered\n\n")
        unitRegisterTests.test_registerUserAuthorize(self)
        unitLoginTests.test_loginRoot(self)
        res = self.client.post('/root/createUser', data={
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
        unitRegisterTests.test_registerUser(self)
        unitProjectTests.test_rootCreateProject(self)
        
        with self.app.app_context():
            id = get_db().execute("select id from user where auth = 0").fetchone()[0]
            assert get_db().execute("select * from user where auth = 0").fetchone() is not None
        with self.client.session_transaction() as session:
            session['aprove_user'] = id
        res = self.client.post('/root/aproveUser', data={
            'role':'3',
            'proyect':'1',
            'aprove':'aprove',
        }, follow_redirects=True)
        with self.app.app_context():
            assert get_db().execute("select * from user where auth = 1").fetchone() is not None
        assert res.status_code == 200
        assert res.request.path == '/user/root'

    def test_rootRejectUser(self):
        print("rootRejectUser\n\n")
        unitRegisterTests.test_registerUser(self)
        unitLoginTests.test_loginRoot(self)
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

    def test_userDeleteUser(self):
            print("rootUserDeleteUser\n")
            self.test_rootCreateUser()
            with self.app.app_context():    
                db = get_db()
                u1 = db.execute("select * from user where id = '2'").fetchone()
                assert u1 is not None
            with self.client.session_transaction() as session:
                session['modify_user'] = '2'
            res = self.client.post('/root/user/modifyUser', data={
                'delete':'delete',
            }, follow_redirects=True)
            with self.app.app_context():    
                db = get_db()
                u1 = db.execute("select * from user where id = '2'").fetchone()
                assert u1 is None
            assert res.status_code == 200
            assert res.request.path == '/root/users'

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
                assert u1['roleId'] == 3
            with self.client.session_transaction() as session:
                session['modify_user'] = '2'
            res = self.client.post('/root/user/modifyUser/changeRole', data={
                'select':'5',
            }, follow_redirects=True)
            with self.app.app_context():    
                db = get_db()
                u1 = db.execute("select * from user where id = 2").fetchone()
                # r1 = db.execute("select * from roles where id = 1").fetchone()
                # r2 = db.execute("select * from roles where id = 2").fetchone()
                #print(u1['role'])
                # assert u1 is not None and r1 is not None and r2 is not None
                assert u1 is not None
                assert u1['roleId'] == 5
            assert res.status_code == 200
            assert res.request.path == '/root/users'