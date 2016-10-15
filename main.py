import os
import re
import time
import shutil
import zipfile
import sys

def isgoal(dirs,name):
    global order
    compName=os.path.join(dirs,name)
    if (len(re.findall(r'\b.*.cpp\b',compName))>0) \
       or (len(re.findall(r'\b.*.py\b',compName))>0)\
       or (len(re.findall(r'\b.*.txt\b',compName))>0)\
       and os.path.getsize(compName)<10240:
           #if(os.path.getsize(compName)<512):
               if order:
                   print(name,os.path.getsize(compName),'B','added')
               return True
    return False

def mkdir(dirs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)
        print('create',dirs)
        
def copyFile(source,target):
    if not os.path.exists(target) \
    or(os.path.exists(target) \
    and (os.path.getsize(target) != os.path.getsize(source))):  
        open(target, "wb").write(open(source, "rb").read())

def work():
    global sourcePath,targetPath
    pathLen=len(sourcePath)
    zf=zipfile.ZipFile(zipname,'w',zipfile.zlib.DEFLATED)
    for dirs,folders,nameList in os.walk(sourcePath):
        zf.write(dirs,dirs[pathLen:])
        for name in nameList:
            if isgoal(dirs,name):
                newName=os.path.join(dirs,name)
                zf.write(newName,newName[pathLen:])
    zf.close()

def readInit():
    
    fld={}
    initFile=open('init.ini','r')
    setting=initFile.read()
    exec(setting,fld)
    initFile.close()

    global para
    return tuple([fld[x] for x in para])

def checkPath(path):
    if not os.path.exists(path):
        print('path',path,'is not exists')
        return True
    else:
        return False
    
def checkInput(pac):
    sourcePath,targetPath,copylist,user=pac
    errors=0
    errors+=checkPath(sourcePath)
    errors+=checkPath(targetPath)
    for cppath in copylist:
        errors+=checkPath(cppath)
    if errors>0:
        print('please check if the format of data in init.ini is correct')
    return errors==0
    
para=['sourcePath','targetPath','copylist','user']
command=input('enter "Y" to start\n') or 'N'
if command[0].lower()=='y':
    sourcePath,targetPath,copylist,user=pac=readInit()
    if not checkInput(pac):
        sys.exit()
    
    inputOrder=input('enter "D" to see details while running\n') or 'N'
    order=inputOrder[0].lower()=='d'
    zipname=os.path.join(targetPath,user)+'_'+time.strftime('%Y%m%d')+'.zip'
    
    work()

    for copyPath in copylist:
        shutil.copy(zipname,copyPath)
    print('finished')
"""
version 0.2
updated on 20161015 by scpointer
now where to zip and where to save the .zip file etc. are customizable
"""
