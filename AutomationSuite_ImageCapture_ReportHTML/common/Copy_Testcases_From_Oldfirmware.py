import glob
import os
import pdb
import re
import shutil
import sys
import time

from Configuration import logging_into_Textdata


def copy_testcases_from_old_firmware(dirName, variantType, variant_old, variant_new):
    """[summary]

      Arguments:
        dirName {[type]} -- [description]
        variantType {[type]} -- [description]
        variant_old {[type]} -- [description]
        variant_new {[type]} -- [description]
    """
    shutil.copytree(r".\%s\%s" % (variantType, variant_old), r".\%s\%s" % (
        variantType, variant_new), ignore=shutil.ignore_patterns('*EmbeddedSW_Delivery*'))
    su_tool_path_old = (r".\%s\%s\EmbeddedSW_Delivery" %
                        (variantType, variant_old))
    su_tool_path_new = (r".\%s\%s\EmbeddedSW_Delivery" %
                        (variantType, variant_new))
    if not os.path.exists(su_tool_path_new):
        os.mkdir(su_tool_path_new)
        intergrpath = r"http://dettsvn.tt.de.ifm/svn/sy/libraries/esw/products/o3mxxx/software/integration/tags"
        versionNum = re.findall(r'\d+', variant_new)
        SW_VERSION = versionNum[0] + '.' + versionNum[1] + '.' + versionNum[2]

        delivery = (r"svn export --force %s/SW_%s_V%s/delivery %s\delivery" %
                    (intergrpath, variantType, SW_VERSION, su_tool_path_new))
        delivery_filename = 'delivery'
        print("\nExporting %s folder from svn..." % delivery_filename)
        logging_into_Textdata(delivery, delivery_filename, 'a+')

        sub_systems = (r"svn export %s/SW_%s_V%s/subsystems %s\subsystems" %
                       (intergrpath, variantType, SW_VERSION, su_tool_path_new))
        subsystems_filename = 'sub_systems'
        print("\nExporting %s folder from svn..." % subsystems_filename)
        logging_into_Textdata(sub_systems, subsystems_filename, 'a+')

    DSP_CPAR_FILE = (
        r"%s\subsystems\externals\dsp_delivery\DSP_CPAR.bin" % su_tool_path_new)
    GP_CPAR_FILE = (
        r"%s\subsystems\externals\gp_delivery\GP_CPAR.bin" % su_tool_path_new)
    KP_CPAR_FILE = (
        r"%s\subsystems\externals\kp_delivery\KP_CPAR.bin" % su_tool_path_new)
    KP_CPAR2D = (r"%s\subsystems\externals\kp_delivery\kp_cpar2D.bin" %
                 su_tool_path_new)

    walk_Dir = os.path.join(dirName, variantType, variant_new)

    for parent, dirnames, filenames in os.walk(walk_Dir):
        for files in filenames:
            if (("_%s_" % variantType) in files) and files.lower().endswith('.bin'):
                os.remove(os.path.join(parent, files))
            if files.lower().endswith('.txt') or files.lower().endswith('.7z') or files.lower().endswith('.html'):
                os.remove(os.path.join(parent, files))
            path = parent + '\\' + 'Result'
            if os.path.exists(path):
                shutil.rmtree(path)
    for parent, dirnames, filenames in os.walk(walk_Dir):
        for dirs in dirnames:
            if dirs.startswith('Step'):
                shutil.copyfile(DSP_CPAR_FILE, parent + "\\" + dirs + "\\" + "DSP_CPAR_" + variantType +
                                "_0_0_0_" + os.path.basename(os.path.dirname(parent + "\\" + dirs)) + "_" + dirs + ".bin")
                shutil.copyfile(GP_CPAR_FILE, parent + "\\" + dirs + "\\" + "GP_CPAR_" + variantType +
                                "_0_0_0_" + os.path.basename(os.path.dirname(parent + "\\" + dirs)) + "_" + dirs + ".bin")
                shutil.copyfile(KP_CPAR_FILE, parent + "\\" + dirs + "\\" + "KP_CPAR_" + variantType +
                                "_0_0_0_" + os.path.basename(os.path.dirname(parent + "\\" + dirs)) + "_" + dirs + ".bin")
                shutil.copyfile(KP_CPAR2D, parent + "\\" + dirs + "\\" + "KP_CPAR2D_" + variantType +
                                "_0_0_0_" + os.path.basename(os.path.dirname(parent + "\\" + dirs)) + "_" + dirs + ".bin")
    print("\nSucessfully copied the Old Firmware hierarchy to the New Firmware hierarchy!!!")
    print(
        "\n***********************************************************************\n")
