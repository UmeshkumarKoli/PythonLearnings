import os
import time
import glob
import shutil
import pdb
import sys
import time
import re
import subprocess
import openpyxl
from xlrd import open_workbook

from Configuration import getCParVersion_FromExcel


def convert_CPAR(dirName, variantType, variant_old, variant_new,videoFormat):
    """[summary]

      Arguments:
        dirName {[type]} -- [description]
        variantType {[type]} -- [description]
        variant_old {[type]} -- [description]
        variant_new {[type]} -- [description]
    """
    intergrpath = r"http://dettsvn.tt.de.ifm/svn/sy/libraries/esw/products/o3mxxx/software/integration/tags"
    su_tool_path_old = (r".\%s\%s\EmbeddedSW_Delivery" %
                        (variantType, variant_old))
    if not os.path.exists(su_tool_path_old):
        inputYES_NO = raw_input(
            "%s does not exists.\n Enter ' Y,y' to update EmbeddedSW_Delivery folder.\n Enter ' N,n' to enter another firmware name.\n" % su_tool_path_old).upper()
        if (inputYES_NO == "Y"):
            os.mkdir(su_tool_path_old)
            versionNum = re.findall(r'\d+', variant_old)
            SW_VERSION = versionNum[0] + '.' + \
                versionNum[1] + '.' + versionNum[2]
            if not os.path.exists(r"%s\delivery" % su_tool_path_old):
                os.system(r"svn export %s/SW_%s_V%s/delivery %s\delivery" %
                          (intergrpath, variantType, SW_VERSION, su_tool_path_old))
            if not os.path.exists(r"%s\subsystems" % su_tool_path_old):
                os.system(r"svn export %s/SW_%s_V%s/subsystems %s\subsystems" %
                          (intergrpath, variantType, SW_VERSION, su_tool_path_old))
        if (inputYES_NO == "N"):
            variant_old = raw_input(
                "Please enter correct firmware name where EmbeddedSW_Delivery folder exists. E.g OD_4_21_4 or OD_4_23_0_NTSC\n\n")
            convert_CPAR(dirName, variantType, variant_old, variant_new)

    su_tool_path_new = (r".\%s\%s\EmbeddedSW_Delivery" %
                        (variantType, variant_new))
    if not os.path.exists(su_tool_path_new):
        os.mkdir(su_tool_path_new)

    versionNum = re.findall(r'\d+', variant_new)
    SW_VERSION = versionNum[0] + '.' + versionNum[1] + '.' + versionNum[2]

    if not os.path.exists(r"%s\delivery" % su_tool_path_new):
        os.system(r"svn export %s/SW_%s_V%s/delivery %s\delivery" %
                  (intergrpath, variantType, SW_VERSION, su_tool_path_new))
    if not os.path.exists(r"%s\subsystems" % su_tool_path_new):
        os.system(r"svn export %s/SW_%s_V%s/subsystems %s\subsystems" %
                  (intergrpath, variantType, SW_VERSION, su_tool_path_new))

    datafile = (r".\%s\%s\EmbeddedSW_Delivery\delivery\Specs\externals\Mobilkamera_compatibility.xls" % (
        variantType, variant_new))
    book = open_workbook(datafile)
    sh = book.sheet_by_index(0)

    for root, dirs, files in os.walk(dirName + "\\" + variantType + "\\" + variant_new):
        for filename in files:
            if filename.startswith(('DSP_CPAR_%s' % variantType)) and filename.endswith('.bin'):
                old_dir_walk=re.sub((r'%s_\d+_\d+_\d+_%s' %(variantType, videoFormat)), variant_old, root)
                for root_old, dirs_old, files_old in os.walk(old_dir_walk):
                    for filename_old in files_old:
                        if filename_old.startswith(('DSP_CPAR_%s' % variantType)) and filename_old.endswith('.bin'):
                            DSP_file_Path_Old=  root_old + '\\'+filename_old
                DSP_version = getCParVersion_FromExcel(sh, 21)
                filename_new = re.sub(r'_\d_\d_\d_', DSP_version, filename)
                DSP_file_Path_New = root + '\\' + filename_new
                os.rename(root + '\\' + filename,root + '\\' + filename_new)
                os.system(r".\Parameter_conversions\convert_DSPCPAR.bat %s %s %s %s" % (
                    su_tool_path_old, DSP_file_Path_Old, su_tool_path_new, DSP_file_Path_New))

        for filename in files:
            if filename.startswith(('KP_CPAR_%s' % variantType)) and filename.endswith('.bin'):
                old_dir_walk=re.sub((r'%s_\d+_\d+_\d+_%s' %(variantType, videoFormat)), variant_old, root)
                for root_old, dirs_old, files_old in os.walk(old_dir_walk):
                    for filename_old in files_old:
                        if filename_old.startswith(('KP_CPAR_%s' % variantType)) and filename_old.endswith('.bin'):
                            KP_file_Path_Old=  root_old + '\\'+filename_old
                KP_version = getCParVersion_FromExcel(sh, 16)
                filename_new = re.sub(r'_\d_\d_\d_', KP_version, filename)
                KP_file_Path_New = root + '\\' + filename_new
                os.rename(root + '\\' + filename,root + '\\' + filename_new)
                os.system(r".\Parameter_conversions\Convert_KPCPAR.bat %s %s %s %s" % (
                    su_tool_path_old, KP_file_Path_Old, su_tool_path_new, KP_file_Path_New))

        for filename in files:
            if filename.startswith(('GP_CPAR_%s' % variantType)) and filename.endswith('.bin'):
                old_dir_walk=re.sub((r'%s_\d+_\d+_\d+_%s' %(variantType, videoFormat)), variant_old, root)
                for root_old, dirs_old, files_old in os.walk(old_dir_walk):
                    for filename_old in files_old:
                        if filename_old.startswith(('GP_CPAR_%s' % variantType)) and filename_old.endswith('.bin'):
                            GP_file_Path_Old= root_old + '\\' + filename_old
                GP_version = getCParVersion_FromExcel(sh, 25)
                filename_new = re.sub(r'_\d_\d_\d_', GP_version, filename)
                GP_file_Path_New = root + '\\' + filename_new
                os.rename(root + '\\' + filename,root + '\\' + filename_new)
                os.system(r".\Parameter_conversions\Convert_GPCPAR.bat %s %s %s %s" % (
                    su_tool_path_old, GP_file_Path_Old, su_tool_path_new, GP_file_Path_New))

        for filename in files:
            if filename.startswith(('KP_CPAR2D_%s' % variantType))and filename.endswith('.bin'):
                old_dir_walk=re.sub((r'%s_\d+_\d+_\d+_%s' %(variantType, videoFormat)), variant_old, root)
                for root_old, dirs_old, files_old in os.walk(old_dir_walk):
                    for filename_old in files_old:
                        if filename_old.startswith(('KP_CPAR2D_%s' % variantType)) and filename_old.endswith('.bin'):
                            KP2D_file_Path_Old= root_old + '\\' + filename_old
                KP2D_version = getCParVersion_FromExcel(sh, 24)
                filename_new = re.sub(r'_\d_\d_\d_', KP2D_version, filename)
                KP2D_file_Path_New = root + '\\' + filename_new
                os.rename(root + '\\' + filename,root + '\\' + filename_new)
                os.system(r".\Parameter_conversions\Convert_KPCPAR2D.bat %s %s %s %s" % (
                        su_tool_path_old, KP2D_file_Path_Old, su_tool_path_new, KP2D_file_Path_New))
                #raw_input("Press Enter to continue...")

    for parent, dirnames, filenames in os.walk(dirName + "\\" + variantType + "\\" + variant_new):
        for files in filenames:
            if files.lower().endswith('.txt'):
                os.remove(os.path.join(parent, files))
            path = parent + '\\' + 'Result'
            if os.path.exists(path):
                shutil.rmtree(path)
