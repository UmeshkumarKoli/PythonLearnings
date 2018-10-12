from pdiffer import PDiffer
from itertools import izip
from PIL import Image
import os, time, glob, shutil, pdb

def main():
    #pdb.set_trace()
    dirName= os.path.dirname(__file__)
    pdiff=PDiffer(bin=dirName+r'\perceptualdiff-1.1.1-win\perceptualDiff.exe')
    flag1= False
    flag2= False
    ext= dirName+r'\perceptualdiff-1.1.1-win\perceptualDiff.exe'
    for root, dirs, files in os.walk(dirName+r"\DI"):
        for bfile in files:
            if bfile.endswith('.bin'):
                binFile=root+ '\\'+bfile
                run_binary_file(binFile,dirName)
                
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
                    #print destFileName
                    os.rename(filename,destFileName)
                    count=count+1

                files = glob.glob(dirName+r"\Temp_Result/*.jpg")
                for f in files:
                    os.remove(f)

                resultImage= glob.glob(root+r"\Result/*.jpg")
                ExpectedresultImage= glob.glob(root+r"/*.jpg")
                
                try:
                    #comparing first result file to baseline image files and check it matches with anyone of them.
                    result=isEqual(resultImage[0],ExpectedresultImage[0])
                    print "PercentageDiff=:",result
                    if result>=1.16:
                        print resultImage[0]+' and '+ ExpectedresultImage[0]+' are different'
                    else:
                        flag1=True 
                        print resultImage[0]+' and ' + ExpectedresultImage[0]+' are same'

                    result=isEqual(resultImage[0],ExpectedresultImage[1])
                    print "PercentageDiff=:",result
                    if result>=1.16:
                        print resultImage[0]+ ' and '+ ExpectedresultImage[1]+' are different'
                    else:
                        flag1=True
                        print resultImage[0]+' and '+ ExpectedresultImage[1]+' are same'


                    #comparing second result file to baseline image files and check it matches with anyone of them
                    result=isEqual(resultImage[1],ExpectedresultImage[0])
                    print "PercentageDiff=:",result
                    if result>=1.16:
                        print resultImage[1]+' and '+ ExpectedresultImage[0]+' are different'
                    else:
                        flag2=True 
                        print resultImage[1]+' and ' + ExpectedresultImage[0]+' are same'
                    
                    result=isEqual(resultImage[1],ExpectedresultImage[1])
                    print "PercentageDiff=:",result
                    if result>=1.16:
                        print resultImage[1]+ ' and '+ ExpectedresultImage[1]+' are different'
                    else:
                        flag2=True 
                        print resultImage[1]+' and '+ ExpectedresultImage[1]+' are same'
                except:
                    print "Error occurred: file not found to compare"
                    pass
                if (flag1== True) and(flag2== True):
                    print " Test case "+bfile +" is passed"
                else:
                    print  " Test case "+bfile +" is failed"
                raw_input("Press Enter to continue...")

def run_binary_file(binFile,dirName):
    os.chdir(dirName+r"\su_tool_DI")
    os.system(r"flash_console.exe -p KP_CPAR2D -f %s -d flash_drv\FlsDrvInt.bin" %binFile)
    time.sleep(20)
    #kept this for reference##os.system("start cmd.exe @cmd /k python E:\\2D_Overlay_testing\\O3M_2D_Overlay_Tests\\CPAR_2D_Editor\\TestCaseSuite\\ActivateHauppageApplication.py")
    HauppageFile=dirName+r"\ActivateHauppageApplication.py"
    os.system("python %s" %HauppageFile)
    time.sleep(5)

def isEqual(image1, image2):
    i1=Image.open(image1)
    i2=Image.open(image2)
    pairs = izip(i1.getdata(), i2.getdata())
    if len(i1.getbands()) == 1:
        # for gray-scale jpegs
        dif = sum(abs(p1-p2) for p1,p2 in pairs)
    else:
        dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
     
    ncomponents = i1.size[0] * i1.size[1] * 3
    PercentageDiff= (dif / 255.0 * 100) / ncomponents
    return PercentageDiff

main()
