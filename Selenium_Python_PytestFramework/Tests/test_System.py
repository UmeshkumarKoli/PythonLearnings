'''
Created on Sep 17, 2019

@author: DTE_ADMIN
'''
from pyrobot import Robot, Keys
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import Util
from time import sleep


class Test_System_Settings():

    def setPassword(self,oldPass,newPass):
        
        self.driver.find_element_by_xpath("//*[@id='pwpForm']//input[@name='passwordOld']").send_keys(oldPass)
        self.driver.find_element_by_xpath("//*[@id='pwpForm']//input[@name='passwordNew']").send_keys(newPass)
        self.driver.find_element_by_xpath("//*[@id='pwpForm']//input[@name='passwordConf']").send_keys(newPass)
        self.driver.find_element_by_xpath("//*[@id='pwpForm']//input[@type='submit']").click()

    @pytest.fixture()
    def test_setUp(self):
        Util.init_ChromeDriver(self)
        #Util.init_IE_Driver(self)
        
        self.driver.maximize_window()
        self.driver.get('http://192.168.0.79')
        yield
        self.driver.switch_to_default_content()
        sleep(2)
        self.driver.find_element_by_id('system').click()
        #self.driver.find_element_by_id('system').click()
        sleep(2)
        robot=Robot()
        robot.add_to_clipboard("admin")
        robot.paste()
        sleep(1)
        robot.press_and_release(Keys.tab)
        sleep(1)
        robot.add_to_clipboard("iepl")
        robot.paste()
        sleep(1)
        robot.press_and_release(Keys.enter)
        self.driver.switch_to_frame("center")
        wait=WebDriverWait(self.driver,10)
        wait.until(expected_conditions.visibility_of_element_located((By.XPATH,"//*[@id='pwpForm']//input[@value='off']")))
        self.driver.find_element_by_xpath("//*[@id='pwpForm']//input[@value='off']").click()
        self.setPassword("iepl","admin")
        self.driver.quit()

        
    def test_System_Settings(self,test_setUp):
        #self.driver.find_element_by_xpath("//*[@id='system']/a").click()
        self.driver.find_element_by_id('system').click()
        self.driver.switch_to_frame("center")
        wait=WebDriverWait(self.driver,10)
        #sleep(2)
        wait.until(expected_conditions.visibility_of_element_located((By.XPATH,"//*[@id='pwpForm']//input[@value='on']")))
        self.driver.find_element_by_xpath("//*[@id='pwpForm']//input[@value='on']").click()
        self.setPassword("admin","iepl")
        element = wait.until(expected_conditions.visibility_of_element_located((By.XPATH,"//*[@id='contentIframe']/table//span")))
        if(element.text== "on"):
             flag1= True
        else: 
            flag1= False
        if(self.driver.find_element_by_xpath("//*[@id='contentIframe']/p[1]").text== "The password protection has been activated."):
            flag2= True
        else: 
            flag2= False
        if(self.driver.find_element_by_xpath("//*[@id='contentIframe']/p[2]").text== "Your password has been changed successfully."):
            flag3= True
        else: 
            flag3= False
        #self.driver.find_element_by_xpath("//*[@id='resetForm']/input").click()
        self.driver.find_element_by_css_selector("#resetForm > input[type=checkbox]").click()
        sleep(1)
        if not self.driver.find_element_by_css_selector("#resetForm > input[type=checkbox]").is_selected():
            self.driver.find_element_by_css_selector("#resetForm > input[type=checkbox]").click()
        #self.driver.find_element_by_xpath("//*[@id='resetForm']//input[@name='submit_button']").click()
        self.driver.find_element_by_css_selector("#resetForm > table > tbody > tr > td > input[type=submit]").click()
        sleep(1)
        element = wait.until(expected_conditions.visibility_of_element_located((By.XPATH,"//*[@id='contentIframe']/p[1]")))
        if(element.text== "The device was successfully restarted."):
            flag4= True
        else: 
            flag4= False
        
        assert(flag1==True and flag2==True and flag3==True and flag4==True)