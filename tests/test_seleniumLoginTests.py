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
from .test_seleniumRegisterTests import registerTests

class seleniumLoginTests(SeleniumClass):
    
    def test_LoginRoot(self):
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

    def test_loginRegisteredNonAuthorizedUser(self):
        registerTests.test_registerNonRegisteredUser(self)
        self.driver.get("http://localhost:5000/auth/login")
        assert "Log In" in self.driver.title
        passwd = self.driver.find_element(By.ID, "password")
        passwd.clear()
        passwd.send_keys("joje")
        user = self.driver.find_element(By.ID, "username")
        user.clear()
        user.send_keys("joje")
        user.send_keys(Keys.RETURN)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/auth/login"))
        actualUrl = "http://localhost:5000/auth/login"
        expectedUrl= self.driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = self.driver.find_element(By.TAG_NAME, 'section')
        elements = element.find_elements(By.TAG_NAME, 'div')
        for e in elements:
            if (e.text == "User 'joje' needs autentication from admin."):
                self.assertEqual(e.text,"User 'joje' needs autentication from admin.")

    def test_loginNonRegisteredUser(self):
        driver = self.driver
        driver.get("http://localhost:5000/auth/login")
        assert "Log In" in driver.title
        passwd = driver.find_element(By.ID, "password")
        passwd.clear()
        passwd.send_keys("joje")
        user = driver.find_element(By.ID, "username")
        user.clear()
        user.send_keys("joje")
        user.send_keys(Keys.RETURN)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/auth/login"))
        actualUrl = "http://localhost:5000/auth/login"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'section')
        elements = element.find_elements(By.TAG_NAME, 'div')
        for e in elements:
            if (e.text == "User doesn't exist."):
                self.assertEqual(e.text,"User doesn't exist.")
    
    def test_loginIncorrectPassword(self):
        driver = self.driver
        driver.get("http://localhost:5000/auth/login")
        assert "Log In" in driver.title
        passwd = driver.find_element(By.ID, "password")
        passwd.clear()
        passwd.send_keys("root")
        user = driver.find_element(By.ID, "username")
        user.clear()
        user.send_keys("joje")
        user.send_keys(Keys.RETURN)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/auth/login"))
        actualUrl = "http://localhost:5000/auth/login"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'section')
        elements = element.find_elements(By.TAG_NAME, 'div')
        for e in elements:
            if (e.text == "Incorrect password."):
                self.assertEqual(e.text,"Incorrect password.")
        
   