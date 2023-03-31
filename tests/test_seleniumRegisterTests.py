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

class seleniumRegisterTests(SeleniumClass):
    
    def test_registerNonRegisteredUser(self):
        driver = self.driver
        driver.get("http://localhost:5000/auth/register")
        assert "Register" in driver.title
        passwd = driver.find_element(By.NAME, "password")
        passwd.clear()
        passwd.send_keys("joje")
        user = driver.find_element(By.NAME, "username")
        user.clear()
        user.send_keys("joje")
        firstname = driver.find_element(By.NAME, "firstname")
        firstname.send_keys("joje")
        secondname = driver.find_element(By.NAME, "secondname")
        secondname.send_keys("joje")
        user.send_keys(Keys.RETURN)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/auth/login"))
        actualUrl = "http://localhost:5000/auth/login"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)

    def test_registerAlreadyRegisteredUser(self):
        self.test_registerNonRegisteredUser()
        driver = self.driver
        driver.get("http://localhost:5000/auth/register")
        assert "Register" in driver.title
        passwd = driver.find_element(By.NAME, "password")
        passwd.clear()
        passwd.send_keys("joje")
        user = driver.find_element(By.NAME, "username")
        user.clear()
        user.send_keys("joje")
        firstname = driver.find_element(By.NAME, "firstname")
        firstname.send_keys("joje")
        secondname = driver.find_element(By.NAME, "secondname")
        secondname.send_keys("joje")
        user.send_keys(Keys.RETURN)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/auth/register"))
        actualUrl = "http://localhost:5000/auth/register"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'section')
        elements = element.find_elements(By.TAG_NAME, 'div')
        for e in elements:
            if (e.text == "User 'joje' is already registered."):
                self.assertEqual(e.text,"User 'joje' is already registered.")

    def test_registerRoot(self):
        driver = self.driver
        driver.get("http://localhost:5000/auth/register")
        assert "Register" in driver.title
        passwd = driver.find_element(By.NAME, "password")
        passwd.clear()
        passwd.send_keys("root")
        user = driver.find_element(By.NAME, "username")
        user.clear()
        user.send_keys("root")
        firstname = driver.find_element(By.NAME, "firstname")
        firstname.send_keys("dsfs")
        secondname = driver.find_element(By.NAME, "secondname")
        secondname.send_keys("dsfsd")
        user.send_keys(Keys.RETURN)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/auth/register"))
        actualUrl = "http://localhost:5000/auth/register"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'section')
        elements = element.find_elements(By.TAG_NAME, 'div')
        for e in elements:
            if (e.text == "User 'root' is already registered."):
                self.assertEqual(e.text,"User 'root' is already registered.")

