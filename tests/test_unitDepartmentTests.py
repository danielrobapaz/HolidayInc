from datetime import datetime
import sys
sys.path.append('../')
from . import UnitTestClass
from http.cookies import SimpleCookie
from flask import session
from .test_unitLoginTests import *

class unitDepartmentTests(UnitTestClass): 

    def test_rootCreateDepartment(self):
        #print("rootCreateDepartment\n\n")
        unitLoginTests.test_loginRoot(self)
        with self.app.app_context():
            assert get_db().execute("select * from departments",).fetchone() is None
        res = self.client.post('/deparment/view', data={
            'dep':'testdpt',
            'create':''
        }, follow_redirects=True)
        assert res.status_code == 200
        assert res.request.path == '/deparment/view'
        with self.app.app_context():
            assert get_db().execute("select * from departments",).fetchone() is not None
    

    def test_rootCreateDepartmentUnique(self):
        #print("rootCreateDepartmentUnique\n\n")
        self.test_rootCreateDepartment()
        with self.app.app_context():
            assert get_db().execute("select * from departments",).fetchone() is not None
        res = self.client.post('/deparment/view', data={
            'dep':'testdpt',
            'create':''
        }, follow_redirects=True)
        assert res.status_code == 200
        assert res.request.path == '/deparment/view'
        html = res.get_data(as_text=True)
        assert f'Department testdpt already exist' in html

    
    def test_rootAddProblemToDepartment(self):
        #print("rootAddProblemToDepartment\n\n")
        self.test_rootCreateDepartment()
        with self.app.app_context():
            assert get_db().execute("select * from departments",).fetchone() is not None
            assert get_db().execute("select * from problems",).fetchone() is None
        res = self.client.post('/deparment/problems', data={
            'select':'1',
            'problem':'testproblem'
        }, follow_redirects=True)
        assert res.status_code == 200
        assert res.request.path == '/deparment/view'
        with self.app.app_context():
            assert get_db().execute("select * from problems where depId = 1",).fetchone() is not None

    

    def test_rootDeleteDepartment(self):
        #print("rootAddProblemToDepartment\n\n")
        self.test_rootCreateDepartment()
        with self.app.app_context():
            assert get_db().execute("select * from departments where id = 1",).fetchone() is not None
        res = self.client.post('/deparment/view', data={
            'delete':'1',
        }, follow_redirects=True)
        assert res.status_code == 200
        assert res.request.path == '/deparment/view'
        with self.app.app_context():
            assert get_db().execute("select * from departments where id = 1",).fetchone() is None