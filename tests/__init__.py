import unittest
from flask import g, session
from app import create_app
from app.db import init_db_command,get_db,close_db
#import click
from selenium import webdriver
from flask import session
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from . import page
class BaseTestsClass(unittest.TestCase):

    def setUp(self) -> None:
        self.app = create_app()
        self.client = self.app.test_client()
        self.driver = webdriver.Firefox()
        with self.app.app_context():
            try: 
                init_db_command()
            except:
                pass

   
    def tearDown(self):
        with self.app.app_context():
            close_db()
        self.driver.close()    