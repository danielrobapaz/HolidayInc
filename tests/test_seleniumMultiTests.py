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
from .test_seleniumMetricTests import *

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
        proyect_end_date.send_keys("2023-03-30")
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
        solution_prompt.send_keys(Keys.RETURN)
        wait.until(EC.url_to_be("http://localhost:5000/root/proyect/detail"))
        actualUrl = "http://localhost:5000/root/proyect/detail"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)


    def test_RootEditCarInAProyect(self):
        self.test_RootAddCarToProyect()
        # Go To Proyect
        print("Go To Project")
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
        edit_detail_proyect_button = driver.find_element(By.NAME, "detail")
        edit_detail_proyect_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/root/proyect/detail"))
        actualUrl = "http://localhost:5000/root/proyect/detail"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)

        # Edit Proyect

        edit_proyect_button = driver.find_element(By.NAME, "edit")
        edit_proyect_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/root/modifyDetail"))
        actualUrl = "http://localhost:5000/root/modifyDetail"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        solution = driver.find_element(By.NAME,"solution")
        oldSolution = solution.get_attribute("value")
        solution.send_keys("fix other things")
        solution.send_keys(Keys.RETURN)
        wait.until(EC.url_to_be("http://localhost:5000/root/proyect/detail"))
        actualUrl = "http://localhost:5000/root/proyect/detail"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        driver.implicitly_wait(10)
        element = driver.find_element(By.TAG_NAME, 'section')   
        elements = element.find_elements(By.TAG_NAME, 'div')
        for e in elements:
            if (e.text == "fix other things"):
                self.assertEqual(e.text,"fix other things")
                self.assertNotEqual(oldSolution,e.text) 


    def test_RootDeleteCarInAProyect(self):
        self.test_RootAddCarToProyect()
        # Go To Proyect
        print("Go To Project")
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

        
        edit_detail_proyect_button = driver.find_element(By.NAME, "detail")
        edit_detail_proyect_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/root/proyect/detail"))
        actualUrl = "http://localhost:5000/root/proyect/detail"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)

        # Delete Car 

        edit_proyect_button = driver.find_element(By.NAME, "delete")
        edit_proyect_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/root/proyect/detail"))
        actualUrl = "http://localhost:5000/root/proyect/detail"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'section')   
        elements = element.find_elements(By.TAG_NAME, 'div')
        for e in elements:
            if (e.text == None):
                self.assertEqual(e.text,None)
        driver.implicitly_wait(10)



    def test_RootAddActions(self):
        
        # Go To Actions
        seleniumMetricTests.test_RootMetricCreate(self)
        self.test_RootAddCarToProyect()

        driver = self.driver
        driver.get("http://localhost:5000/root/proyect/detail")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/root/proyect/detail"))
        actualUrl = "http://localhost:5000/root/proyect/detail"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        action_button = driver.find_element(By.NAME, "action")
        action_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/plan"))
        actualUrl = "http://localhost:5000/plan"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)

        # Add Action
        create_action_button = driver.find_element(By.NAME, "create")
        create_action_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/plan/create"))
        actualUrl = "http://localhost:5000/plan/create"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        action_description = driver.find_element(By.NAME, "action")
        action_description.send_keys("testAction")
        activity_description = driver.find_element(By.NAME, "activity")
        activity_description.click()
        activity_description.send_keys("testActivity")
        action_starting_date = driver.find_element(By.NAME, "starting-date")
        action_starting_date.click()
        action_starting_date.send_keys("2023-03-11")
        action_end_date = driver.find_element(By.NAME, "end-date")
        action_end_date.click()
        action_end_date.send_keys("2023-03-12")
        respSelect = Select(driver.find_element(By.NAME, "resp"))
        respSelect.select_by_value("2")
        workers = driver.find_element(By.NAME, "workers")
        workers.click()
        workers.send_keys("3")
        costHour = driver.find_element(By.NAME, "costHour")
        costHour.click()
        costHour.send_keys("5")
        categorySelect = Select(driver.find_element(By.NAME, "category"))
        categorySelect.select_by_value("Material")
        supplie = driver.find_element(By.NAME, "supplie")
        supplie.click()
        supplie.send_keys("cuerda")
        metricSelect = Select(driver.find_element(By.NAME, "metric"))
        metricSelect.select_by_value("1")
        quantity = driver.find_element(By.NAME, "quantity")
        quantity.click()
        quantity.send_keys("2")
        costSupplie = driver.find_element(By.NAME, "costSupplie")
        costSupplie.click()
        costSupplie.send_keys("5")
        costSupplie.send_keys(Keys.RETURN)
        wait.until(EC.url_to_be("http://localhost:5000/plan"))
        actualUrl = "http://localhost:5000/plan"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        hours = False
        total = False
        element = driver.find_elements(By.TAG_NAME, 'td')
        for e in element:
            if (e.text == "16"):
                hours = True
            if (e.text == "90"):
                total = True
        self.assertTrue(hours and total)
        human = driver.find_element(By.NAME, "human")
        human.click()        
        wait.until(EC.url_to_be("http://localhost:5000/plan/humanTalent"))
        actualUrl = "http://localhost:5000/plan/humanTalent"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        hours = False
        total = False
        element = driver.find_elements(By.TAG_NAME, 'td')
        for e in element:
            if (e.text == "3"):
                hours = True
            if (e.text == "80"):
                total = True
        self.assertTrue(hours and total)
        supplie = driver.find_element(By.NAME, "supplie")
        supplie.click()        
        wait.until(EC.url_to_be("http://localhost:5000/plan/supplie"))
        actualUrl = "http://localhost:5000/plan/supplie"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        hours = False
        total = False
        element = driver.find_elements(By.TAG_NAME, 'td')
        for e in element:
            if (e.text == "2"):
                hours = True
            if (e.text == "10"):
                total = True
        self.assertTrue(hours and total)
        
    
    def test_RootEditActions(self):
        
        # Go To Actions
        self.test_RootAddActions()
         
        # go to edit
        driver = self.driver
        driver.get("http://localhost:5000/plan")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/plan"))
        actualUrl = "http://localhost:5000/plan"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        edit_button = driver.find_element(By.NAME, "edit")
        edit_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/plan/edit"))
        actualUrl = "http://localhost:5000/plan/edit"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)

        # Edit Action
        action_description = driver.find_element(By.NAME, "action")
        action_description.clear()
        action_description.send_keys("testActionNew")
        # activity_description = driver.find_element(By.NAME, "activity")
        # activity_description.click()
        # activity_description.send_keys("testActivity")
        # action_starting_date = driver.find_element(By.NAME, "starting-date")
        # action_starting_date.click()
        # action_starting_date.send_keys("2023-03-11")
        # action_end_date = driver.find_element(By.NAME, "end-date")
        # action_end_date.click()
        # action_end_date.send_keys("2023-03-12")
        # respSelect = Select(driver.find_element(By.NAME, "resp"))
        # respSelect.select_by_value("2")
        # workers = driver.find_element(By.NAME, "workers")
        # workers.click()
        # workers.send_keys("3")
        # costHour = driver.find_element(By.NAME, "costHour")
        # costHour.click()
        # costHour.send_keys("5")
        # categorySelect = Select(driver.find_element(By.NAME, "category"))
        # categorySelect.select_by_value("Material")
        # supplie = driver.find_element(By.NAME, "supplie")
        # supplie.click()
        # supplie.send_keys("cuerda")
        # metricSelect = Select(driver.find_element(By.NAME, "metric"))
        # metricSelect.select_by_value("1")
        # quantity = driver.find_element(By.NAME, "quantity")
        # quantity.click()
        # quantity.send_keys("2")
        costSupplie = driver.find_element(By.NAME, "costSupplie")
        costSupplie.clear()
        costSupplie.send_keys("10")
        costSupplie.send_keys(Keys.RETURN)
        wait.until(EC.url_to_be("http://localhost:5000/plan"))
        actualUrl = "http://localhost:5000/plan"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        hours = False
        total = False
        element = driver.find_elements(By.TAG_NAME, 'td')
        for e in element:
            if (e.text == "16"):
                hours = True
            if (e.text == "100"):
                total = True
        self.assertTrue(hours and total)
        human = driver.find_element(By.NAME, "human")
        human.click()        
        wait.until(EC.url_to_be("http://localhost:5000/plan/humanTalent"))
        actualUrl = "http://localhost:5000/plan/humanTalent"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        hours = False
        total = False
        element = driver.find_elements(By.TAG_NAME, 'td')
        for e in element:
            if (e.text == "3"):
                hours = True
            if (e.text == "80"):
                total = True
        self.assertTrue(hours and total)
        supplie = driver.find_element(By.NAME, "supplie")
        supplie.click()        
        wait.until(EC.url_to_be("http://localhost:5000/plan/supplie"))
        actualUrl = "http://localhost:5000/plan/supplie"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        hours = False
        total = False
        element = driver.find_elements(By.TAG_NAME, 'td')
        for e in element:
            if (e.text == "2"):
                hours = True
            if (e.text == "20"):
                total = True
        self.assertTrue(hours and total)


    def test_RootAddActionsOnlyHuman(self):
        
        # Go     To Actions
        seleniumMetricTests.test_RootMetricCreate(self)
        self.test_RootAddCarToProyect()

        driver = self.driver
        driver.get("http://localhost:5000/root/proyect/detail")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/root/proyect/detail"))
        actualUrl = "http://localhost:5000/root/proyect/detail"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        action_button = driver.find_element(By.NAME, "action")
        action_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/plan"))
        actualUrl = "http://localhost:5000/plan"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)

        # go to create
        create_button = driver.find_element(By.NAME, "create")
        create_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/plan/create"))
        actualUrl = "http://localhost:5000/plan/create"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)

        # Create Only Human Action
        action_description = driver.find_element(By.NAME, "action")
        action_description.clear()
        action_description.send_keys("testActionOnlyHuman")
        activity_description = driver.find_element(By.NAME, "activity")
        activity_description.click()
        activity_description.send_keys("testActivity")
        action_starting_date = driver.find_element(By.NAME, "starting-date")
        action_starting_date.click()
        action_starting_date.send_keys("2023-03-11")
        action_end_date = driver.find_element(By.NAME, "end-date")
        action_end_date.click()
        action_end_date.send_keys("2023-03-12")
        respSelect = Select(driver.find_element(By.NAME, "resp"))
        respSelect.select_by_value("2")
        workers = driver.find_element(By.NAME, "workers")
        workers.click()
        workers.send_keys("3")
        costHour = driver.find_element(By.NAME, "costHour")
        costHour.click()
        costHour.send_keys("5")
        # categorySelect = Select(driver.find_element(By.NAME, "category"))
        # categorySelect.select_by_value("Material")
        # supplie = driver.find_element(By.NAME, "supplie")
        # supplie.click()
        # supplie.send_keys("cuerda")
        # metricSelect = Select(driver.find_element(By.NAME, "metric"))
        # metricSelect.select_by_value("1")
        # quantity = driver.find_element(By.NAME, "quantity")
        # quantity.click()
        # quantity.send_keys("2")
        # costSupplie = driver.find_element(By.NAME, "costSupplie")
        # costSupplie.clear()
        # costSupplie.send_keys("10")
        costHour.send_keys(Keys.RETURN)
        wait.until(EC.url_to_be("http://localhost:5000/plan"))
        actualUrl = "http://localhost:5000/plan"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        hours = False
        total = False
        element = driver.find_elements(By.TAG_NAME, 'td')
        for e in element:
            if (e.text == "16"):
                hours = True
            if (e.text == "80"):
                total = True
        self.assertTrue(hours and total)
        human = driver.find_element(By.NAME, "human")
        human.click()        
        wait.until(EC.url_to_be("http://localhost:5000/plan/humanTalent"))
        actualUrl = "http://localhost:5000/plan/humanTalent"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        hours = False
        total = False
        element = driver.find_elements(By.TAG_NAME, 'td')
        for e in element:
            if (e.text == "3"):
                hours = True
            if (e.text == "80"):
                total = True
        self.assertTrue(hours and total)
        supplie = driver.find_element(By.NAME, "supplie")
        supplie.click()        
        wait.until(EC.url_to_be("http://localhost:5000/plan/supplie"))
        actualUrl = "http://localhost:5000/plan/supplie"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        hours = False
        total = False
        element = driver.find_elements(By.TAG_NAME, 'td')
        for e in element:
            if (e.text == "0"):
                hours = True
            if (e.text == "0"):
                total = True
        self.assertTrue(hours and total)


    def test_RootAddActionsIncomplete(self):
        
        # Go To Actions
        seleniumMetricTests.test_RootMetricCreate(self)
        self.test_RootAddCarToProyect()

        driver = self.driver
        driver.get("http://localhost:5000/root/proyect/detail")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/root/proyect/detail"))
        actualUrl = "http://localhost:5000/root/proyect/detail"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        action_button = driver.find_element(By.NAME, "action")
        action_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/plan"))
        actualUrl = "http://localhost:5000/plan"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)

        # go to create
        create_button = driver.find_element(By.NAME, "create")
        create_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/plan/create"))
        actualUrl = "http://localhost:5000/plan/create"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)

        # Create Only Human Action
        action_description = driver.find_element(By.NAME, "action")
        action_description.clear()
        # action_description.send_keys("testActionOnlyHuman")
        activity_description = driver.find_element(By.NAME, "activity")
        activity_description.click()
        activity_description.send_keys("testActivity")
        action_starting_date = driver.find_element(By.NAME, "starting-date")
        action_starting_date.click()
        action_starting_date.send_keys("2023-03-11")
        action_end_date = driver.find_element(By.NAME, "end-date")
        action_end_date.click()
        action_end_date.send_keys("2023-03-12")
        respSelect = Select(driver.find_element(By.NAME, "resp"))
        respSelect.select_by_value("2")
        workers = driver.find_element(By.NAME, "workers")
        workers.click()
        workers.send_keys("3")
        costHour = driver.find_element(By.NAME, "costHour")
        costHour.click()
        costHour.send_keys("5")
        # categorySelect = Select(driver.find_element(By.NAME, "category"))
        # categorySelect.select_by_value("Material")
        # supplie = driver.find_element(By.NAME, "supplie")
        # supplie.click()
        # supplie.send_keys("cuerda")
        # metricSelect = Select(driver.find_element(By.NAME, "metric"))
        # metricSelect.select_by_value("1")
        # quantity = driver.find_element(By.NAME, "quantity")
        # quantity.click()
        # quantity.send_keys("2")
        # costSupplie = driver.find_element(By.NAME, "costSupplie")
        # costSupplie.clear()
        # costSupplie.send_keys("10")
        costHour.send_keys(Keys.RETURN)
        wait.until(EC.url_to_be("http://localhost:5000/plan/create"))
        actualUrl = "http://localhost:5000/plan/create"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        

    def test_RootAddActionsOutdated(self):
        
        # Go To Actions
        seleniumMetricTests.test_RootMetricCreate(self)
        self.test_RootAddCarToProyect()

        driver = self.driver
        driver.get("http://localhost:5000/root/proyect/detail")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/root/proyect/detail"))
        actualUrl = "http://localhost:5000/root/proyect/detail"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        action_button = driver.find_element(By.NAME, "action")
        action_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/plan"))
        actualUrl = "http://localhost:5000/plan"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)

        # Add Action
        create_action_button = driver.find_element(By.NAME, "create")
        create_action_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/plan/create"))
        actualUrl = "http://localhost:5000/plan/create"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        action_description = driver.find_element(By.NAME, "action")
        action_description.send_keys("testAction")
        activity_description = driver.find_element(By.NAME, "activity")
        activity_description.click()
        activity_description.send_keys("testActivity")
        action_starting_date = driver.find_element(By.NAME, "starting-date")
        action_starting_date.click()
        action_starting_date.send_keys("2023-04-11")
        action_end_date = driver.find_element(By.NAME, "end-date")
        action_end_date.click()
        action_end_date.send_keys("2023-05-12")
        respSelect = Select(driver.find_element(By.NAME, "resp"))
        respSelect.select_by_value("2")
        workers = driver.find_element(By.NAME, "workers")
        workers.click()
        workers.send_keys("3")
        costHour = driver.find_element(By.NAME, "costHour")
        costHour.click()
        costHour.send_keys("5")
        categorySelect = Select(driver.find_element(By.NAME, "category"))
        categorySelect.select_by_value("Material")
        supplie = driver.find_element(By.NAME, "supplie")
        supplie.click()
        supplie.send_keys("cuerda")
        metricSelect = Select(driver.find_element(By.NAME, "metric"))
        metricSelect.select_by_value("1")
        quantity = driver.find_element(By.NAME, "quantity")
        quantity.click()
        quantity.send_keys("2")
        costSupplie = driver.find_element(By.NAME, "costSupplie")
        costSupplie.click()
        costSupplie.send_keys("5")
        costSupplie.send_keys(Keys.RETURN)
        wait.until(EC.url_to_be("http://localhost:5000/plan/create"))
        actualUrl = "http://localhost:5000/plan/create"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        driver.implicitly_wait(2)
        element = driver.find_element(By.TAG_NAME, 'section')
        elements = element.find_elements(By.TAG_NAME, 'div')
        for e in elements:
            if (e.text == "Invalid dates, out of proyect range"):
                self.assertEqual(e.text,"Invalid dates, out of proyect range")


    def test_RootDeleteMetricCheck(self):
        self.test_RootAddActions()
        driver = self.driver
        driver.get("http://localhost:5000/metrics/metrics")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/metrics/metrics"))
        actualUrl = "http://localhost:5000/metrics/metrics"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_elements(By.TAG_NAME, 'td')
        for e in element:
            if (e.text == "10"):
                self.assertEqual(e.text,"10")
        edit_button = driver.find_element(By.NAME, "delete")
        edit_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/metrics/metrics"))
        actualUrl = "http://localhost:5000/metrics/metrics"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_elements(By.TAG_NAME, 'td')
        for e in element:
            if (e.text == "20"):
                self.assertNotEqual(e.text,"20")
        driver.implicitly_wait(2)
        driver.get("http://localhost:5000/plan/supplie")
        wait.until(EC.url_to_be("http://localhost:5000/plan/supplie"))
        actualUrl = "http://localhost:5000/plan/supplie"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        total = False
        element = driver.find_elements(By.TAG_NAME, 'td')
        for e in element:
            if (e.text == "0"):
                total = True
        self.assertTrue(total)
