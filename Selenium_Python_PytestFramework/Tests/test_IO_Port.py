'''
Created on Aug 26, 2019

@author: DTE_ADMIN
'''
from time import sleep
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
import Util


class Test_IO_Port_settings():

    @pytest.fixture()
    def test_setUp(self):
        Util.init_ChromeDriver(self)
        #Util.init_IE_Driver(self)
        self.driver.maximize_window()
        self.driver.get('http://192.168.0.79')
        yield
        self.defaultValues()
        self.driver.find_element_by_name("action").click()
        self.driver.quit()

    def defaultValues(self):
        self.driver.find_element_by_xpath("//*[@id='failsafeOff']").click()
        Select(self.driver.find_element_by_id("selektor_channel_io1")).select_by_value("inactive")
        Select(self.driver.find_element_by_id("selektor_channel_io2")).select_by_value("inactive")
        Select(self.driver.find_element_by_id("selektor_channel_io3")).select_by_value("inactive")
        Select(self.driver.find_element_by_id("selektor_channel_io4")).select_by_value("inactive")
        self.driver.find_element_by_name("action").click()
        sleep(1)
        self.driver.find_element_by_name("action").click()

    def test_change_Settings(self,test_setUp):
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
        if(self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[1]/tr[1]/td[2]/span").text== "on"):
            flag1= True
        else: 
            flag1= False
        
        if(self.driver.find_element_by_xpath("//*[@id='currmode_channel_io1']/span").text== "Input"):
             flag2= True
        else: 
            flag2= False
        if(self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[2]/tr[2]/td[2]").text== "100"):
             flag3= True
        else: 
            flag3= False
        if(self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[2]/tr[3]/td[2]/span").text== "off"):
             flag4= True
        else: 
            flag4= False
        
        if(self.driver.find_element_by_xpath("//*[@id='currmode_channel_io2']/span").text== "Output"):
             flag5= True
        else: 
            flag5= False
        if(self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[3]/tr[2]/td[2]").text== "2000"):
             flag6= True
        else: 
            flag6= False
        if(self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[3]/tr[3]/td[2]/span").text, "off"):
             flag7= True
        else: 
            flag7= False
        if(self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[3]/tr[4]/td[2]/span").text, "off"):
             flag8= True
        else: 
            flag8= False
        
        if(self.driver.find_element_by_xpath("//*[@id='currmode_channel_io3']/span").text== "RWH RW"):
             flag9= True
        else: 
            flag9= False
        if(self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[4]/tr[2]/td[2]").text== "20"):
             flag10= True
        else: 
            flag10= False
        if(self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[4]/tr[3]/td[2]/span").text== "off"):
             flag11= True
        else: 
            flag11= False
        if(self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[4]/tr[4]/td[2]/span").text== "off"):
             flag12= True
        else: 
            flag12= False
        if(self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[4]/tr[6]/td[2]").text== "200"):
             flag13= True
        else: 
            flag13= False
        if(self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[4]/tr[7]/td[2]").text== "255"):
             flag14= True
        else: 
            flag14= False
        if(self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[4]/tr[8]/td[2]/span").text== "on"):
             flag15= True
        else: 
            flag15= False
        
        if(self.driver.find_element_by_xpath("//*[@id='currmode_channel_io4']/span").text== "Inactive"):
             flag16= True
        else: 
            flag16= False
        
        self.driver.find_element_by_xpath("//input[@name='action']").click()
        assert(flag1==True and flag2==True and flag3==True and
               flag4==True and flag5==True and flag6==True and
               flag7==True and flag8==True and flag9==True and
               flag10==True and flag11==True and flag12==True and 
               flag13==True and flag14==True and flag15==True and 
               flag16==True)
        sleep(1)