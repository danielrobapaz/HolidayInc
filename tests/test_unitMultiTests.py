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
from .test_unitMetricTests import *

class unitMultiTests(UnitTestClass): 

    def test_rootAddCarToProyect(self):
        #print("rootAddCarToProyect\n\n")
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
        #print("rootAddProblemToDepartment\n\n")
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
        #print("rootEnableProject\n\n")
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
        #print("add manager")
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
            session['currProy'] = '1'
        res = self.client.post('/root/addClient', data={
            'plaque':'1',
            'manager':'2',
            'problem':'1',
            'solution':'AAA',
            'obser':'None'
        }, follow_redirects=True)
        assert res.status_code == 200
        assert res.request.path == '/root/proyect/detail'
        with self.app.app_context():
            assert get_db().execute("select * from proyectClients",).fetchone() is not None
    
    def test_rootModifyProyectDetailProblem(self):
        #print("rootModifyProyectDetail\n\n")
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
        #print("rootDeelteProyectDetail\n\n")
        #print("rootAddCarToProyect\n\n")
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
        #print("rootAddProblemToDepartment\n\n")
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
        #print("rootEnableProject\n\n")
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
            session['currProy'] = '1'
        res = self.client.post('/root/addClient', data={
            'plaque':'1',
            'manager':'2',
            'problem':'1',
            'solution':'AAA',
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

    def test_rootActionCreateComplete(self):
        ##print("rootCreateUser\n\n")
        self.test_rootAddCarToProyect()
        unitMetricTests.test_rootMetricCreate(self)        
        with self.app.app_context():
            assert get_db().execute("select * from actionPlan where id = 1 and action = 'testAction'").fetchone() is None
        with self.client.session_transaction() as session:
            session['currProy'] = 1
            session['actionProy'] = 1
        res = self.client.post('/plan/create', data={
            'action':'testAction',
            'activity': 'testactivity',
            'starting-date':'2023-01-30',
            'end-date':'2023-02-01',    
            'resp':'2',
            'workers': '2',
            'costHour': '20',
            'category': 'Material',
            'supplie': 'Cinta',
            'metric': '1',
            'quantity': '2',
            'costSupplie': '24'
        }, follow_redirects=True)
        assert res.status_code == 200
        assert res.request.path == '/plan'
        with self.app.app_context():
            assert get_db().execute("select * from actionPlan where id = 1 and action = 'testAction'").fetchone() is not None
        res = self.client.get('/plan/supplie', follow_redirects=True)
        assert res.request.path == '/plan/supplie'
        html = res.get_data(as_text=True)
        assert f'40' in html
        res = self.client.get('/plan', follow_redirects=True)
        assert res.request.path == '/plan'
        html = res.get_data(as_text=True)
        assert f'24' in html and f'520' in html
        res = self.client.get('/plan/humanTalent', follow_redirects=True)
        assert res.request.path == '/plan/humanTalent'
        html = res.get_data(as_text=True)
        assert f'24' in html and f'480' in html

    def test_rootActionCreateOnlyHuman(self):
        ##print("rootCreateUser\n\n")
        self.test_rootAddCarToProyect()
        unitMetricTests.test_rootMetricCreate(self)        
        with self.app.app_context():
            assert get_db().execute("select * from actionPlan where id = 1 and action = 'testAction'").fetchone() is None
        with self.client.session_transaction() as session:
            session['currProy'] = 1
            session['actionProy'] = 1
        res = self.client.post('/plan/create', data={
            'action':'testAction',
            'activity': 'testactivity',
            'starting-date':'2023-01-30',
            'end-date':'2023-02-01',    
            'resp':'2',
            'workers': '2',
            'costHour': '20',
            'supplie': '',
            'quantity': '',
            'costSupplie': ''
        }, follow_redirects=True)
        assert res.status_code == 200
        assert res.request.path == '/plan'
        with self.app.app_context():
            assert get_db().execute("select * from actionPlan where id = 1 and action = 'testAction'").fetchone() is not None
        res = self.client.get('/plan/supplie', follow_redirects=True)
        assert res.request.path == '/plan/supplie'
        html = res.get_data(as_text=True)
        assert f'40' not in html
        res = self.client.get('/plan', follow_redirects=True)
        assert res.request.path == '/plan'
        html = res.get_data(as_text=True)
        assert f'24' in html and f'480' in html
        res = self.client.get('/plan/humanTalent', follow_redirects=True)
        assert res.request.path == '/plan/humanTalent'
        html = res.get_data(as_text=True)
        assert f'24' in html and f'480' in html

    def test_rootActionEdit(self):
        #print("rootCreateUser\n\n")
        self.test_rootActionCreateComplete()
        with self.app.app_context():
            assert get_db().execute("select * from actionPlan where action = 'testAction' and  end = '2023-02-01'").fetchone() is not None
        with self.client.session_transaction() as session:
            session['currProy'] = 1
            session['editAction'] = 1
        res = self.client.post('/plan/edit', data={
            'action':'testAction',
            'activity': 'testactivity',
            'starting-date':'2023-01-30',
            'end-date':'2023-02-05',    
            'workers': '2',
            'costHour': '20',
            'supplie': 'Cinta',
            'quantity': '2',
            'costSupplie': '24'
        }, follow_redirects=True)
        assert res.status_code == 200
        assert res.request.path == '/plan'
        with self.app.app_context():
            assert get_db().execute("select * from actionPlan where action = 'testAction' and  end = '2023-02-05'").fetchone() is not None
        res = self.client.get('/plan/supplie', follow_redirects=True)
        assert res.request.path == '/plan/supplie'
        html = res.get_data(as_text=True)
        assert f'48' in html and f'2' in html
        res = self.client.get('/plan', follow_redirects=True)
        assert res.request.path == '/plan'
        html = res.get_data(as_text=True)
        assert f'56' in html and f'1168' in html
        res = self.client.get('/plan/humanTalent', follow_redirects=True)
        assert res.request.path == '/plan/humanTalent'
        html = res.get_data(as_text=True)
        assert f'56' in html and f'1120' in html

    def test_rootActionDelete(self):
        print("Delete action")
        self.test_rootActionCreateComplete()
        with self.app.app_context():
            assert get_db().execute("select * from actionPlan where action = 'testAction' and  end = '2023-02-01'").fetchone() is not None
        res = self.client.post('/plan', data={
            'delete':'1',
        }, follow_redirects=True)
        assert res.status_code == 200
        assert res.request.path == '/plan'
        with self.app.app_context():
            assert get_db().execute("select * from actionPlan where action = 'testAction'").fetchone() is None
        res = self.client.get('/plan/supplie', follow_redirects=True)
        assert res.request.path == '/plan/supplie'
        html = res.get_data(as_text=True)
        assert not (f'40' in html and f'2' in html)
        res = self.client.get('/plan', follow_redirects=True)
        assert res.request.path == '/plan'
        html = res.get_data(as_text=True)
        assert f'56' not in html and f'1160' not in html
        res = self.client.get('/plan/humanTalent', follow_redirects=True)
        assert res.request.path == '/plan/humanTalent'
        html = res.get_data(as_text=True)
        assert f'56' not in html and f'1120' not in html


    def test_rootActionCreateDateOutOfRange(self):
        ##print("rootCreateUser\n\n")
        self.test_rootAddCarToProyect()
        unitMetricTests.test_rootMetricCreate(self)        
        with self.app.app_context():
            assert get_db().execute("select * from actionPlan where id = 1 and action = 'testAction'").fetchone() is None
        with self.client.session_transaction() as session:
            session['currProy'] = 1
            session['actionProy'] = 1
        res = self.client.post('/plan/create', data={
            'action':'testAction',
            'activity': 'testactivity',
            'starting-date':'2023-04-30',
            'end-date':'2023-05-01',    
            'resp':'2',
            'workers': '2',
            'costHour': '20',
            'category': 'Material',
            'supplie': 'Cinta',
            'metric': '1',
            'quantity': '2',
            'costSupplie': '24'
        }, follow_redirects=True)
        assert res.status_code == 200
        assert res.request.path == '/plan/create'
        html = res.get_data(as_text=True)
        assert f'Invalid dates, out of proyect range' in html
        with self.app.app_context():
            assert get_db().execute("select * from actionPlan where id = 1 and action = 'testAction'").fetchone() is None
        
    
    def test_rootActionEditDateOutOfRange(self):
        #print("rootCreateUser\n\n")
        self.test_rootActionCreateComplete()
        with self.app.app_context():
            assert get_db().execute("select * from actionPlan where action = 'testAction' and  end = '2023-02-01'").fetchone() is not None
        with self.client.session_transaction() as session:
            session['currProy'] = 1
            session['editAction'] = 1
        res = self.client.post('/plan/edit', data={
            'action':'testAction',
            'activity': 'testactivity',
            'starting-date':'2023-01-30',
            'end-date':'2023-03-05',    
            'resp':'2',
            'workers': '2',
            'costHour': '20',
            'category': 'Material',
            'supplie': 'Cinta',
            'metric': '1',
            'quantity': '2',
            'costSupplie': '24'
        }, follow_redirects=True)
        assert res.status_code == 200
        assert res.request.path == '/plan/edit'
        with self.app.app_context():
            assert get_db().execute("select * from actionPlan where action = 'testAction' and  end = '2023-02-05'").fetchone() is None


    def test_rootActionDeleteMetric(self):
        self.test_rootActionCreateComplete()
        with self.app.app_context():
            assert get_db().execute("select * from actionPlan where action = 'testAction' and  end = '2023-02-01'").fetchone() is not None
        res = self.client.post('/metrics/metrics', data = {
            'delete':1,
        }, follow_redirects=True)
        assert res.status_code == 200
        assert res.request.path == '/metrics/metrics'
        with self.app.app_context():
            assert get_db().execute("select * from metricsUnit where dimension = 5 and unit = 'Meters'").fetchone() is None
        with self.app.app_context():
            assert get_db().execute("select * from actionPlan where action = 'testAction' and  totalSupplie = 0").fetchone() is not None
        res = self.client.get('/plan/supplie', follow_redirects=True)
        assert res.request.path == '/plan/supplie'
        html = res.get_data(as_text=True)
        assert not (f'40' in html and f'2' in html)

