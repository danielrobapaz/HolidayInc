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

    def test_RootCreateProyectStartDateAfterEndDate(self):
        driver = self.driver
        driver.get("http://localhost:5000/auth/login")
        assert "Log In" in driver.title
        passwd = driver.find_element(By.ID, "password")
        passwd.clear()
        passwd.send_keys("root")
        user = driver.find_element(By.ID, "username")
        user.clear()
        user.send_keys("root")
        user.send_keys(Keys.RETURN)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/user/root"))
        actualUrl = "http://localhost:5000/user/root"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        user_button = driver.find_element(By.ID, "proyect")
        user_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/root/proyects"))
        actualUrl = "http://localhost:5000/root/proyects"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        create_proyect_button = driver.find_element(By.NAME, "create-proyect")
        create_proyect_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/root/proyect/createProyect"))
        actualUrl = "http://localhost:5000/root/proyect/createProyect"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        proyect_description = driver.find_element(By.ID, "description")
        proyect_description.send_keys("testproyect")
        proyect_starting_date = driver.find_element(By.ID, "starting-date")
        proyect_starting_date.click()
        proyect_starting_date.send_keys("2023-03-20")
        proyect_end_date = driver.find_element(By.ID, "end-date")
        proyect_end_date.click()
        proyect_end_date.send_keys("2023-03-10")
        proyect_description.send_keys(Keys.RETURN)
        wait.until(EC.url_to_be("http://localhost:5000/root/proyect/createProyect"))
        actualUrl = "http://localhost:5000/root/proyect/createProyect"
        driver.implicitly_wait(30)
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'section')
        elements = element.find_elements(By.TAG_NAME, 'div')
        for e in elements:
            if (e.text == "The proyect must end after it begins"):
                self.assertEqual(e.text,"The proyect must end after it begins") 

    def test_RootCreateProyectEmptyDescription(self):
        driver = self.driver
        driver.get("http://localhost:5000/auth/login")
        assert "Log In" in driver.title
        passwd = driver.find_element(By.ID, "password")
        passwd.clear()
        passwd.send_keys("root")
        user = driver.find_element(By.ID, "username")
        user.clear()
        user.send_keys("root")
        user.send_keys(Keys.RETURN)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/user/root"))
        actualUrl = "http://localhost:5000/user/root"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        user_button = driver.find_element(By.ID, "proyect")
        user_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/root/proyects"))
        actualUrl = "http://localhost:5000/root/proyects"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        create_proyect_button = driver.find_element(By.NAME, "create-proyect")
        create_proyect_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/root/proyect/createProyect"))
        actualUrl = "http://localhost:5000/root/proyect/createProyect"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        proyect_description = driver.find_element(By.ID, "description")
        proyect_starting_date = driver.find_element(By.ID, "starting-date")
        proyect_starting_date.click()
        proyect_starting_date.send_keys("2023-03-20")
        proyect_end_date = driver.find_element(By.ID, "end-date")
        proyect_end_date.click()
        proyect_end_date.send_keys("2023-03-10")
        proyect_description.send_keys(Keys.RETURN)
        wait.until(EC.url_to_be("http://localhost:5000/root/proyect/createProyect"))
        actualUrl = "http://localhost:5000/root/proyect/createProyect"
        if (proyect_description.get_attribute("value") == None):
            self.assertEqual(proyect_description.get_attribute("value"),None)

    def test_RootEnableProyect(self):
        self.test_RootCreateProyect()
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        actualUrl = "http://localhost:5000/root/proyects"
        expectedUrl= self.driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'tr')
        elements = element.find_elements(By.TAG_NAME, 'td')
        for e in elements:
            if (e.text == "Closed"):
                self.assertEqual(e.text,"Closed")
        enable_proyect_button = self.driver.find_element(By.NAME, "enable-proyect")
        enable_proyect_button.click()
        driver.implicitly_wait(1)
        wait.until(EC.url_to_be("http://localhost:5000/root/proyects"))
        actualUrl = "http://localhost:5000/root/proyects"
        expectedUrl= self.driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'tr')
        elements = element.find_elements(By.TAG_NAME, 'td')
        for e in elements:
            if (e.text == "Enabled"):
                self.assertEqual(e.text,"Enabled")


    def test_RootCloseProyect(self):
        self.test_RootEnableProyect()
        driver = self.driver
        wait = WebDriverWait(driver, 5)
        actualUrl = "http://localhost:5000/root/proyects"
        expectedUrl= self.driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'tr')
        elements = element.find_elements(By.TAG_NAME, 'td')
        for e in elements:
            if (e.text == "Enabled"):
                self.assertEqual(e.text,"Enabled")
        enable_proyect_button = self.driver.find_element(By.NAME, "close-proyect")
        enable_proyect_button.click()
        driver.implicitly_wait(1)
        wait.until(EC.url_to_be("http://localhost:5000/root/proyects"))
        actualUrl = "http://localhost:5000/root/proyects"
        expectedUrl= self.driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'tr')
        elements = element.find_elements(By.TAG_NAME, 'td')
        for e in elements:
            if (e.text == "Closed"):
                self.assertEqual(e.text,"Closed")


    def test_RootModifyProyectDate(self):
        self.test_RootCreateProyect()
        driver = self.driver
        wait = WebDriverWait(driver, 20)
        driver.implicitly_wait(1)
        actualUrl = "http://localhost:5000/root/proyects"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        modify_proyect_button = driver.find_element(By.NAME, "modify-proyect")
        modify_proyect_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/modifyProyect"))
        actualUrl = "http://localhost:5000/modifyProyect"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        change_dates_button = driver.find_element(By.NAME, "change-dates")
        change_dates_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/changeDatesProyect"))
        actualUrl = "http://localhost:5000/changeDatesProyect"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        proyect_starting_date = driver.find_element(By.NAME, "starting-date")
        proyect_starting_date.click()
        proyect_starting_date.send_keys("2023-03-15")
        proyect_end_date = driver.find_element(By.NAME, "end-date")
        proyect_end_date.click()
        proyect_end_date.send_keys("2023-03-30")
        proyect_button = driver.find_element(By.XPATH, "//input[@value='Create proyect']")
        proyect_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/root/proyects"))
        actualUrl = "http://localhost:5000/root/proyects"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)


    def test_RootModifyProyectDateStartDateAfterEndDate(self):
        self.test_RootCreateProyect()
        driver = self.driver
        wait = WebDriverWait(driver, 20)
        driver.implicitly_wait(1)
        actualUrl = "http://localhost:5000/root/proyects"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        modify_proyect_button = driver.find_element(By.NAME, "modify-proyect")
        modify_proyect_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/modifyProyect"))
        actualUrl = "http://localhost:5000/modifyProyect"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        change_dates_button = driver.find_element(By.NAME, "change-dates")
        change_dates_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/changeDatesProyect"))
        actualUrl = "http://localhost:5000/changeDatesProyect"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        proyect_starting_date = driver.find_element(By.NAME, "starting-date")
        proyect_starting_date.click()
        proyect_starting_date.send_keys("2023-04-15")
        proyect_end_date = driver.find_element(By.NAME, "end-date")
        proyect_end_date.click()
        proyect_end_date.send_keys("2023-03-30")
        proyect_button = driver.find_element(By.XPATH, "//input[@value='Create proyect']")
        proyect_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/changeDatesProyect"))
        actualUrl = "http://localhost:5000/changeDatesProyect"
        driver.implicitly_wait(30)
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'section')
        elements = element.find_elements(By.TAG_NAME, 'div')
        for e in elements:
            if (e.text == "The proyect must end after it begins"):
                self.assertEqual(e.text,"The proyect must end after it begins")

    def test_RootRemoveProyect(self):
        self.test_RootCreateProyect()
        driver = self.driver
        wait = WebDriverWait(driver, 20)
        driver.implicitly_wait(1)
        actualUrl = "http://localhost:5000/root/proyects"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        modify_proyect_button = driver.find_element(By.NAME, "modify-proyect")
        modify_proyect_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/modifyProyect"))
        actualUrl = "http://localhost:5000/modifyProyect"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        delete_button = driver.find_element(By.NAME, "delete")
        delete_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/root/proyects"))
        actualUrl = "http://localhost:5000/root/proyects"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        try:
            modify_proyect_button = driver.find_element(By.NAME, "modify-proyect")
        except:
            print("Proyect Deleted")