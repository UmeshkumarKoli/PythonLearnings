'''
Created on Aug 14, 2019

@author: DTE_ADMIN
'''
from time import sleep
import unittest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

import Util


class Network_Settings(unittest.TestCase):

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
    
    def setUp(self):
        Util.init_ChromeDriver(self)
        #Util.init_IE_Driver(self)
        self.driver.maximize_window()
        self.driver.get('http://192.168.0.79')

    def test_Start(self):
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
        sleep(2)
        error_respose=self.driver.find_element_by_xpath("//*[@id='contentIframe']/p[@class='resp_error']").text
#         if(error_respose=="ERROR: The TCP/IP reconfiguration has been rejected because, compared to the current settings, the submitted settings contained no changes."):
#             print "Test pass: Error message shown on page"
#         else:
#             print "Test Fail: Error message not displayed"
#         
        self.assertEqual(error_respose, "ERROR: The TCP/IP reconfiguration has been rejected because, compared to the current settings, the submitted settings contained no changes.")
        self.set_NetworkIP("192", "168","0","101")
        self.set_SubnetMaskIP("255", "255","255","0")
        self.set_GateWayIP("192", "168","0","100")
        
        self.driver.find_element_by_xpath("//*[@type='submit']").click()
        success_response=self.driver.find_element_by_xpath("//*[@id='contentIframe']/p[1]").text
#         if(success_response=="The IP settings have been accepted."):
#             print "Test Pass: Network Ip setting have been saved"
#         else:
#             print "Test Fail: Network Ip setting change message not found"

        self.assertEqual(success_response,"The IP settings have been accepted.")
        sleep(2)
        self.driver.find_element_by_xpath("//*[@id='contentIframe']/p[3]/a").click()
            
        #element= wait.until(expected_conditions.visibility_of_element_located("//*[@id='ipconfig']/a"), "Network menu")
        sleep(2)
        self.driver.find_element_by_xpath("//*[@id='ipconfig']/a").click()
        self.driver.switch_to_frame("center")
        #wait.until(expected_conditions.visibility_of_element_located("//input[@name='ip0']"),"wait for ip address")
        newIP_address_Label=self.driver.find_element_by_xpath("//*[@id='contentIframe']//tbody/tr[2]/td[2]").text
#         if(newIP_address_Lable=="192.168.0.101"):
#             print "Test Pass: New IP address 192.168.0.101 is showing on page"
#         else:
#             print "Test Fail: New IP address is showing %s on page" %newIP_address_Lable

        self.assertEqual(newIP_address_Label,"192.168.0.101")
        
    def tearDown(self):
        self.reset_Network()
        self.driver.quit()
    
if __name__ == "__main__":
    unittest.main()
# suite = unittest.TestSuite()
# suite.addTest(unittest.makeSuite(Network_Settings))
# output=open(r"E:\DTE_WebServer_Automation\DTEWebServer\Test\Network_Settings.html",'w+')    
# runner = HTMLTestRunner.HTMLTestRunner(
#         stream=output,
#         title='Test the Report',
#         description='Result of tests'
#         )
# runner.run(suite)