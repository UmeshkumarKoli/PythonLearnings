'''
Created on Aug 22, 2019

@author: DTE_ADMIN
'''
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def init_ChromeDriver(self):
    self.driver=webdriver.Chrome("..\BrowserDriver\Chrome\chromedriver_76.exe")


def init_IE_Driver(self):
    cap = DesiredCapabilities.INTERNETEXPLORER.copy()
    cap['INTRODUCE_FLAKINESS_BY_IGNORING_SECURITY_DOMAINS'] = True
    cap["nativeEvents"]= False
    cap["unexpectedAlertBehaviour"]= "accept"
    cap["ignoreProtectedModeSettings"]= True
    cap["disable-popup-blocking"]=True
    cap["enablePersistentHover"]= True
    cap["ignoreZoomSetting"]= True
    self.driver=webdriver.Ie(capabilities=cap,executable_path=r'..\BrowserDriver\IE\IEDriverServer_x64_3.14.0\IEDriverServer.exe')