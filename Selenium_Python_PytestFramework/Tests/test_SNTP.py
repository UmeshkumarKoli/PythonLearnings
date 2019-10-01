'''
Created on Sep 19, 2019

@author: DTE_ADMIN
'''
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
import Util

@pytest.mark.DTE_COMMON
class Test_Sntp_Settings():

    @pytest.fixture()
    def test_setUp(self):
        Util.init_ChromeDriver(self)
        #Util.init_IE_Driver(self)
        self.driver.maximize_window()
        self.driver.get('http://192.168.0.79')
        yield
        
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
        if (self.driver.find_element_by_css_selector("#contentIframe tr[class='row_odd']  span").text == "on"):
            flag1= True
        else: 
            flag1= False
            
        if(self.driver.find_element_by_css_selector("#contentIframe tbody tr:nth-child(3) td:nth-child(2)").text== "192.168.0.5"):
            flag2= True
        else: 
            flag2= False
        if(self.driver.find_element_by_css_selector("#contentIframe tbody tr:nth-child(4) td:nth-child(2)").text== "UTC+5:30"):
            flag3= True
        else: 
            flag3= False
        self.driver.switch_to_default_content()
        self.driver.find_element_by_css_selector('#sntpconfig > a').click()
        self.driver.switch_to_frame("center")
        wait=WebDriverWait(self.driver,10)
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR,"input[type='radio']:nth-child(1)")))
        if(self.driver.find_element_by_css_selector("#sntpcfgForm tr:nth-child(3) td:nth-child(2)").text== "192.168.0.5"):
            flag4= True
        else: 
            flag4= False
        if(self.driver.find_element_by_css_selector("#sntpcfgForm tr:nth-child(4) td:nth-child(2)").text== "UTC+5:30"):
            flag5= True
        else: 
            flag5= False
        assert(flag1==True and flag2==True and flag3==True and flag4==True and flag5==True)  
              
    def test_SNTP_Settings(self,test_setUp):
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
