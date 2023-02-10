import unittest
from flask import g, session
from app import create_app
from app.db import init_db_command,get_db,close_db
import click
class BaseTestsClass(unittest.TestCase):

    def setUp(self) -> None:
        self.app = create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            try: 
                init_db_command()
            except:
                pass

    def tearDown(self):
        with self.app.app_context():
            close_db()