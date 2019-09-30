'''
Created on Sep 24, 2019

@author: DTE_ADMIN
'''
import unittest


class Test(unittest.TestCase):


    def testName(self):
        a=False
        b=True
        c= False
        
        if ((a==False) and (b==False) and (c==False)):
            pass
        else:
            print a, b, c
            raise AssertionError
        #assert (a,b,c)==(True, False, False)
        
        #self.assertEquals((1,1) and (2,2) and(3,3))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()