'''
Created on Sep 5, 2019

@author: DTE_ADMIN
'''
import os,pytest
import Util
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from pyrobot import Robot
from pyrobot import Robot, Keys

class Test_Firmware_Settings():
    @pytest.fixture()
    def test_setUp(self):
        Util.init_ChromeDriver(self)
        #Util.init_IE_Driver(self)
        self.driver.maximize_window()
        self.driver.get('http://192.168.0.79')
        yield
        self.driver.close()
        self.driver.quit()
    
    def verify_settings(self):
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath("//*[@id='fwupdate']/a").click()
        self.driver.switch_to_frame("center")
        wait=WebDriverWait(self.driver,10)
        wait.until(expected_conditions.visibility_of_element_located((By.XPATH,"//*[@id='fwupdateForm']/p[2]/input")))
        version_firmware=self.driver.find_element_by_xpath("//tbody/tr[2]/td[3]").text
        if(version_firmware== "V1.2.6"):
            flag3= True
        else: 
            flag3= False
        self.driver.switch_to_default_content()
        version_firmware_HardwareTable=self.driver.find_element_by_xpath("//*[@id='content']/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr[4]/td[2]").text
        if(version_firmware_HardwareTable== "V1.2.6"):
            flag4= True
        else: 
            flag4= False
        assert(flag3==True and flag4==True)
        
    def test_firmware(self,test_setUp):
        self.driver.find_element_by_xpath("//*[@id='fwupdate']/a").click()
        self.driver.switch_to_frame("center")
        wait=WebDriverWait(self.driver,10)
        wait.until(expected_conditions.visibility_of_element_located((By.XPATH,"//*[@id='fwupdateForm']/p[2]/input")))
        self.driver.find_element_by_xpath("//*[@id='fwupdateForm']/p[2]/input").click()
        sleep(1)
        robot=Robot()
        robot.add_to_clipboard("I:\Share\Umesh\Firmware\DTE\dte101_1.2.6.nxf")
        robot.paste()
        robot.press_and_release(Keys.enter)
         
        self.driver.find_element_by_xpath("//input[@type='submit']").click()
        wait.until(expected_conditions.visibility_of_element_located((By.XPATH,"//*[@id='contentIframe']/p[1]/b")))
        if(self.driver.find_element_by_xpath("//*[@id='contentIframe']/p[1]/b").text== "Firmware transfer and update succeeded!"):
            flag1= True
        else: 
            flag1= False
        sleep(1)
        self.driver.find_element_by_xpath("//input[@type='checkbox']").click()
        self.driver.find_element_by_xpath("//input[@type='submit']").click()
        wait.until(expected_conditions.visibility_of_element_located((By.XPATH,"//*[@id='contentIframe']/p[1]")))
        if(self.driver.find_element_by_xpath("//*[@id='contentIframe']/p[1]").text== "The device was successfully restarted."):
            flag2= True
        else: 
            flag2= False
        assert(flag1==True and flag2==True)
        self.verify_settings()