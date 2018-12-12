from __future__ import print_function

import glob
import os
import pdb
import re
import shutil
import sys
import time
from VideoCapture import Device

import openpyxl
import win32com.client as comclt
from pywinauto import Application, win32defines
from pywinauto.win32functions import SetForegroundWindow, ShowWindow
from xlrd import open_workbook

from common.Configuration import (captureScreenshot, pre_automation_setup,
                                  readDTC_Report, run_binary_file,
                                  run_CAN_simulator, videoStandard_Hauppauge)
from common.Convert_CPAR import convert_CPAR
from common.Copy_Testcases_From_Oldfirmware import \
    copy_testcases_from_old_firmware
from common.Execute_Complete_TestSuite import execute_CompleteSuite


def main():
    """[summary]
    """
    os.system('cls')
    print("\t*******************************************")
    print("\t***         2D Overlay Tests            ***")
    print("\t*******************************************")

    dirName = os.path.dirname(os.path.abspath(__file__))
    print("\nPlease enter the firmware version to test. \n e.g. OD_4_21_4_PAL or OD_4_23_0_NTSC \n")
    variant_new = raw_input().upper()
    variantType = re.split(r"_\d+_\d+_\d+_", variant_new)[0]
    try:
        videoFormat = re.split(r"_\d+_\d+_\d+_", variant_new)[1]
    except:
        print ("\n Entered firmware version format is incorrect")
        print("\nPlease enter Variant type.\n e.g. OD or DI \n")
        variantType = raw_input().upper()
        print("\nPlease enter valid video standard mode.\n e.g. PAL or NTSC \n")
        videoFormat = raw_input().upper()
    videoStandard_Hauppauge(videoFormat)
    print("\n***********************************************************************\n")

    input_Copy_Yes_No = raw_input(
        "\nDo you want to copy test cases from old firmware folder?\n Please enter  Y,y or N,n \n\n").upper()
    print("\n***********************************************************************\n")
    if (input_Copy_Yes_No == "Y"):
        variant_old = raw_input(
            "\nPlease enter old firmware name to copy test cases \n e.g OD_4_21_4_PAL or OD_4_23_0_NTSC \n\n").upper()
        print("\n***********************************************************************\n")
        os.system('cls')
        if not os.path.exists(r".\%s\%s" % (variantType, variant_old)):
            print("%s doesn't exists" % variant_old)
            print(
                "\nPlease enter correct firmware number E.g OD_4_21_4_PAL or OD_4_23_0_NTSC")
            variant_old = raw_input()
            print(
                "\n***********************************************************************\n")
        if os.path.exists(r".\%s\%s" % (variantType, variant_new)):
            shutil.rmtree(r".\%s\%s" % (variantType, variant_new))
        copy_testcases_from_old_firmware(
            dirName, variantType, variant_old, variant_new)
    else:
        input_Copy_Yes_No="N"
        
    input_CPAR_Yes_No = raw_input(
        "\nDo you want to convert bin files to latest CPAR?\n Enter  Y,y or N,n \n\n").upper()
    print("\n***********************************************************************\n")
    if (input_CPAR_Yes_No == "Y") and (input_Copy_Yes_No == "Y"):
        convert_CPAR(dirName, variantType, variant_old, variant_new,videoFormat)

    if (input_CPAR_Yes_No == "Y")and (input_Copy_Yes_No == "N"):
        variant_old = raw_input(
            "\nPlease enter old firmware name to convert bin files. \n e.g OD_4_21_4_PAL or OD_4_23_0_NTSC \n\n").upper()
        print("\n***********************************************************************\n")
        convert_CPAR(dirName, variantType, variant_old, variant_new,videoFormat)
    else:
        input_CPAR_Yes_No="N"
        
    os.system('cls')
    input_UPDATE_Yes_No = raw_input(
        "\nDo you want to update firmware?\n Enter  Y,y or N,n \n\n").upper()
    print("\n***********************************************************************\n")
    if (input_UPDATE_Yes_No == "Y"):
        su_tool_path_new = (
            r".\%s\%s\EmbeddedSW_Delivery\delivery\su_tools" % (variantType, variant_new))
        if os.path.exists(su_tool_path_new):
            pre_automation_setup(dirName, su_tool_path_new)
        else:
            print ("\n %s does not exists" % su_tool_path_new)
            os.mkdir(su_tool_path_new)
            intergrpath = r"http://URL"
            versionNum = re.findall(r'\d+', variant_new)
            SW_VERSION = versionNum[0] + '.' + \
                versionNum[1] + '.' + versionNum[2]
            os.system(r"svn export %s/SW_%s_V%s/delivery %s\delivery" %
                      (intergrpath, variantType, SW_VERSION, su_tool_path_new))
            os.system(r"svn export %s/SW_%s_V%s/subsystems %s\subsystems" %
                      (intergrpath, variantType, SW_VERSION, su_tool_path_new))
            pre_automation_setup(dirName, su_tool_path_new)
    else:
        input_UPDATE_Yes_No="N"
    print("\n***********************************************************************\n")

    os.system('cls')
    input_Execute_Complete_Yes_No = raw_input(
        "\nDo you want to execute complete suite?\n Enter  Y,y or N,n \n\n").upper()
    print("\n***********************************************************************\n")
    if (input_Execute_Complete_Yes_No == "Y"):
        if (input_UPDATE_Yes_No == "N"):
            run_CAN_simulator()
        testcaseID=""
        execute_CompleteSuite(dirName, variantType, variant_new,testcaseID)
    else:
        input_Execute_Complete_Yes_No="N"

    os.system('cls')
    input_Execute_Single_Yes_No = raw_input(
        " \nDo you want to execute single test?\n Enter  Y,y or N,n \n\n").upper()
    print("\n***********************************************************************\n")
    if (input_Execute_Single_Yes_No == "Y"):
        startAgain = "Y"
        while (startAgain == "Y"):
            print("Enter testcase id. E.g O3M_14929 or O3M_14929\\Step1\n\n")
            testcaseID = raw_input()
            execute_CompleteSuite(dirName, variantType, variant_new,testcaseID)
            print("Do you want to run any other test case? Enter Y,y or N,n \n\n")
            startAgain = raw_input().upper()
    else:
        input_Execute_Single_Yes_No == "N"


if __name__ == '__main__':
    main()
