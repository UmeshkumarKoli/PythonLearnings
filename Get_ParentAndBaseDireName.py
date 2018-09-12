import os
def main():
    """
    Problem: I want to get name of Parent folder and base folder
             from path E:\testing\RegressionSuite\Development\Editor\TestCaseSuite\Umesh\Firmware_1_26_2
    Function: In this function, For loop searches for each directories and sub directories and searches for dir name= Test_Step
    Expected Result:
            "Parent folder= TestFolder1
             Basefolder   = Test_Step_1
    """
    for parent, dirnames, filenames in os.walk(r"E:\testing\RegressionSuite\Development\Editor\TestCaseSuite\Umesh\Firmware_1_26_2"):
        for dirs in dirnames:
            if dirs.startswith('Test_Step'):
                outputname= os.path.basename(os.path.dirname(parent+"\\"+dirs))
                print "Parent folder=%s" %outputname
                print "Basefolder   =%s" %dirs
                

main()
