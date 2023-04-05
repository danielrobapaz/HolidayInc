from datetime import datetime
import sys
sys.path.append('../')
from . import UnitTestClass
from http.cookies import SimpleCookie
from flask import session
from .test_unitLoginTests import *

class unitDepartmentTests(UnitTestClass): 

    def test_rootCreateDepartment(self):
        print("rootCreateDepartment\n\n")
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
        print("rootCreateDepartmentUnique\n\n")
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
        print("rootAddProblemToDepartment\n\n")
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
        print("rootAddProblemToDepartment\n\n")
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


    
        

    '''def test_rootCreateClient(self):
        print("rootCreateClient\n\n")
        unitLoginTests.test_loginRoot(self)
        with self.app.app_context():
            assert get_db().execute("select * from clients",).fetchone() is None
        res = self.client.post('/clients/addClient', data={
            'dni':'V-1111111',
            'firstname':'jorge',
            'secondname':'correia',
            'birthday':'1970-03-31',
            'phone':'0414-1234032',
            'mail':'something@example.com',
            'address':'Caracas'
        }, follow_redirects=True)
        assert res.status_code == 200
        assert res.request.path == '/clients'
        with self.app.app_context():
            assert get_db().execute("select * from clients where dni = 'V-1111111'",).fetchone() is not None

    def test_rootCreateClientMissingField(self):
        print("rootCreateClientMissingField\n\n")
        unitLoginTests.test_loginRoot(self)
        with self.app.app_context():
            assert get_db().execute("select * from clients",).fetchone() is None
        res = self.client.post('/clients/addClient', data={
            'dni':'V-1111111',
            'firstname':'',
            'secondname':'correia',
            'birthday':'1970-03-31',
            'phone':'',
            'mail':'something@example.com',
            'address':'Caracas'
        }, follow_redirects=True)
        assert res.status_code == 200
        assert res.request.path == '/clients/addClient'
        with self.app.app_context():
            assert get_db().execute("select * from clients where dni = 'V-1111111'",).fetchone() is None

    def test_rootCreateClientSameDni(self):
        print("rootCreateClientSameDni\n\n")
        self.test_rootCreateClient()
        with self.app.app_context():
            assert get_db().execute("select * from clients",).fetchone() is not None
        res = self.client.post('/clients/addClient', data={
            'dni':'V-1111111',
            'firstname':'Juan',
            'secondname':'Arreia',
            'birthday':'1970-03-31',
            'phone':'2313-1231323',
            'mail':'something@example.com',
            'address':'Caracas'
        }, follow_redirects=True)
        assert res.status_code == 200
        assert res.request.path == '/clients/addClient'
        html = res.get_data(as_text=True)
        assert f'Client already registered' in html
        

    def test_rootModifyClient(self):
        print("rootModifyClient\n\n")
        self.test_rootCreateClient()
        with self.app.app_context():
            db = get_db()
            u1 = db.execute("select * from clients where dni = 'V-1111111'",).fetchone()
            assert u1 is not None
            assert u1['dni'] == 'V-1111111'
            old_dni = u1['dni']
        with self.client.session_transaction() as session:
            session['client_id'] = '1'
        res = self.client.post('/clients/modifyClient', data={
            'dni':'V-1111113',
            'firstname':'jorge',
            'secondname':'correia',
            'phone':'0414-1234032',
            'mail':'something@example.com',
            'address':'Caracas'
        }, follow_redirects=True)
        assert res.status_code == 200
        assert res.request.path == '/clients'
        with self.app.app_context():    
            db = get_db()
            u2 = db.execute("select * from clients where id = 1").fetchone()
            assert u2 is not None
            assert u2['dni'] != old_dni
            assert u2['dni'] == 'V-1111113'

    def test_rootDeleteClient(self):
        print("rootDeleteClient\n\n")
        self.test_rootCreateClient()
        with self.app.app_context():
            db = get_db()
            u1 = db.execute("select * from clients where dni = 'V-1111111'",).fetchone()
            assert u1 is not None
        res = self.client.post('/clients', data={
            'delete':'1'
        }, follow_redirects=True)
        assert res.status_code == 200
        assert res.request.path == '/clients'
        with self.app.app_context():    
            db = get_db()
            u2 = db.execute("select * from clients where id = 1").fetchone()
            assert u2 is None

    def test_rootAddCarToClient(self):
        print("rootAddCarToClient\n\n")
        self.test_rootCreateClient()
        with self.app.app_context():
            db = get_db()
            u1 = db.execute("select * from cars where ownerId = 1",).fetchone()
            assert u1 is None
        with self.client.session_transaction() as session:
            session['client_id'] = '1'
        res = self.client.post('/clients/addCar', data={
            'plaque':'A1E231',
            'brand':'Toyota',
            'model':'Corolla',
            'year':'2020',
            'bodywork':'JAKF9031ALFOF2231',
            'motor':'JAKF9032313AFFG31',
            'color':'white',
            'problem':'Bad lights'
        }, follow_redirects=True)
        assert res.status_code == 200
        assert res.request.path == '/clients/details'
        with self.app.app_context():    
            db = get_db()
            u2 = db.execute("select * from cars where ownerId = 1 and plaque = 'A1E231'").fetchone()
            assert u2 is not None

    def test_rootModifyCarOfClient(self):
        print("rootModifyCarOfClient\n\n")
        self.test_rootAddCarToClient()
        with self.app.app_context():
            db = get_db()
            u1 = db.execute("select * from cars where ownerId = 1 and plaque = 'A1E231'",).fetchone()
            assert u1 is not None
            old_problem = u1['problem']
        with self.client.session_transaction() as session:
            session['client_id'] = '1'
            session['car_id'] = '1'
        res = self.client.post('/clients/modifyCar', data={
            'plaque':'A1E231',
            'brand':'Toyota',
            'model':'Corolla',
            'year':'2020',
            'bodywork':'JAKF9031ALFOF2231',
            'motor':'JAKF9032313AFFG31',
            'color':'white',
            'problem':'Nothing'
        }, follow_redirects=True)
        assert res.status_code == 200
        assert res.request.path == '/clients/details'
        with self.app.app_context():    
            db = get_db()
            u2 = db.execute("select * from cars where ownerId = 1 and plaque = 'A1E231'").fetchone()
            assert u2 is not None and u2['problem'] != old_problem

    def test_rootDeleteCarFromClient(self):
        print("rootDeleteCarFromClient\n\n")
        self.test_rootAddCarToClient()
        with self.app.app_context():    
            db = get_db()
            u1 = db.execute("select * from cars where ownerId = 1").fetchone()
            assert u1 is not None
        with self.client.session_transaction() as session:
            session['client_id'] = '1'
        res = self.client.post('/clients/details', data={
            'delete':'1'
        }, follow_redirects=True)
        assert res.status_code == 200
        assert res.request.path == '/clients/details'
        with self.app.app_context():    
            db = get_db()
            u2 = db.execute("select * from cars where ownerId = 1").fetchone()
            assert u2 is None
    '''