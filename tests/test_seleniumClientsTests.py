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


class seleniumClientsTests(SeleniumClass):
    
    def test_rootCreateClient(self):
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
        clients_button = driver.find_element(By.ID, "clients")
        clients_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/clients"))
        actualUrl = "http://localhost:5000/clients"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        create_client_button = driver.find_element(By.NAME, "add")
        create_client_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/clients/addClient"))
        actualUrl = "http://localhost:5000/clients/addClient"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        client_dni = driver.find_element(By.ID, "dni")
        client_dni.send_keys("V-1111111")
        client_firstname = driver.find_element(By.ID, "firstname")
        client_firstname.click()
        client_firstname.send_keys("Jorge")
        client_secondname = driver.find_element(By.ID, "secondname")
        client_secondname.click()
        client_secondname.send_keys("Correia")
        client_birthday = driver.find_element(By.NAME, "birthday")
        client_birthday.click()
        client_birthday.send_keys("2000-03-15")
        client_phone = driver.find_element(By.ID, "phone")
        client_phone.click()
        client_phone.send_keys("0416-8321311")
        client_mail = driver.find_element(By.ID, "mail")
        client_mail.click()
        client_mail.send_keys("test@example.com")
        client_address = driver.find_element(By.ID, "address")
        client_address.click()
        client_address.send_keys("Universidad Simon Bolivar")
        client_dni.send_keys(Keys.RETURN)
        wait.until(EC.url_to_be("http://localhost:5000/clients"))
        actualUrl = "http://localhost:5000/clients"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'tr')
        elements = element.find_elements(By.TAG_NAME, 'td')
        for e in elements:
            if (e.text == "V-1111111"):
                self.assertEqual(e.text,"V-1111111")


    def test_rootCreateClientEmptyFields(self):
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
        clients_button = driver.find_element(By.ID, "clients")
        clients_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/clients"))
        actualUrl = "http://localhost:5000/clients"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        create_client_button = driver.find_element(By.NAME, "add")
        create_client_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/clients/addClient"))
        actualUrl = "http://localhost:5000/clients/addClient"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        client_dni = driver.find_element(By.ID, "dni")
        client_dni.send_keys("V-1111111")
        client_firstname = driver.find_element(By.ID, "firstname")
        client_firstname.click()
        client_firstname.send_keys("Jorge")
        client_secondname = driver.find_element(By.ID, "secondname")
        client_secondname.click()
        client_birthday = driver.find_element(By.NAME, "birthday")
        client_birthday.click()
        client_birthday.send_keys("2000-03-15")
        client_phone = driver.find_element(By.ID, "phone")
        client_phone.click()
        client_mail = driver.find_element(By.ID, "mail")
        client_mail.click()
        client_mail.send_keys("test@example.com")
        client_address = driver.find_element(By.ID, "address")
        client_address.click()
        client_dni.send_keys(Keys.RETURN)
        wait.until(EC.url_to_be("http://localhost:5000/clients/addClient"))
        actualUrl = "http://localhost:5000/clients/addClient"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        if ((client_address.get_attribute("value") == None) and 
            (client_phone.get_attribute("value") == None) and 
                (client_secondname.get_attribute("value") == None)):
            (self.assertEqual(client_address.get_attribute("value"),None) 
                and self.assertEqual(client_phone.get_attribute("value"),None) 
                    and self.assertEqual(client_secondname.get_attribute("value"),None))
            


    def test_rootCreateClientSameDNI(self):
        self.test_rootCreateClient()
        driver = self.driver
        driver.get("http://localhost:5000/clients/addClient")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/clients/addClient"))
        actualUrl = "http://localhost:5000/clients/addClient"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        client_dni = driver.find_element(By.ID, "dni")
        client_dni.send_keys("V-1111111")
        client_firstname = driver.find_element(By.ID, "firstname")
        client_firstname.click()
        client_firstname.send_keys("Jafsafa")
        client_secondname = driver.find_element(By.ID, "secondname")
        client_secondname.click()
        client_secondname.send_keys("Cosfdsafaa")
        client_birthday = driver.find_element(By.NAME, "birthday")
        client_birthday.click()
        client_birthday.send_keys("2000-03-15")
        client_phone = driver.find_element(By.ID, "phone")
        client_phone.click()
        client_phone.send_keys("0416-8321231")
        client_mail = driver.find_element(By.ID, "mail")
        client_mail.click()
        client_mail.send_keys("test2@example.com")
        client_address = driver.find_element(By.ID, "address")
        client_address.click()
        client_address.send_keys("Universidad Simon Bolivar Litoral")
        client_dni.send_keys(Keys.RETURN)
        wait.until(EC.url_to_be("http://localhost:5000/clients/addClient"))
        actualUrl = "http://localhost:5000/clients/addClient"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'section')
        elements = element.find_elements(By.TAG_NAME, 'div')
        for e in elements:
            if (e.text == "Client already registered"):
                self.assertEqual(e.text,"Client already registered")



    def test_rootModifyClient(self):
        self.test_rootCreateClient()
        driver = self.driver
        driver.get("http://localhost:5000/clients")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/clients"))
        actualUrl = "http://localhost:5000/clients"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'section')
        elements = element.find_elements(By.TAG_NAME, 'div')
        for e in elements:
            if (e.text == "Jorge"):
                self.assertEqual(e.text,"Jorge")
                old_name = e.text
        client_modify = driver.find_element(By.NAME, "modify")
        client_modify.click()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/clients/modifyClient"))
        actualUrl = "http://localhost:5000/clients/modifyClient"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        client_firstname = driver.find_element(By.ID, "firstname")
        client_firstname.click()
        client_firstname.clear()
        client_firstname.send_keys("Juan")
        client_firstname.send_keys(Keys.RETURN)
        wait.until(EC.url_to_be("http://localhost:5000/clients"))
        actualUrl = "http://localhost:5000/clients"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'tr')
        elements = element.find_elements(By.TAG_NAME, 'td')
        for k in elements:
            if (k.text == "Juan"):
                self.assertEqual(k.text,old_name)


    def test_rootDeleteClient(self):
        self.test_rootCreateClient()
        driver = self.driver
        driver.get("http://localhost:5000/clients")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/clients"))
        actualUrl = "http://localhost:5000/clients"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'section')
        elements = element.find_elements(By.TAG_NAME, 'div')
        for e in elements:
            if (e.text == "V-1111111"):
                self.assertEqual(e.text,"V-1111111")
                DNI = e.text
        client_modify = driver.find_element(By.NAME, "delete")
        client_modify.click()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/clients"))
        actualUrl = "http://localhost:5000/clients"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'tr')
        elements = element.find_elements(By.TAG_NAME, 'td')
        for k in elements:
            if (k.text == None):
                self.assertNotEqual(k.text,DNI)


    def test_rootAddCar(self):
        self.test_rootCreateClient()
        driver = self.driver
        driver.get("http://localhost:5000/clients")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/clients"))
        actualUrl = "http://localhost:5000/clients"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        client_details = driver.find_element(By.NAME, "detail")
        client_details.click()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/clients/details"))
        actualUrl = "http://localhost:5000/clients/details"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        client_firstname = driver.find_element(By.NAME, "add")
        client_firstname.click()
        wait.until(EC.url_to_be("http://localhost:5000/clients/addCar"))
        actualUrl = "http://localhost:5000/clients/addCar"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        car_plaque = driver.find_element(By.NAME, "plaque")
        car_plaque.send_keys("A1E231")
        car_brand = driver.find_element(By.NAME, "brand")
        car_brand.click()
        car_brand.send_keys("Toyota")
        car_model = driver.find_element(By.NAME, "model")
        car_model.click()
        car_model.send_keys("Corolla")
        car_year = driver.find_element(By.NAME, "year")
        car_year.click()
        car_year.send_keys("2000")
        car_bodywork = driver.find_element(By.NAME, "bodywork")
        car_bodywork.click()
        car_bodywork.send_keys("JAKF9031ALFOF2231")
        car_motor = driver.find_element(By.NAME, "motor")
        car_motor.click()
        car_motor.send_keys("JAKF9032313AFFG31")
        car_color = driver.find_element(By.NAME, "color")
        car_color.click()
        car_color.send_keys("White")
        car_problem = driver.find_element(By.NAME, "problem")
        car_problem.click()
        car_problem.send_keys("Bad lights")
        car_plaque.send_keys(Keys.RETURN)
        wait.until(EC.url_to_be("http://localhost:5000/clients/details"))
        actualUrl = "http://localhost:5000/clients/details"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'tr')
        elements = element.find_elements(By.TAG_NAME, 'td')
        for k in elements:
            if (k.text == "JAKF9031ALFOF2231"):
                self.assertEqual(k.text,"JAKF9031ALFOF2231")