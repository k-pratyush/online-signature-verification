# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


# PARAMETERS:
# filename -> Name of the .fpg file
# showXY   -> Set this parameter to '1' to show XY signature image (Handritten image).
# showWV   -> Set this parameter to '1' to show signature parameter waveforms.
# 
# RESULTS:
# x   -> X coordinate sequence.             Original Range -> [0 - 12699]
# y   -> Y coordinate sequence.             Original Range -> [0 - 9649]
# z   -> Pressure coordinate sequence.      Range -> [0 - 1024]
# az  -> Pen Azimuth coordinate sequence.   Range -> [0 - 360]
# inn  -> Pen Elevation coordinate sequence. Range -> [0 - 90]
# pps -> Sampling rate (Points Per Second).


# in variable (MATLAB) -> inn (python)


# NOTE:
# In the database provided with this M-file, X and Y coordinates have been normalized
# in order to force the begining of each signature at (X,Y)=(0,0) coordinate.
# Due to this, current XY range is not the one shown above
#

import numpy as np
import matplotlib.pyplot as plt

def FPG_Signature_Read(filename, showXY, showWV):

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

    ##Windows
    # with open("C:\\Users\\MAHE\\Desktop\\research@mit\\DataSet\\0000\\0000f00.fpg", "rb") as f:

    ##Mac
    with open(filename, "rb") as f:
        
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


    #Plotting
    x = vectores[:,0]
    y = vectores[:,1]
    z = vectores[:,2]
    # print(x)
    # print(y)
    # print(z)
            
    az = vectores[:,3]
    inn = vectores[:,4]
    pps = Fs

    if(showXY == 1):
        fig = plt.figure(1)
        p0 = min(vectores[:,2])
        #print(p0)
        #print(type(vectores[:,2]))
        ind_p0 = np.where(vectores[:,2] == p0)[0]
        #print(ind_p0)
        vnan = np.ones([len(ind_p0),1])
        vnan[:] = np.nan
        #print(vnan)
        x = vectores[:,0]
        x2 = x
        x2[ind_p0][0] = vnan
        #print(x2)
        y = vectores[:,1];
        y2 = y
        y2[ind_p0][0] = vnan
        alto = max(y2)-min(y2)
        ancho = max(x2) - min(x2)
        relacion = alto/ancho
        plt.plot(x2,y2,'k',2)
        #locs, labels = plt.xticks()

        '''
        plt.tick_params(
            axis='y',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            labelbottom=False) # labels along the bottom edge are off
        '''

        ##This works too
        #plt.xticks([],[])
        #plt.yticks([],[])

        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())


        if(showWV != 1):
            plt.show()

    if(showWV == 1):
        plt.figure(2)
        plt.title(filename)
        l = len(x)

        plt.subplot(5,1,1)
        plt.plot(x)
        plt.ylabel('X')
        plt.axis([0, l, min(x), max(x)])

        plt.subplot(5,1,2)
        plt.plot(y)
        plt.ylabel('Y')
        plt.axis([0, l, min(y), max(y)])

        plt.subplot(5,1,3)
        plt.plot(z)
        plt.ylabel('Pressure')
        plt.axis([0, l, min(z), max(z)])

        plt.subplot(5,1,4)
        plt.plot(az)
        plt.ylabel('Azimuth')
        plt.axis([0, l, min(az), max(az)])

        plt.subplot(5,1,5)
        plt.plot(inn)
        plt.ylabel('Elevation')
        plt.axis([0, l, min(inn), max(inn)])

        plt.show()

#Example
# FPG_Signature_Read("MCYT_Signature_100/0042/0042f13.fpg", 1, 1)
FPG_Signature_Read("MCYT_Signature_100/0000/0000f01.fpg", 1, 0)
# FPG_Signature_Read("MCYT_Signature_100/0000/0000f02.fpg", 0, 1)
# FPG_Signature_Read("MCYT_Signature_100/0000/0000f03.fpg", 0, 0)
