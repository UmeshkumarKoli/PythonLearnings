import os, time, glob, shutil, pdb, sys,time
import cv2
import numpy as np
import shutil

def main():
    #pdb.set_trace()
    dirName= os.path.dirname(os.path.abspath(__file__))
    #DSP_path=r"E:\2D_Overlay_testing\O3M_2D_Overlay_Tests\Development\CPAR_2D_Editor\TestCaseSuite\DSP_CPAR.bin"
    #KP_CPAR_path=r"E:\2D_Overlay_testing\O3M_2D_Overlay_Tests\Development\CPAR_2D_Editor\TestCaseSuite\KP_CPAR.bin"
    GP_CPAR_path=r"E:\2D_Overlay_testing\O3M_2D_Overlay_Tests\Development\CPAR_2D_Editor\TestCaseSuite\GP_CPAR.bin"
    for root, dirs, files in os.walk(dirName+"\\"+"OD\\OD_4_23_0_NTSC"):
        for bfile in files:
            if bfile.endswith('.bin'):
                binFile=root+ '\\'+bfile
                remove_result_folder(root)
                """ DI """"""""""""""
                print"----------------------------------------------------------------------------"
                print"-------------%s starts------------------------------------" %binFile
                
                firstlevel=os.path.dirname(binFile)
                folder2=os.path.basename(firstlevel)
                secondlevel=os.path.dirname(firstlevel)
                folder1=os.path.basename(secondlevel)
                DSP_new=root+'\\'+'DSP_CPAR_DI_4_1_2_'+folder1+'_'+folder2+'.bin'
                KP_CPAR_new=root+'\\'+'KP_CPAR_DI_4_1_2_'+folder1+'_'+folder2+'.bin'
                GP_CPAR_new=root+'\\'+'GP_CPAR_OD_4_1_0_'+folder1+'_'+folder2+'.bin'
                
                #Another way to get folder1 and folder2 is
                #KP_CPAR_path.split("\\")
                #list_dic=KP_CPAR_path.split("\\")
                #list_dic[-3] and list_dic[-2]
                
                shutil.copyfile(DSP_path, DSP_new)
                shutil.copyfile(KP_CPAR_path, KP_CPAR_new)

                print"----------------------------------------------------------------------------"
                print"-------------%s Ends------------------------------------" %binFile
                """
                    
                """"OD """
                print"----------------------------------------------------------------------------"
                print"-------------%s starts------------------------------------" %binFile
               
                firstlevel=os.path.dirname(binFile)
                folder2=os.path.basename(firstlevel)
                secondlevel=os.path.dirname(firstlevel)
                folder1=os.path.basename(secondlevel)
                #DSP_new=root+'\\'+'DSP_CPAR_OD_6_1_2_'+folder1+'_'+folder2+'.bin'
                #KP_CPAR_new=root+'\\'+'KP_CPAR_OD_6_1_2_'+folder1+'_'+folder2+'.bin'
                GP_CPAR_new=root+'\\'+'GP_CPAR_OD_5_0_0_'+folder1+'_'+folder2+'.bin'

                
                #shutil.copyfile(DSP_path, DSP_new)
                #shutil.copyfile(KP_CPAR_path, KP_CPAR_new)
                shutil.copyfile(GP_CPAR_path, GP_CPAR_new)

                print"----------------------------------------------------------------------------"
                print"-------------%s Ends------------------------------------" %binFile
                #"""
                
def remove_result_folder(root):
    path= root+'\\'+'Result'
    if os.path.exists(path):
        shutil.rmtree(path)
   
                
main()
