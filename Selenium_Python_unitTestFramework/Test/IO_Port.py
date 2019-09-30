'''
Created on Aug 26, 2019

@author: DTE_ADMIN
'''
from time import sleep
import unittest

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
import Util


class IO_Port_settings(unittest.TestCase):

    def setUp(self):
        Util.init_ChromeDriver(self)
        #Util.init_IE_Driver(self)
        self.driver.maximize_window()
        self.driver.get('http://192.168.0.79')

    def defaultValues(self):
        self.driver.find_element_by_xpath("//*[@id='failsafeOff']").click()
        Select(self.driver.find_element_by_id("selektor_channel_io1")).select_by_value("inactive")
        Select(self.driver.find_element_by_id("selektor_channel_io2")).select_by_value("inactive")
        Select(self.driver.find_element_by_id("selektor_channel_io3")).select_by_value("inactive")
        Select(self.driver.find_element_by_id("selektor_channel_io4")).select_by_value("inactive")
        
    def tearDown(self):
        self.defaultValues()
        self.driver.find_element_by_name("action").click()
        self.driver.quit()

    def test_change_Settings(self):
        self.driver.find_element_by_xpath("//*[@id='ioportconfig']/a").click()
        self.driver.switch_to_frame("center")
        sleep(2)
        self.defaultValues()
        
        # Global_Settings
        self.driver.find_element_by_xpath("//*[@id='failsafeOn']").click()
        
        # IO-1 Settings
        Select(self.driver.find_element_by_id("selektor_channel_io1")).select_by_value("input")
        Select(self.driver.find_element_by_name("dataHoldTime_io1")).select_by_visible_text("100")
        self.driver.find_element_by_xpath("//*[@id='overloadDetection_off_io1']").click()
        
        # IO-2 Settings
        Select(self.driver.find_element_by_id("selektor_channel_io2")).select_by_value("output")
        Select(self.driver.find_element_by_name("dataHoldTime_io2")).select_by_visible_text("2000")
        self.driver.find_element_by_xpath("//*[@id='overloadDetection_off_io2']").click()
        self.driver.find_element_by_xpath("//*[@id='overcurrentDetection_off_io2']").click()
        
        # IO-3 Settings
        Select(self.driver.find_element_by_id("selektor_channel_io3")).select_by_value("rwh_rw")
        Select(self.driver.find_element_by_name("dataHoldTime_io3")).select_by_visible_text("20")
        self.driver.find_element_by_xpath("//*[@id='overloadDetection_off_io3']").click()
        self.driver.find_element_by_xpath("//*[@id='overcurrentDetection_off_io3']").click()
        self.driver.find_element_by_id("dataNumberOfBlocks_io3").send_keys(Keys.CONTROL + "a")
        self.driver.find_element_by_id("dataNumberOfBlocks_io3").send_keys(Keys.DELETE)
        self.driver.find_element_by_id("dataNumberOfBlocks_io3").send_keys("200")
        Select(self.driver.find_element_by_name("dataBlockLength_io3")).select_by_visible_text("255")
        self.driver.find_element_by_id("uidEdgedControlled_on_io3").click()
        
        # IO-4 Settings
        Select(self.driver.find_element_by_id("selektor_channel_io4")).select_by_value("rwh_rw")
        sleep(1)
        Select(self.driver.find_element_by_id("selektor_channel_io4")).select_by_value("inactive")
        
        # Click on Activate and Save
        self.driver.find_element_by_name("action").click()
        
        # Verification
        wait = WebDriverWait(self.driver, 10)
        wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "//*[@id='tblPortconfig']/tbody[1]/tr[1]/td[2]/span")))
        self.assertEqual(self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[1]/tr[1]/td[2]/span").text, "on")
        
        self.assertEqual(self.driver.find_element_by_xpath("//*[@id='currmode_channel_io1']/span").text, "Input")
        self.assertEqual(self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[2]/tr[2]/td[2]").text, "100")
        self.assertEqual(self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[2]/tr[3]/td[2]/span").text, "off")
        
        self.assertEqual(self.driver.find_element_by_xpath("//*[@id='currmode_channel_io2']/span").text, "Output")
        self.assertEqual(self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[3]/tr[2]/td[2]").text, "2000")
        self.assertEqual(self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[3]/tr[3]/td[2]/span").text, "off")
        self.assertEqual(self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[3]/tr[4]/td[2]/span").text, "off")
        
        self.assertEqual(self.driver.find_element_by_xpath("//*[@id='currmode_channel_io3']/span").text, "RWH RW")
        self.assertEqual(self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[4]/tr[2]/td[2]").text, "20")
        self.assertEqual(self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[4]/tr[3]/td[2]/span").text, "off")
        self.assertEqual(self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[4]/tr[4]/td[2]/span").text, "off")
        self.assertEqual(self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[4]/tr[6]/td[2]").text, "200")
        self.assertEqual(self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[4]/tr[7]/td[2]").text, "255")
        self.assertEqual(self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[4]/tr[8]/td[2]/span").text, "on")
        
        self.assertEqual(self.driver.find_element_by_xpath("//*[@id='currmode_channel_io4']/span").text, "Inactive")
        
        self.driver.find_element_by_xpath("//input[@name='action']").click()
        
        sleep(1)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
