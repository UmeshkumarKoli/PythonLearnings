import glob
import os
import pdb
import re
import shutil
import sys
import time
from VideoCapture import Device

import win32com.client as comclt
from pywinauto import Application, win32defines
from pywinauto.win32functions import SetForegroundWindow, ShowWindow

from Configuration import readDTC_Report, run_binary_file


def execute_CompleteSuite(dirName, variantType, variant_new,testcaseID):
    """[summary]

      Arguments:
        dirName {[type]} -- [description]
        variantType {[type]} -- [description]
        variant_new {[type]} -- [description]
    """
    su_tool_path = (r".\%s\%s\EmbeddedSW_Delivery\delivery\su_tools" %
                    (variantType, variant_new))
    if not os.path.exists(su_tool_path):
        input_UPDATE_YES_NO = raw_input(
            "EmbeddedSW_delivery folder doesn't exists, Do you want to checkout EmbeddedSW_deliver folder. Enter  Y,y or N,n\n").upper()
        if (input_UPDATE_YES_NO == "Y"):
            intergrpath = r"http://URL"
            versionNum = re.findall(r'\d+', variant_new)
            SW_VERSION = versionNum[0] + '.' + \
                versionNum[1] + '.' + versionNum[2]
            os.system(r"svn export %s/SW_%s_V%s/delivery %s\delivery" %
                      (intergrpath, variantType, SW_VERSION, su_tool_path))
            os.system(r"svn export %s/SW_%s_V%s/subsystems %s\subsystems" %
                      (intergrpath, variantType, SW_VERSION, su_tool_path))
        else:
            execute_CompleteSuite(dirName, variantType, variant_new,testcaseID)

    html = '<html><table border="10"><tr style= position:static><th>TestCaseName</th><th>BaselineImage1</th><th>BaselineImage2</th><th>ActualImage1</th><th>ActualImage2</th><th>DTC Error Status</th><th>Content of CPAR2D bin file</th></tr>'

    executeTestcaseDir = dirName + "\\" + variantType + \
        "\\" + variant_new + "\\" + testcaseID
    if not os.path.exists(executeTestcaseDir):
        print("%s testcase doesn't exists" % testcaseID)
        return
        
    for root, dirs, files in os.walk(executeTestcaseDir):
        for filename in files:
            if filename.startswith(('DSP_CPAR_%s' % variantType)) and filename.endswith('.bin'):
                DSP_file_Path = root + '\\' + filename
                print(
                    "==================================================================================")
                print("Please wait %s testcase is executing" % DSP_file_Path)
                print(
                    "==================================================================================")
                os.system(r"%s\tools\flash_console.exe -p DSP_CPAR -f %s -d %s\tools\flash_drv\FlsDrvInt.bin -c" %
                          (su_tool_path, DSP_file_Path, su_tool_path))
                time.sleep(20)
                print(
                    "==================================================================================")
                print("%s testcase execution finished" % DSP_file_Path)
                print(
                    "==================================================================================")

        for filename in files:
            if filename.startswith(('KP_CPAR_%s' % variantType)) and filename.endswith('.bin'):
                KP_file_Path = root + '\\' + filename
                print(
                    "==================================================================================")
                print("Please wait %s testcase is executing" % KP_file_Path)
                print(
                    "==================================================================================")
                os.system(r"%s\tools\flash_console.exe -p KP_CPAR -f %s -d %s\tools\flash_drv\FlsDrvInt.bin -c" %
                          (su_tool_path, KP_file_Path, su_tool_path))
                time.sleep(20)
                print(
                    "==================================================================================")
                print("%s testcase execution finished" % KP_file_Path)
                print(
                    "==================================================================================")

        for filename in files:
            if filename.startswith(('GP_CPAR_%s' % variantType)) and filename.endswith('.bin'):
                GP_file_Path = root + '\\' + filename
                print(
                    "==================================================================================")
                print("Please wait %s testcase is executing" % GP_file_Path)
                print(
                    "==================================================================================")
                os.system(r"%s\tools\flash_console.exe -p GP_CPAR -f %s -d %s\tools\flash_drv\FlsDrvInt.bin -c" %
                          (su_tool_path, GP_file_Path, su_tool_path))
                time.sleep(20)
                print(
                    "==================================================================================")
                print("%s testcase execution finished" % GP_file_Path)
                print(
                    "==================================================================================")

        for filename in files:
            if filename.startswith(('KP_CPAR2D_%s' % variantType))and filename.endswith('.bin'):
                bfile = filename
                print(
                    "==================================================================================")
                print("Please wait %s testcase is executing" % bfile)
                print(
                    "==================================================================================")

                binFile = root + '\\' + bfile
                Bin2Txt = root + '\\' + ("%s.txt" % bfile)
                os.system(r".\Parameter_conversions\CPAR2DBin_to_Text.exe %s >%s <nul" % (
                    binFile, Bin2Txt))

                files = glob.glob(dirName + r"\Temp_Result/*.jpg")
                for f in files:
                    os.remove(f)
                if os.path.exists(root + r"\DTC_Report.txt"):
                    os.remove(root + r"\DTC_Report.txt")
                if os.path.exists(root + r"\DTC_Report_activeDTCs.txt"):
                    os.remove(root + r"\DTC_Report_activeDTCs.txt")

                run_binary_file(binFile, dirName, root, su_tool_path)
                path = root + '\\' + 'Result'
                if os.path.exists(path):
                    shutil.rmtree(path)
                time.sleep(2)
                os.mkdir(path)

                capturedFile = glob.glob(dirName + r"\Temp_Result/*.jpg")
                count = 1
                for itr in capturedFile:
                    filename = itr
                    fName, ext = os.path.splitext(bfile)

                    destFileName = root + '\\' + 'Result' + \
                        '\\' + fName + '_' + str(count) + ".jpg"
                    os.rename(filename, destFileName)
                    count = count + 1

                files = glob.glob(dirName + r"\Temp_Result/*.jpg")
                for f in files:
                    os.remove(f)
                resultImage = glob.glob(root + r"\Result/*.jpg")
                ExpectedresultImage = glob.glob(root + r"/*.jpg")

                print(
                    "==================================================================================")
                print("%s testcase execution finished" % bfile)
                print(
                    "==================================================================================")

                html += '<tr><td>%s</td>' % bfile
                for countExpectImg in ExpectedresultImage:
                    if len(ExpectedresultImage) == 1:
                        countExpectImg = '.\\' + \
                            re.split((r"%s\\%s" % (variantType, variant_new)),
                                     countExpectImg)[-1]
                        html += '<td><a href="%s"><img src="%s" alt="BaselineImage" width="200" height="200"></a></td>' % (
                            countExpectImg, countExpectImg)
                        html += '<td><a href="%s"><img src="%s" alt="BaselineImage" width="200" height="200"></a></td>' % (
                            countExpectImg, countExpectImg)
                    else:
                        countExpectImg = '.\\' + \
                            re.split((r"%s\\%s" % (variantType, variant_new)),
                                     countExpectImg)[-1]
                        html += '<td><a href="%s"><img src="%s" alt="BaselineImage" width="200" height="200"></a></td>' % (
                            countExpectImg, countExpectImg)
                for countResultImg in resultImage:
                    countResultImg = '.\\' + \
                        re.split((r"%s\\%s" % (variantType, variant_new)),
                                 countResultImg)[-1]
                    html += '<td><a href="%s"><img src="%s" alt="ActualImage" width="200" height="200"></a></td>' % (
                        countResultImg, countResultImg)

                DTC_file = root + r"\DTC_Report_activeDTCs.txt"
                if os.path.exists(DTC_file):
                    DTC_Error_status = readDTC_Report(DTC_file)
                    DTC_file = '.\\' + \
                        re.split(
                            (r"%s\\%s" % (variantType, variant_new)), DTC_file)[-1]
                    html += '<td><a href="%s">%s</a></td>' % (
                        DTC_file, DTC_Error_status)

                Bin2Txt_file = '.\\' + \
                    re.split(
                        (r"%s\\%s" % (variantType, variant_new)), Bin2Txt)[-1]
                html += '<td><a href="%s">%s.txt</a></td>' % (
                    Bin2Txt_file, bfile)
                html += '</tr>'
                # raw_input("Press Enter to continue...")
    html += '</table></html>'
    os.chdir(dirName + "\\" + variantType + "\\" + variant_new)
    if (testcaseID==''):
        file_ = open('result.html', 'w')
        file_.write(html)
        file_.close()
        print("\n Opening result html page")
        os.system('result.html')
    else:
        file_ = open(('result_%s.html' %(testcaseID.replace("\\","_"))), 'w')
        file_.write(html)
        file_.close()
        print("\n Opening result html page")
        os.system('result_%s.html' %(testcaseID.replace("\\","_")))
    os.chdir(dirName)
