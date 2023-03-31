from datetime import datetime
from . import SeleniumClass
from app.db import get_db
#from http.cookies import SimpleCookie
from flask import session
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from .test_seleniumRegisterTests import *
from .test_seleniumProjectTests import *

class seleniumUserTests(SeleniumClass):

    def test_rootRejectUser(self):
        seleniumRegisterTests.test_registerNonRegisteredUser(self)
        self.driver.get("http://localhost:5000/auth/login")
        assert "Log In" in self.driver.title
        passwd = self.driver.find_element(By.ID, "password")
        passwd.clear()
        passwd.send_keys("root")
        user = self.driver.find_element(By.ID, "username")
        user.clear()
        user.send_keys("root")
        user.send_keys(Keys.RETURN)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/user/root"))
        actualUrl = "http://localhost:5000/user/root"
        expectedUrl= self.driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        user_button = self.driver.find_element(By.ID, "user")
        user_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/root/users"))
        actualUrl = "http://localhost:5000/root/users"
        expectedUrl= self.driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        reject_button = self.driver.find_element(By.NAME, "reject")
        reject_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/root/users"))
        actualUrl = "http://localhost:5000/root/users"
        expectedUrl= self.driver.current_url
        self.assertEqual(expectedUrl,actualUrl)



    def test_rootAproveUser(self):
         seleniumRegisterTests.test_registerNonRegisteredUser(self)
         seleniumProjectTests.test_RootCreateProyect(self)
         self.driver.get("http://localhost:5000/auth/login")
         assert "Log In" in self.driver.title
         passwd = self.driver.find_element(By.ID, "password")
         passwd.clear()
         passwd.send_keys("root")
         user = self.driver.find_element(By.ID, "username")
         user.clear()
         user.send_keys("root")
         user.send_keys(Keys.RETURN)
         wait = WebDriverWait(self.driver, 10)
         wait.until(EC.url_to_be("http://localhost:5000/user/root"))
         actualUrl = "http://localhost:5000/user/root"
         expectedUrl= self.driver.current_url
         self.assertEqual(expectedUrl,actualUrl)
         user_button = self.driver.find_element(By.ID, "user")
         user_button.click()
         wait.until(EC.url_to_be("http://localhost:5000/root/users"))
         actualUrl = "http://localhost:5000/root/users"
         expectedUrl= self.driver.current_url
         self.assertEqual(expectedUrl,actualUrl)
         reject_button = self.driver.find_element(By.NAME, "aprove")
         reject_button.click()
         wait.until(EC.url_to_be("http://localhost:5000/root/aproveUser"))
         actualUrl = "http://localhost:5000/root/aproveUser"
         expectedUrl= self.driver.current_url
         self.assertEqual(expectedUrl,actualUrl)
         roleSelect = Select(self.driver.find_element(By.NAME, "role"))
         roleSelect.select_by_visible_text("Gerente de operaciones")
         proyectSelect = Select(self.driver.find_element(By.NAME, "proyect"))
         proyectSelect.select_by_visible_text("testproyect")
         aproveButton = self.driver.find_element(By.NAME, "aprove")
         aproveButton.click()
         wait.until(EC.url_to_be("http://localhost:5000/user/root"))
         actualUrl = "http://localhost:5000/user/root"
         expectedUrl= self.driver.current_url
         self.assertEqual(expectedUrl,actualUrl)