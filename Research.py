# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np

vectores=0
nvectores=0
mvector=0
res=0
fs=0
coef=0
formt=0
mod=0
nc=0
Fs=0
ver = 1

with open("C:\\Users\\MAHE\\Desktop\\research@mit\\DataSet\\0000\\0000f00.fpg", "rb") as f:
    
    id = f.read(4)
    if((id[0]!=70)|(id[1]!=80)|(id[2]!=71)|(id[3]!=32)):
        print('Error: The file is not FPG')
    else:
        print((id[0:3]))
    
    hsize = np.fromfile(f, dtype=np.uint16)[0]
    
    
    
    if((hsize == 48)|(hsize == 60)):
        ver =2
    #print(ver)
    f.seek(6)
    #print(f.tell())
    formt = np.fromfile(f, dtype=np.uint16)[0]
    #print(formt)
    #print(formt,"format")#np.fromfile(f, dtype=np.uint16))
    if(formt == 4):
        f.seek(8)
        m = np.fromfile(f, dtype=np.uint16)[0]
        f.seek(10)
        can = np.fromfile(f, dtype=np.uint16)[0]
        
        #print(m,can)
        f.seek(12)
        Ts = np.fromfile(f, dtype=np.uint32)[0]
        f.seek(16)
        res = np.fromfile(f, dtype=np.uint16)[0]
        #print(Ts,res)
        f.seek(18)
        f.seek(4,1)
        #print(f.tell())
        coef = np.fromfile(f, dtype=np.uint32)[0]
        f.seek(26)
        mvector = np.fromfile(f, dtype=np.uint32)[0]
        f.seek(30)
        nvectores = np.fromfile(f, dtype=np.uint32)[0]
        f.seek(34) 
        nc = np.fromfile(f, dtype=np.uint16)[0]
        f.seek(36)
        if(ver == 2):
            Fs = np.fromfile(f, dtype=np.uint32)[0]
            f.seek(40)
            mventana =np.fromfile(f, dtype=np.uint32)[0]
            f.seek(44)
            msolapadas =np.fromfile(f, dtype=np.uint32)[0]
            f.seek(48)
        f.seek(hsize-12)
        #print(f.tell())
        datos = np.fromfile(f, dtype=np.uint32)[0]
        f.seek(hsize-8)
        #print(f.tell())
        delta = np.fromfile(f,dtype = np.uint32)[0]
        f.seek(hsize-4)
        ddelta=delta = np.fromfile(f,dtype = np.uint32)[0]
        f.seek(hsize)
                   
        tam_tot = nvectores*can*mvector
        #print(f.tell())
        if res ==8:
            temp = np.fromfile(f,dtype = np.uint8)
            f.seek(61)
        elif res ==16:
            temp = np.fromfile(f,dtype = np.uint16)
            f.seek(62)
        elif res ==32:
            temp = np.fromfile(f,dtype = np.float32)
            f.seek(64)
        else:
            temp = np.fromfile(f,dtype = np.float64)
            f.seek(68)
        #print(f.tell())
        h=0
        #print(len(temp))
        vectores = np.zeros([nvectores,mvector]) 
        for i in range(0,nvectores):
            for m in range(0,mvector):
                vectores[i][m] = temp[h]
                h=h+1
        #print(vectores)
    else:
        vectores = np.zeros([0,0])
f.close()
            
        
    