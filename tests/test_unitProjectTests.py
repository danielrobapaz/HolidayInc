from datetime import datetime
import sys
sys.path.append('../')
from . import UnitTestClass
from http.cookies import SimpleCookie
from flask import session
from app.db import get_db
from .test_unitLoginTests import *
from .test_unitUserTests import *

class unitProjectTests(UnitTestClass): 

    def test_rootCreateProject(self,name='proyect1'):
            print("rootCreateProject\n\n")
            unitLoginTests.test_loginRoot()
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
        unitUserTests.test_rootCreateUser()
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