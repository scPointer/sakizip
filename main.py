import os
import re
import time
import shutil
import zipfile


def isgoal(dirs,name):
    global order
    compName=os.path.join(dirs,name)
    if (len(re.findall(r'\b.*.cpp\b',compName))>0) \
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
    global path,targetPath
    pathLen=len(path)
    zf=zipfile.ZipFile(zipname,'w',zipfile.zlib.DEFLATED)
    for dirs,folders,nameList in os.walk(path):
        #newPath=targetPath+dirs[pathLen:]
        #mkdir(newPath)
        zf.write(dirs,dirs[pathLen:])
        #print(newPath)
        for name in nameList:
            if isgoal(dirs,name):
                newName=os.path.join(dirs,name)
                zf.write(newName,newName[pathLen:])
                #shutil.copy(os.path.join(dirs,name),newPath)
                #copyFile(os.path.join(dirs,name),os.path.join(newPath,name))
    zf.close()

command=input('enter "Y" to start\n')
inputOrder=input('enter "D" to see details while running\n')
order=inputOrder[0]=='D' or inputOrder[0]=='d'
if(command[0]=='Y' or command[0]=='y'): 
    path=r'F:\charlotte_code'
    targetPath=r'F:\backups'
    user=r'scpointer'
    zipname=targetPath+user+time.strftime('%Y%m%d')+'.zip'
    work()
    print('finished')
"""
version 0.1
created on 20161011 by scpointer
original version
"""
