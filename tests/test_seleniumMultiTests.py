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

class seleniumMultiTests(SeleniumClass):
    
    def test_RootAddCarToProyect(self):
        # CreateProyect
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
        proyect_description = driver.find_element(By.ID, "description")
        proyect_description.send_keys("testproyect")
        proyect_starting_date = driver.find_element(By.ID, "starting-date")
        proyect_starting_date.click()
        proyect_starting_date.send_keys("2023-03-10")
        proyect_end_date = driver.find_element(By.ID, "end-date")
        proyect_end_date.click()
        proyect_end_date.send_keys("2023-03-15")
        proyect_description.send_keys(Keys.RETURN)
        wait.until(EC.url_to_be("http://localhost:5000/root/proyects"))
        actualUrl = "http://localhost:5000/root/proyects"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        # Create USer

        driver.get("http://localhost:5000/root/users")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/root/users"))
        actualUrl = "http://localhost:5000/root/users"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        create_user_button = driver.find_element(By.NAME, "create")
        create_user_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/root/createUser"))
        actualUrl = "http://localhost:5000/root/createUser"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        username = driver.find_element(By.NAME,"username")
        username.send_keys("manager")
        firstname = driver.find_element(By.NAME, "firstname")
        firstname.send_keys("managername")
        secondname = driver.find_element(By.NAME, "secondname")
        secondname.send_keys("managersecondname")
        password = driver.find_element(By.NAME,"password")
        password.send_keys("password")
        roleSelect = Select(driver.find_element(By.NAME, "role"))
        roleSelect.select_by_visible_text("Gerente de operaciones")
        proyectSelect = Select(driver.find_element(By.NAME, "proyect"))
        proyectSelect.select_by_visible_text("testproyect")
        username.send_keys(Keys.RETURN)
        wait.until(EC.url_to_be("http://localhost:5000/root/users"))
        actualUrl = "http://localhost:5000/root/users"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'section')   
        elements = element.find_elements(By.TAG_NAME, 'div')
        for e in elements:
            if (e.text == "manager"):
                self.assertEqual(e.text,"manager") 

        # Create Client 
        driver.get("http://localhost:5000/user/root")
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

        # Create Car

        driver.get("http://localhost:5000/clients")
        wait.until(EC.url_to_be("http://localhost:5000/clients"))
        actualUrl = "http://localhost:5000/clients"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        client_details = driver.find_element(By.NAME, "detail")
        client_details.click()
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

        # Create Department
        
        driver.get("http://localhost:5000/user/root")
        wait.until(EC.url_to_be("http://localhost:5000/user/root"))
        actualUrl = "http://localhost:5000/user/root"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        department_button = driver.find_element(By.NAME, "dep")
        department_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/deparment/view"))
        actualUrl = "http://localhost:5000/deparment/view"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        create_dep_input = driver.find_element(By.NAME, "dep")
        create_dep_input.click()
        create_dep_input.send_keys("testdept")
        create_dep_button = driver.find_element(By.NAME, "create")
        create_dep_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/deparment/view"))
        actualUrl = "http://localhost:5000/deparment/view"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'tr')
        elements = element.find_elements(By.TAG_NAME, 'td')
        for k in elements:
            if (k.text == "testdept"):
                self.assertEqual(k.text,"testdept")

        # Create Problem    

        driver.get("http://localhost:5000/deparment/view")
        wait.until(EC.url_to_be("http://localhost:5000/deparment/view"))
        actualUrl = "http://localhost:5000/deparment/view"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        problems_button = driver.find_element(By.NAME, "problems")
        problems_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/deparment/problems"))
        actualUrl = "http://localhost:5000/deparment/problems"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        select_dept = Select(driver.find_element(By.NAME, "select"))
        select_dept.select_by_visible_text("testdept")
        problems_input = driver.find_element(By.NAME, "problem")
        problems_input.click()
        problems_input.send_keys("testproblem")
        problems_input.send_keys(Keys.RETURN)
        wait.until(EC.url_to_be("http://localhost:5000/deparment/view"))
        actualUrl = "http://localhost:5000/deparment/view"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        dpt_details = driver.find_element(By.NAME, "detail")
        dpt_details.click()
        wait.until(EC.url_to_be("http://localhost:5000/deparment/detail"))
        actualUrl = "http://localhost:5000/deparment/detail"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'tr')
        elements = element.find_elements(By.TAG_NAME, 'td')
        for k in elements:
            if (k.text == "testproblem"):
                self.assertEqual(k.text,"testproblem")
        # Add client to the project

        driver.get("http://localhost:5000/root/proyects")
        actualUrl = "http://localhost:5000/root/proyects"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        detail_proj_button = driver.find_element(By.NAME, "detail")
        detail_proj_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/root/proyect/detail"))
        actualUrl = "http://localhost:5000/root/proyect/detail"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        add_client_button = driver.find_element(By.NAME, "add")
        add_client_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/root/addClient"))
        actualUrl = "http://localhost:5000/root/addClient"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        carSelect = Select(driver.find_element(By.NAME, "plaque"))
        carSelect.select_by_index(1)
        managerSelect = Select(driver.find_element(By.NAME, "manager"))
        managerSelect.select_by_index(1)
        problemSelect = Select(driver.find_element(By.NAME, "problem"))
        problemSelect.select_by_index(1)
        solution_prompt = driver.find_element(By.NAME, "solution")
        solution_prompt.send_keys("fix things")
        total_prompt = driver.find_element(By.NAME, "total")
        total_prompt.send_keys("32132")
        total_prompt.send_keys(Keys.RETURN)
        wait.until(EC.url_to_be("http://localhost:5000/root/proyect/detail"))
        actualUrl = "http://localhost:5000/root/proyect/detail"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
