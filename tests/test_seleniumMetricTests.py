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
from .test_seleniumLoginTests import *


class seleniumMetricTests(SeleniumClass):
    
    def test_RootMetricCreate(self):
        seleniumLoginTests.test_LoginRoot(self)
        driver = self.driver
        driver.get("http://localhost:5000/metrics/metrics")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/metrics/metrics"))
        actualUrl = "http://localhost:5000/metrics/metrics"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        dim_input = driver.find_element(By.NAME, "dim")
        dim_input.send_keys("10")
        metric_input = driver.find_element(By.NAME, "metric")
        metric_input.send_keys("metros")
        create_button = driver.find_element(By.NAME, "create")
        create_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/metrics/metrics"))
        actualUrl = "http://localhost:5000/metrics/metrics"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'tr')   
        elements = element.find_elements(By.TAG_NAME, 'td')
        for e in elements:
            if (e.text == "10"):
                self.assertEqual(e.text,"10")

    def test_RootMetricEdit(self):
        self.test_RootMetricCreate()
        driver = self.driver
        driver.get("http://localhost:5000/metrics/metrics")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/metrics/metrics"))
        actualUrl = "http://localhost:5000/metrics/metrics"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'tr')   
        elements = element.find_elements(By.TAG_NAME, 'td')
        for e in elements:
            if (e.text == "10"):
                self.assertEqual(e.text,"10")
        edit_button = driver.find_element(By.NAME, "edit")
        edit_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/metrics/editMetric"))
        actualUrl = "http://localhost:5000/metrics/editMetric"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        dim_input = driver.find_element(By.NAME, "dim")
        dim_input.clear()
        dim_input.send_keys("20")
        metric_input = driver.find_element(By.NAME, "unit")
        metric_input.send_keys(Keys.RETURN)
        wait.until(EC.url_to_be("http://localhost:5000/metrics/metrics"))
        actualUrl = "http://localhost:5000/metrics/metrics"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'tr')   
        elements = element.find_elements(By.TAG_NAME, 'td')
        for e in elements:
            if (e.text == "20"):
                self.assertEqual(e.text,"20")
        driver.implicitly_wait(10)

    def test_RootMetricDelete(self):
        self.test_RootMetricCreate()
        driver = self.driver
        driver.get("http://localhost:5000/metrics/metrics")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_to_be("http://localhost:5000/metrics/metrics"))
        actualUrl = "http://localhost:5000/metrics/metrics"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'tr')   
        elements = element.find_elements(By.TAG_NAME, 'td')
        for e in elements:
            if (e.text == "10"):
                self.assertEqual(e.text,"10")
        edit_button = driver.find_element(By.NAME, "delete")
        edit_button.click()
        wait.until(EC.url_to_be("http://localhost:5000/metrics/metrics"))
        actualUrl = "http://localhost:5000/metrics/metrics"
        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,actualUrl)
        element = driver.find_element(By.TAG_NAME, 'tr')   
        elements = element.find_elements(By.TAG_NAME, 'td')
        for e in elements:
            if (e.text == "20"):
                self.assertNotEqual(e.text,"20")
        driver.implicitly_wait(10)