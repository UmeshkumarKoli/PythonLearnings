'''
Created on Sep 19, 2019

@author: DTE_ADMIN
'''
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
import Util

class Sntp_Settings(unittest.TestCase):


    def setUp(self):
        Util.init_ChromeDriver(self)
        #Util.init_IE_Driver(self)
        self.driver.maximize_window()
        self.driver.get('http://192.168.0.79')


    def tearDown(self):
        self.driver.find_element_by_css_selector("input[type='radio']:nth-child(1)").click()
        self.driver.find_element_by_css_selector("#sntpcfgForm  tr[class='row_even']  input[type=text]:nth-child(1)").send_keys("0")
        self.driver.find_element_by_css_selector("#sntpcfgForm  tr[class='row_even']  input[type=text]:nth-child(2)").send_keys("0")
        self.driver.find_element_by_css_selector("#sntpcfgForm  tr[class='row_even']  input[type=text]:nth-child(3)").send_keys("0")
        self.driver.find_element_by_css_selector("#sntpcfgForm  tr[class='row_even']  input[type=text]:nth-child(4)").send_keys("0")
        Select(self.driver.find_element_by_name("utc")).select_by_value("")
        self.driver.find_element_by_css_selector("#sntpcfgForm input[type=submit]").click()
        self.driver.switch_to_default_content()
        self.driver.find_element_by_css_selector('#sntpconfig > a').click()
        self.driver.switch_to_frame("center")
        self.driver.find_element_by_css_selector("input[type='radio']:nth-child(3)").click()
        self.driver.find_element_by_css_selector("#sntpcfgForm input[type=submit]").click()
        self.driver.close()
        self.driver.quit()

    def verify_Settings(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "#contentIframe tr[class='row_odd']  span")))
        self.assertEqual(self.driver.find_element_by_css_selector("#contentIframe tr[class='row_odd']  span").text, "on")
        self.assertEqual(self.driver.find_element_by_css_selector("#contentIframe tbody tr:nth-child(3) td:nth-child(2)").text, "192.168.0.5")
        self.assertEqual(self.driver.find_element_by_css_selector("#contentIframe tbody tr:nth-child(4) td:nth-child(2)").text, "UTC+5:30")
        self.driver.switch_to_default_content()
        self.driver.find_element_by_css_selector('#sntpconfig > a').click()
        self.driver.switch_to_frame("center")
        wait=WebDriverWait(self.driver,10)
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR,"input[type='radio']:nth-child(1)")))
        self.assertEqual(self.driver.find_element_by_css_selector("#sntpcfgForm tr:nth-child(3) td:nth-child(2)").text, "192.168.0.5")
        self.assertEqual(self.driver.find_element_by_css_selector("#sntpcfgForm tr:nth-child(4) td:nth-child(2)").text, "UTC+5:30")
                         
    def test_SNTP_Settings(self):
        self.driver.find_element_by_css_selector('#sntpconfig > a').click()
        self.driver.switch_to_frame("center")
        wait=WebDriverWait(self.driver,10)
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR,"input[type='radio']:nth-child(1)")))
        self.driver.find_element_by_css_selector("input[type='radio']:nth-child(1)").click()
        self.driver.find_element_by_css_selector("#sntpcfgForm  tr[class='row_even']  input[type=text]:nth-child(1)").send_keys("192")
        self.driver.find_element_by_css_selector("#sntpcfgForm  tr[class='row_even']  input[type=text]:nth-child(2)").send_keys("168")
        self.driver.find_element_by_css_selector("#sntpcfgForm  tr[class='row_even']  input[type=text]:nth-child(3)").send_keys("0")
        self.driver.find_element_by_css_selector("#sntpcfgForm  tr[class='row_even']  input[type=text]:nth-child(4)").send_keys("5")
        Select(self.driver.find_element_by_name("utc")).select_by_value("330")
        self.driver.find_element_by_css_selector("#sntpcfgForm input[type=submit]").click()
        self.verify_Settings()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()