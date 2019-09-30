'''
Created on Sep 23, 2019

@author: DTE_ADMIN
'''
from time import sleep
import unittest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

import Util


class Profinet_Settings(unittest.TestCase):


    def setUp(self):
        Util.init_ChromeDriver(self)
        #Util.init_IE_Driver(self)
        self.driver.maximize_window()
        self.driver.get('http://192.168.0.79')

    def tearDown(self):
        self.driver.close()
        self.driver.quit()

    def test_Change_Profinet_Settings(self):
        wait=WebDriverWait(self.driver,10)
        self.driver.find_element_by_xpath("//*[@id='pnconfig']/a").click()
        self.driver.switch_to_frame("center")
        element=wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "#pnStationNameID")))
        element.send_keys("123456")
        self.driver.find_element_by_css_selector("#pnsettingsID").click()
        element=wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "#resetForm > input[type=checkbox]")))
        element.click()
        sleep(1)
        self.driver.find_element_by_css_selector("#resetForm input[type=submit]").click()
        sleep(1)
        element=wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "#contentIframe > p.resp_success")))
        sleep(2)
        self.assertEqual(element.text,"The device was successfully restarted.")
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()