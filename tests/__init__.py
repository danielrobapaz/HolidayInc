import unittest
from flask import g, session
from app import create_app
from app.db import init_db,get_db,close_db

class BaseTestsClass(unittest.TestCase):

    def setUp(self) -> None:
        self.app = create_app()
        self.client = self.app.test_client()

        with self.app.app_context():
            init_db()
            get_db()

    def tearDown(self):
        with self.app.app_context():
            close_db()