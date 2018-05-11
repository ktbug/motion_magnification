#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 10:11:19 2018

@author: Katie Kosak
## CFSA, Warwick University
### Uses Dr. Sergei Anfinogentov's Motion Magnification Code
### This code enables the use of video formats with the code
## Requirements: ffmpeg
## Tested with Windows OS and Linux
"""

from magnify import *
import cv2
from matplotlib import pyplot as plt
import numpy as np
from matplotlib import animation
import os
import os.path
import subprocess
from tempfile import mkdtemp

## Animation Settings ############
# Not needed with the Matplotlib format
#Writer = animation.writers['ffmpeg']
#writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=180)

# Have  a mp4 file converted into a data cube ##################
filename='London.mp4'
title=filename[:-4]
cap = cv2.VideoCapture(filename)
frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

temp_file= os.path.join(mkdtemp(), 'newfile.dat')
input_data = np.memmap('temp_file.myarray', dtype=np.float64, mode='w+',
              shape=(frameCount, frameHeight, frameWidth,3))
fc = 0
ret = True

while (fc < frameCount  and ret):
    ret, input_data[fc] = cap.read()
    fc += 1

cap.release()

############### Convert RGB Data to 1 Color Stream ################
input_data=np.average(input_data,axis=3)

###################### MOtion Magnification ###########################
k= 15#Magnification
width= 90 # width
result = magnify_motions_2d(input_data, k, width)


################### Time Distance Map ##################################
#plt.figure()
#plt.title('Magnification x 15')
#plt.imshow(input_data[:,:,150].T,cmap='Greys')
#plt.xlabel('Time (Frame)')
#plt.ylabel('Pixel')
#plt.show()
#plt.savefig('modelx1-butter-from-0.5-to-10-alpha-20-lambda_c-80-chromAtn-0.png')
#
################## Save the Movie as mp4 ##################

############# Create a folder of images to save memory ##########
subfolder='Data'
try:
    os.mkdir(subfolder)
except Exception:
    pass
# Change to the directory
os.chdir(subfolder)

## Now create the images 
#### Note: The images but be in integer format
### Example Test_1.png then Test_2.png
for i in range(frameCount):
    plt.figure()
    plt.imshow(result[i],cmap='gray')  
    plt.savefig(title+'_'+str(i)+'.png')
    plt.close()
## Change back to former directory
os.chdir('..')
###### Animage the png files in the folder ##########
 #Movie Name
result_movie=title+'_Mx'+str(k)+'.mp4'

filepath1=os.path.join( os.path.dirname(os.path.realpath("__file__")),subfolder)
params='ffmpeg -framerate 25 -i ' + str(title)+'_%d.png '+ result_movie
p=subprocess.Popen(params,cwd=filepath1,shell=True)
