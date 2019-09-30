'''
Created on Aug 26, 2019

@author: DTE_ADMIN
'''
import HTMLTestRunner
import unittest, os

from IO_Port import IO_Port_settings
from Network import Network_Settings 
from Firmware import Firmware_Settings
from Profinet import Profinet_Settings
from SNTP import Sntp_Settings
from System import System_Settings


def main():
    outfile=open(os.getcwd()+"_smokeTestreport.html","w+")
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(IO_Port_settings))
    suite.addTest(unittest.makeSuite(Profinet_Settings))
    suite.addTest(unittest.makeSuite(Firmware_Settings))
    suite.addTest(unittest.makeSuite(Sntp_Settings))
    suite.addTest(unittest.makeSuite(System_Settings))
    suite.addTest(unittest.makeSuite(Network_Settings))
    
    runner = HTMLTestRunner.HTMLTestRunner(
            stream=outfile,
            verbosity=2,
            title='Test the Report',
            description='Result of tests'
            )
    runner.run(suite)
if __name__ == "__main__":
    main()
