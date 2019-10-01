'''
Created on Aug 14, 2019

@author: DTE_ADMIN
'''
from time import sleep
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

import Util


class Test_Network_Settings():

    def set_NetworkIP(self,firstPartIP, secondPartIP, thirdPartIP,fourthPartIP):
        self.driver.find_element_by_xpath("//input[@name='ip0']").send_keys(firstPartIP)
        self.driver.find_element_by_xpath("//input[@name='ip1']").send_keys(secondPartIP)
        self.driver.find_element_by_xpath("//input[@name='ip2']").send_keys(thirdPartIP)
        self.driver.find_element_by_xpath("//input[@name='ip3']").send_keys(fourthPartIP)
    
    def set_SubnetMaskIP(self,firstPartIP, secondPartIP, thirdPartIP,fourthPartIP):  
        self.driver.find_element_by_xpath("//input[@name='sn0']").send_keys(firstPartIP)
        self.driver.find_element_by_xpath("//input[@name='sn1']").send_keys(secondPartIP)
        self.driver.find_element_by_xpath("//input[@name='sn2']").send_keys(thirdPartIP)
        self.driver.find_element_by_xpath("//input[@name='sn3']").send_keys(fourthPartIP)
    
    def set_GateWayIP(self,firstPartIP, secondPartIP, thirdPartIP,fourthPartIP):
        self.driver.find_element_by_xpath("//input[@name='gw0']").send_keys(firstPartIP)
        self.driver.find_element_by_xpath("//input[@name='gw1']").send_keys(secondPartIP)
        self.driver.find_element_by_xpath("//input[@name='gw2']").send_keys(thirdPartIP)
        self.driver.find_element_by_xpath("//input[@name='gw3']").send_keys(fourthPartIP)
        
    def reset_Network(self):
        self.set_NetworkIP("192", "168","0","79")
        self.set_SubnetMaskIP("255", "255","255","0")
        self.set_GateWayIP("192", "168","0","79")
        self.driver.find_element_by_xpath("//*[@type='submit']").click()
        
    @pytest.fixture()
    def test_setUp(self):
        Util.init_ChromeDriver(self)
        #Util.init_IE_Driver(self)
        self.driver.maximize_window()
        self.driver.get('http://192.168.0.79')
        yield
        self.reset_Network()
        self.driver.quit()
        
    def test_Change_Network_Settings(self,test_setUp):
        self.driver.find_element_by_xpath("//*[@id='ipconfig']/a").click()
        self.driver.switch_to_frame("center")
        #sleep(2)
        wait=WebDriverWait(self.driver,10)
        wait.until(expected_conditions.visibility_of_element_located((By.XPATH,"//input[@name='ip0']")))
        self.driver.find_element_by_xpath("//input[@name='ip0']").click()
        self.set_NetworkIP("192", "168","0","79")
        self.set_SubnetMaskIP("255", "255","255","0")
        self.set_GateWayIP("192", "168","0","79")
        
        self.driver.find_element_by_xpath("//*[@type='submit']").click()
        sleep(5)
        error_respose=self.driver.find_element_by_xpath("//*[@id='contentIframe']/p").text
#         if(error_respose=="ERROR: The TCP/IP reconfiguration has been rejected because, compared to the current settings, the submitted settings contained no changes."):
#             print "Tests pass: Error message shown on page"
#         else:
#             print "Tests Fail: Error message not displayed"
#         
        if (error_respose== "ERROR: The TCP/IP reconfiguration has been rejected because, compared to the current settings, the submitted settings contained no changes."):
            flag1= True
        else: 
            flag1= False
        self.set_NetworkIP("192", "168","0","101")
        self.set_SubnetMaskIP("255", "255","255","0")
        self.set_GateWayIP("192", "168","0","79")
        
        self.driver.find_element_by_xpath("//*[@type='submit']").click()
        success_response=self.driver.find_element_by_xpath("//*[@id='contentIframe']/p[1]").text
#         if(success_response=="The IP settings have been accepted."):
#             print "Tests Pass: Network Ip setting have been saved"
#         else:
#             print "Tests Fail: Network Ip setting change message not found"

        if(success_response=="The IP settings have been accepted."):
            flag2= True
        else: 
            flag2= False
        sleep(2)
        self.driver.find_element_by_xpath("//*[@id='contentIframe']/p[3]/a").click()
            
        #element= wait.until(expected_conditions.visibility_of_element_located("//*[@id='ipconfig']/a"), "Network menu")
        sleep(2)
        self.driver.find_element_by_xpath("//*[@id='ipconfig']/a").click()
        self.driver.switch_to_frame("center")
        #wait.until(expected_conditions.visibility_of_element_located("//input[@name='ip0']"),"wait for ip address")
        newIP_address_Label=self.driver.find_element_by_xpath("//*[@id='contentIframe']//tbody/tr[2]/td[2]").text
#         if(newIP_address_Lable=="192.168.0.101"):
#             print "Tests Pass: New IP address 192.168.0.101 is showing on page"
#         else:
#             print "Tests Fail: New IP address is showing %s on page" %newIP_address_Lable

        if(newIP_address_Label,"192.168.0.101"):
            flag3= True
        else: 
            flag3= False
        
        assert(flag1==True and flag2==True and flag3==True)