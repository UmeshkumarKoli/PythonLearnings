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

@pytest.mark.DTE601
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
        Select(self.driver.find_element_by_id("selektor_channel_io1")).select_by_value("rwh_cmd26")
        Select(self.driver.find_element_by_id("selektor_channel_io2")).select_by_value("portmode_off")
        Select(self.driver.find_element_by_id("selektor_channel_io3")).select_by_value("portmode_off")        
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
        
        Select(self.driver.find_element_by_id("selektor_channel_io1")).select_by_value("rwh_cmd86")
        Select(self.driver.find_element_by_name("dataHoldTime_io1")).select_by_visible_text("100")
        self.driver.find_element_by_id("dataNumberOfBlocks_io1").send_keys(Keys.CONTROL + "a")
        self.driver.find_element_by_id("dataNumberOfBlocks_io1").send_keys(Keys.DELETE)
        self.driver.find_element_by_id("dataNumberOfBlocks_io1").send_keys("200")
        Select(self.driver.find_element_by_name("dataBlockLength_io1")).select_by_visible_text("255")
        self.driver.find_element_by_id("uidEdgedControlled_on_io1").click()
        
        # IO-1 Settings
        Select(self.driver.find_element_by_id("selektor_channel_io2")).select_by_value("input")
        Select(self.driver.find_element_by_name("dataHoldTime_io2")).select_by_visible_text("2000")
        
        # IO-2 Settings
        Select(self.driver.find_element_by_id("selektor_channel_io3")).select_by_value("output_2b")
        Select(self.driver.find_element_by_name("dataHoldTime_io3")).select_by_visible_text("20")
                
        # Click on Activate and Save
        self.driver.find_element_by_name("action").click()
        
        # Verification
        wait = WebDriverWait(self.driver, 10)
        wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "//*[@id='tblPortconfig']/tbody[1]/tr[1]/td[2]/span")))
        
        if (self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[1]/tr[1]/td[2]/span").text == "on"):
             flag1= True
        else: 
            flag1= False
        if (self.driver.find_element_by_xpath("//*[@id='currmode_channel_io1']/span").text== "RWH CMD (86 bytes)"):
             flag2= True
        else: 
            flag2= False
        if(self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[2]/tr[2]/td[2]").text== "100"):
             flag3= True
        else: 
            flag3= False
        if(self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[2]/tr[6]/td[2]").text== "200"):
             flag4= True
        else: 
            flag4= False
        if(self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[2]/tr[7]/td[2]").text== "255"):
             flag5= True
        else: 
            flag5= False
        if(self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[2]/tr[8]/td[2]/span").text== "on"):
             flag6= True
        else: 
            flag6= False
        
        if(self.driver.find_element_by_xpath("//*[@id='currmode_channel_io2']/span").text== "Input"):
             flag7= True
        else: 
            flag7= False
        if(self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[3]/tr[2]/td[2]").text== "2000"):
             flag8= True
        else: 
            flag8= False
        
        if(self.driver.find_element_by_xpath("//*[@id='currmode_channel_io3']/span").text== "Output (2 bytes)"):
             flag9= True
        else: 
            flag9= False
        if(self.driver.find_element_by_xpath("//*[@id='tblPortconfig']/tbody[4]/tr[2]/td[2]").text== "20"):
             flag10= True
        else: 
            flag10= False
            
        self.driver.find_element_by_xpath("//input[@name='action']").click()
        assert(flag1==True and flag2==True and flag3==True and
               flag4==True and flag5==True and flag6==True and
               flag7==True and flag8==True and flag9==True and
               flag10==True )
        
        sleep(1)