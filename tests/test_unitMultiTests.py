from datetime import datetime
import sys
sys.path.append('../')
from . import UnitTestClass
from http.cookies import SimpleCookie
from flask import session
from .test_unitLoginTests import *
from .test_unitDepartmentTests import *
from .test_unitClientTests import *
from .test_unitProjectTests import *

class unitMultiTests(UnitTestClass): 

    def test_rootAddCarToProyect(self):
        print("rootAddCarToProyect\n\n")
        # Create Client
        unitClientTests.test_rootCreateClient(self)
        # Add Car
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

        # Add Department
        unitDepartmentTests.test_rootCreateDepartment(self)
        print("rootAddProblemToDepartment\n\n")
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

        # Create Proyect
        # 
        print("rootEnableProject\n\n")
        unitProjectTests.test_rootCreateProject(self)
        with self.app.app_context():
            db = get_db()
            assert db.execute("select statusId from proyect where id = 1").fetchone()[0] == 2

        res = self.client.post('/root/proyects', data={
            'enable-proyect':'1',
        }, follow_redirects=True)
        assert res.status_code == 200
        with self.app.app_context():
            db = get_db()
            assert db.execute("select statusId from proyect where id = 1").fetchone()[0] == 1
        assert res.status_code == 200
        assert res.request.path == '/root/proyects' 

        # Create Manager
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
         

        # Add Client to proyect
        with self.app.app_context():
            assert get_db().execute("select * from proyectClients",).fetchone() is None
        with self.client.session_transaction() as session:
            session['proyId'] = '1'
        res = self.client.post('/root/addClient', data={
            'plaque':'1',
            'manager':'2',
            'problem':'1',
            'solution':'AAA',
            'total':'123',
            'obser':'None',
        }, follow_redirects=True)
        assert res.status_code == 200
        assert res.request.path == '/root/proyect/detail'
        with self.app.app_context():
            assert get_db().execute("select * from proyectClients",).fetchone() is not None
    
    def test_rootModifyProyectDetailProblem(self):
        print("rootModifyProyectDetail\n\n")
        self.test_rootAddCarToProyect()
        with self.app.app_context():
            p1 = get_db().execute("select * from proyectClients where id = 1",).fetchone()
            assert p1 is not None
            oldSolution = p1['solution']
        with self.client.session_transaction() as session:
            session['editProy'] = '1'
        res = self.client.post('/root/modifyDetail', data={
            'solution':'AAAAAA',
            'total':'123',
            'obser':'None',
        }, follow_redirects=True)
        assert res.status_code == 200
        assert res.request.path == '/root/proyect/detail'
        with self.app.app_context():
            p2 = get_db().execute("select * from proyectClients where id = 1",).fetchone()
            assert p2 is not None
            assert p2['solution'] != oldSolution


    def test_rootDeleteProyectDetailProblem(self):
        print("rootDeelteProyectDetail\n\n")
        print("rootAddCarToProyect\n\n")
        # Create Client
        unitClientTests.test_rootCreateClient(self)
        # Add Car
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

        # Add Department
        unitDepartmentTests.test_rootCreateDepartment(self)
        print("rootAddProblemToDepartment\n\n")
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

        # Create Proyect
        # 
        print("rootEnableProject\n\n")
        unitProjectTests.test_rootCreateProject(self)
        with self.app.app_context():
            db = get_db()
            assert db.execute("select statusId from proyect where id = 1").fetchone()[0] == 2

        res = self.client.post('/root/proyects', data={
            'enable-proyect':'1',
        }, follow_redirects=True)
        assert res.status_code == 200
        with self.app.app_context():
            db = get_db()
            assert db.execute("select statusId from proyect where id = 1").fetchone()[0] == 1
        assert res.status_code == 200
        assert res.request.path == '/root/proyects' 

        # Create Manager
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
         

        # Add Client to proyect
        with self.app.app_context():
            assert get_db().execute("select * from proyectClients",).fetchone() is None
        with self.client.session_transaction() as session:
            session['proyId'] = '1'
        res = self.client.post('/root/addClient', data={
            'plaque':'1',
            'manager':'2',
            'problem':'1',
            'solution':'AAA',
            'total':'123',
            'obser':'None',
        }, follow_redirects=True)
        assert res.status_code == 200
        assert res.request.path == '/root/proyect/detail'

        with self.app.app_context():
            assert get_db().execute("select * from proyectClients",).fetchone() is not None
        
        with self.app.app_context():
            p1 = get_db().execute("select * from proyectClients where id = 1",).fetchone()
            assert p1 is not None
        
        with self.client.session_transaction() as session:
            session['proyId'] = '1'
        
        res = self.client.post('/root/proyect/detail', data={
            'delete':'1'
        }, follow_redirects=True)
        
        assert res.status_code == 200
        
        assert res.request.path == '/root/proyect/detail'
        
        with self.app.app_context():
            p2 = get_db().execute("select * from proyectClients where id = 1",).fetchone()
            assert p2 is None