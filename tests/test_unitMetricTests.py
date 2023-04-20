from datetime import datetime
import sys
sys.path.append('../')
from . import UnitTestClass
from http.cookies import SimpleCookie
from flask import session
from .test_unitProjectTests import *
from .test_unitLoginTests import *
from .test_unitRegisterTests import *

class unitMetricTests(UnitTestClass): 

    def test_rootMetricCreate(self):
        ##print("rootCreateUser\n\n")
        unitLoginTests.test_loginRoot(self)
        res = self.client.post('/metrics/metrics', data={
            'create':' ',
            'metric':'meters',
            'dim':'5'            
        }, follow_redirects=True)
        assert res.status_code == 200
        assert res.request.path == '/metrics/metrics'
        with self.app.app_context():
            assert get_db().execute("select * from metricsUnit where dimension = 5 and unit = 'Meters'").fetchone() is not None

    def test_rootMetricEdit(self):
        self.test_rootMetricCreate()
        with self.app.app_context():
            assert get_db().execute("select * from metricsUnit where dimension = 5 and unit = 'Meters'").fetchone() is not None
        with self.client.session_transaction() as session:
            session['editId'] = '1'
        res = self.client.post('/metrics/editMetric', data = {
            'dim':'10',
            'unit':'Meters'
        }, follow_redirects=True)
        assert res.status_code == 200
        assert res.request.path == '/metrics/metrics'
        with self.app.app_context():
            assert get_db().execute("select * from metricsUnit where dimension = 10 and unit = 'Meters'").fetchone() is not None

    def test_rootMetricDelete(self):
        self.test_rootMetricCreate()
        with self.app.app_context():
            assert get_db().execute("select * from metricsUnit where dimension = 5 and unit = 'Meters'").fetchone() is not None
        res = self.client.post('/metrics/metrics', data = {
            'delete':1,
        }, follow_redirects=True)
        assert res.status_code == 200
        assert res.request.path == '/metrics/metrics'
        with self.app.app_context():
            assert get_db().execute("select * from metricsUnit where dimension = 5 and unit = 'Meters'").fetchone() is None