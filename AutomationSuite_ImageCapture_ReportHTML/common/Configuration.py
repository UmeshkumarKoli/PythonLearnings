import glob
import os
import pdb
import re
import shutil
import subprocess
import sys
import time
from subprocess import PIPE, Popen
from VideoCapture import Device

import win32com.client as comclt
from pywinauto import Application, win32defines
from pywinauto.win32functions import SetForegroundWindow, ShowWindow


def run_binary_file(binFile, dirName, root, su_tool_path):
    """[summary]

      Arguments:
        binFile {[type]} -- [description]
        dirName {[type]} -- [description]
        root {[type]} -- [description]
        su_tool_path {[type]} -- [description]
    """
    os.chdir(su_tool_path)
    os.system(
        r".\tools\flash_console.exe -p KP_CPAR2D -f %s -d .\tools\flash_drv\FlsDrvInt.bin" % binFile)
    time.sleep(20)
    captureScreenshot(dirName)
    time.sleep(5)

    os.system(r".\tools\ReportDTCs ..\Specs\externals\DiagMobCa.cdd  FF >%s" %
              (root + r"\DTC_Report.txt"))
    os.system(r".\tools\ReportDTCs ..\Specs\externals\DiagMobCa.cdd  09 >%s" %
              (root + r"\DTC_Report_activeDTCs.txt"))
    os.chdir(dirName)


def captureScreenshot(dirName):
    """[summary]

      Arguments:
        dirName {[type]} -- [description]
    """
    print("==================================================================================")
    print("Please wait, Save Snapshot function started")
    print("==================================================================================")
    cam = Device(0, 0)
    cam.saveSnapshot(dirName + r"\Temp_Result\screenshot1.jpg")
    time.sleep(3)
    files = glob.glob(dirName + r"\Temp_Result/*.jpg")
    while len(files) > 1:
        os.remove(files[-1])
        files.pop()
    cam.saveSnapshot(dirName + r"\Temp_Result\screenshot2.jpg")
    time.sleep(3)
    files = glob.glob(dirName + r"\Temp_Result/*.jpg")
    while len(files) > 2:
        os.remove(files[-1])
        files.pop()
    del cam
    print("==================================================================================")
    print("Save Snapshot function completed")
    print("==================================================================================")


def run_CAN_simulator():
    """[summary]
    """
    os.system(r".\automationConfig_files\RunCAN_Simulator.bat")
    time.sleep(2)
    app = Application().connect(path=r".\automationConfig_files\MBC_CAN-rx_Simulator.exe")
    w = app.top_window()
    if w.HasStyle(win32defines.WS_MINIMIZE):  # if minimized
        ShowWindow(w.wrapper_object(), 9)  # restore window state
    else:
        SetForegroundWindow(w.wrapper_object())  # bring to front
    wsh = comclt.Dispatch("WScript.Shell")
    for count in range(0, 9):
        wsh.SendKeys("{+}")
    time.sleep(1)
    wsh.SendKeys("{2}")
    for count in range(0, 9):
        wsh.SendKeys("{+}")


def readDTC_Report(DTC_file):
    """[summary]

      Arguments:
        DTC_file {[type]} -- [description]
    """
    print("==================================================================================")
    print("Please wait, Reading DTC_Report_activeDTCs.txt file")
    print("==================================================================================")
    lineNumber = 1
    DTC_Error_status = "No Error Found"
    fp = open(DTC_file)
    for line in fp:
        if lineNumber == 3:
            if line != '\n':
                DTC_Error_status = "Fail, Error found= %s" % line
                return DTC_Error_status
                break
        lineNumber += 1
    fp.close()
    print("==================================================================================")
    print("Reading DTC_Report_activeDTCs.txt file completed")
    print("==================================================================================")
    return DTC_Error_status


def pre_automation_setup(dirName, su_tool_path):
    """[summary]

      Arguments:
        dirName {[type]} -- [description]
        su_tool_path {[type]} -- [description]
    """
    #run_CAN_simulator()
    # change directory because user flash.bat file required relative path to flash files.
    os.chdir(su_tool_path)
    # <nul is added to remove pause effect
    os.system("user_Flash_console_bin.bat < nul")
    os.chdir(dirName)
    os.system(
        r".\automationConfig_files\VirtualSwitchInput.exe .\automationConfig_files\Virtual_input.txt")


def videoStandard_Hauppauge(videoFormat):
    """[summary]

      Arguments:
        videoFormat {[type]} -- [description]
    """
    if not os.path.exists(r"C:\Users\Public\Hauppauge Capture\config.xml"):
        print("**************************************************************************")
        print("Hauppauage is not installed on system. Please install Hauappage.\n")
        print(
            "**************************************************************************\n")
        raw_input("Press any key to exit")
        exit()

    if (videoFormat == "PAL"):
        shutil.copy(r".\automationConfig_files\config_PAL.xml",
                    r".\automationConfig_files\config.xml")
        os.remove(r"C:\Users\Public\Hauppauge Capture\config.xml")
        os.rename(r".\automationConfig_files\config.xml", r"C:\Users\Public\Hauppauge Capture\config.xml")
    elif (videoFormat == "NTSC"):
        shutil.copy(r".\automationConfig_files\config_NTSC.xml",
                    r".\automationConfig_files\config.xml")
        os.remove(r"C:\Users\Public\Hauppauge Capture\config.xml")
        os.rename(r".\automationConfig_files\config.xml", r"C:\Users\Public\Hauppauge Capture\config.xml")
    else:
        print("\n***********************************************************************\n")
        print("\nPlease enter valid video standard mode.\n e.g. PAL or NTSC \n")
        videoFormat = raw_input().upper()
        videoStandard_Hauppauge(videoFormat)
        print("\n***********************************************************************\n")


def getCParVersion_FromExcel(sh, row):
    """[summary]

    Arguments:
        sh {[type]} -- [description]
        row {[type]} -- [description]
    """
    # my_list = [16, 21, 24, 25] # KP_CPAR, DSP, KP_CPAR2D, GP_CPAR

    cell_values = sh.row_slice(rowx=row, start_colx=12, end_colx=15)
    cells = [item.value for item in cell_values]
    values = list(map(int, cells))
    version_string = "_" + \
        str(values[0]) + "_" + str(values[1]) + "_" + str(values[2]) + "_"
    return version_string


def logging_into_Textdata(args, filename, ext):
    """[summary]
    """
    dir = '.\logs'
    if not os.path.exists(dir):
        os.makedirs(dir)
    try:
        subprocess.check_call(args, stdout=open(
            '.\logs\%s.txt' % filename, ext), shell=True)
    except subprocess.CalledProcessError as error:
        print error
