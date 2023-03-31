from . import SeleniumClass
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class seleniumClientsTests(SeleniumClass):

    def test_RootCreateDepartment(self):
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

    def test_RootDepartmentDuplicated(self):
        self.test_RootCreateDepartment()
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        driver.get("http://localhost:5000/deparment/view")
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
        element = driver.find_element(By.TAG_NAME, 'section')
        elements = element.find_elements(By.TAG_NAME, 'div')
        for k in elements:
            if (k.text == "Department testdept already exist"):
                self.assertEqual(k.text,"Department testdept already exist")


    def test_RootDepartmentAddProblem(self):
        self.test_RootCreateDepartment()
        driver = self.driver
        wait = WebDriverWait(driver, 10)
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



    def test_RootDeleteDepartment(self):
        self.test_RootCreateDepartment()
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        driver.get("http://localhost:5000/deparment/view")
        wait.until(EC.url_to_be("http://localhost:5000/deparment/view"))
        actualUrl = "http://localhost:5000/deparment/view"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'tr')
        elements = element.find_elements(By.TAG_NAME, 'td')
        for k in elements:
            if (k.text == "testdept"):
                self.assertEqual(k.text,"testdept")
        delete_dept_button = driver.find_element(By.NAME, "delete")
        delete_dept_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/deparment/view"))
        actualUrl = "http://localhost:5000/deparment/view"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'section')
        elements = element.find_elements(By.TAG_NAME, 'div')
        for k in elements:
            if (k.text == None):
                self.assertNotEqual(k.text,"testdept")