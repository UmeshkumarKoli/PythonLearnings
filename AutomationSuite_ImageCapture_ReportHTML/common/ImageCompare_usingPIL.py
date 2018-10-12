from VideoCapture import Device
from itertools import izip
from PIL import Image
import os, time, glob, shutil, pdb, sys,time
import win32com.client as comclt
from pywinauto import Application, win32defines
from pywinauto.win32functions import SetForegroundWindow, ShowWindow
import cv2
import numpy as np


def main():
    #pdb.set_trace()
    dirName= os.path.dirname(os.path.abspath(__file__))
    
    run_CAN_simulator()
    
    os.system(r".\su_tool\flash_console -p GP_CPAR -f .\su_tool\GP_CPAR.bin -d .\su_tool\flash_drv\FlsDrvInt.bin -c")
    time.sleep(20)
    
    os.system(r".\su_tool\flash_console -p DSP_CPAR -f .\su_tool\DSP_CPAR_zone.bin -d .\su_tool\flash_drv\FlsDrvInt.bin -c")
    time.sleep(20)
    
    os.system(r".\su_tool\VirtualSwitchInput.exe .\su_tool\Virtual_input.txt")
    
    variant= sys.argv[1]
    ##### please comment below line if you want to see output on console.
    sys.stdout = open(dirName+"\\"+variant+'\ResultLog.txt', 'w')
    
    Result_flag1= False
    Result_flag2= False
        
    for root, dirs, files in os.walk(dirName+"\\"+variant):
        for bfile in files:
            if bfile.endswith('.bin'):
                binFile=root+ '\\'+bfile
                files = glob.glob(dirName+r"\Temp_Result/*.jpg")
                for f in files:
                    os.remove(f)
                if os.path.exists(root+r"\DTC_Report.txt"):
                    os.remove(root+r"\DTC_Report.txt")
                run_binary_file(binFile,dirName,root)
                
                path= root+'\\'+'Result'
                if os.path.exists(path):
                    shutil.rmtree(path)
                time.sleep(2)
                os.mkdir(path)
                
                capturedFile= glob.glob(dirName+r"\Temp_Result/*.jpg")
                count=1
                for itr in capturedFile:
                    filename= itr
                    fName, ext=os.path.splitext(bfile)

                    destFileName= root+'\\'+'Result'+'\\'+fName+'_'+str(count)+".jpg"
                    os.rename(filename,destFileName)
                    count=count+1

                files = glob.glob(dirName+r"\Temp_Result/*.jpg")
                for f in files:
                    os.remove(f)

                resultImage= glob.glob(root+r"\Result/*.jpg")
                ExpectedresultImage= glob.glob(root+r"/*.jpg")
                
                try:
                    cnt=0
                    ##comparing first result file to baseline image files and check it matches with anyone of them.
                    print "======================================================================================="
                    for countResultImg in resultImage:
                        for countExpectImg in ExpectedresultImage:
                            result=compareImage(countResultImg,countExpectImg)
                            #print "PercentageDiff=:",result
                            if result==False:
                                if cnt == 0:
                                    Result_flag1= False
                                if cnt == 1:
                                    Result_flag2= False
                                print countResultImg +' and '+ countExpectImg+' are different'
                                print "---------------------------------------------------------------------------------------"
                            else:
                                if cnt == 0:
                                    Result_flag1= True
                                if cnt == 1:
                                    Result_flag2= True
                                cnt=cnt+1
                                print countResultImg+' and ' + countExpectImg +' are same'
                                print "---------------------------------------------------------------------------------------"
                                
                except:
                    print "Error occurred: file not found to compare"
                    print "---------------------------------------------------------------------------------------"
                    pass
                if (Result_flag1== True) and(Result_flag2== True):
                    print " Test case "+bfile +" is passed"
                    print "---------------------------------------------------------------------------------------"
                else:
                    print  " Test case "+bfile +" is failed"
                    print "---------------------------------------------------------------------------------------"
                #raw_input("Press Enter to continue...")
    sys.stdout.close()

def run_binary_file(binFile,dirName, root):
    os.chdir(dirName+r"\su_tool")
    os.system(r"flash_console.exe -p KP_CPAR2D -f %s -d flash_drv\FlsDrvInt.bin" %binFile)
    time.sleep(20)
    captureScreenshot(dirName)
    time.sleep(5)
    os.system(r"ReportDTCs.exe >%s" %(root+r"\DTC_Report.txt"))

def captureScreenshot(dirName):
    cam=Device(0,0)
    cam.saveSnapshot(dirName+r"\Temp_Result\screenshot1.jpg")
    time.sleep(3)
    files = glob.glob(dirName+r"\Temp_Result/*.jpg")
    while len(files)>1:
        os.remove(files[-1])
        files.pop()
    cam.saveSnapshot(dirName+r"\Temp_Result\screenshot2.jpg")
    time.sleep(3)
    files = glob.glob(dirName+r"\Temp_Result/*.jpg")
    while len(files)>2:
        os.remove(files[-1])
        files.pop()
        
def compareImage(img1, img2):
    image1= cv2.imread(img1)
    image2= cv2.imread(img2)
    diff=cv2.subtract(image1, image2)
    #diff = cv2.absdiff(image1, image2)
    mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    imask =  mask>210
    canvas = np.zeros_like(image1, np.uint8)
    canvas[imask] = image1[imask]
    ### Generate diff image using below code
    ### cv2.imwrite(r"E:\2D_Overlay_testing\O3M_2D_Overlay_Tests\CPAR_2D_Editor\TestCaseSuite\Temp_Result\result.jpg", canvas)
    result= not np.any(canvas[imask])
    #result=not np.any(diff)
    return result

def run_CAN_simulator():
    os.system(r".\su_tool\RunCAN_Simulator.bat")
    time.sleep(2)
    app = Application().connect(path=r".\su_tool\MBC_CAN-rx_Simulator.exe")
    w = app.top_window()
    if w.HasStyle(win32defines.WS_MINIMIZE): # if minimized
        ShowWindow(w.wrapper_object(), 9) # restore window state
    else:
        SetForegroundWindow(w.wrapper_object()) #bring to front
    wsh= comclt.Dispatch("WScript.Shell")
    for count in range(0,9):
        wsh.SendKeys("{+}")
    time.sleep(1)
    wsh.SendKeys("{2}")
    for count in range(0,9):
        wsh.SendKeys("{+}")
main()
