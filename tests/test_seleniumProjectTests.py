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

class seleniumProjectTests(SeleniumClass):
    
    def test_RootCreateProyect(self):
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
        user_button = self.driver.find_element(By.ID, "proyect")
        user_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/root/proyects"))
        actualUrl = "http://localhost:5000/root/proyects"
        expectedUrl= self.driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        create_proyect_button = self.driver.find_element(By.NAME, "create-proyect")
        create_proyect_button.click()
        proyect_description = self.driver.find_element(By.ID, "description")
        proyect_description.send_keys("testproyect")
        proyect_starting_date = self.driver.find_element(By.ID, "starting-date")
        proyect_starting_date.click()
        proyect_starting_date.send_keys("2023-03-10")
        proyect_end_date = self.driver.find_element(By.ID, "end-date")
        proyect_end_date.click()
        proyect_end_date.send_keys("2023-03-15")
        proyect_description.send_keys(Keys.RETURN)
        wait.until(EC.url_to_be("http://localhost:5000/root/proyects"))
        actualUrl = "http://localhost:5000/root/proyects"
        expectedUrl= self.driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
