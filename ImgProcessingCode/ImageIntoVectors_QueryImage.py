import sys
import cv2
import numpy as np
import gzip
import os
 
#Takes input a directory and generates a text file with feature with all the jpg files present inside the folder.
#Doesnot recursively dive into the subfolders
#Generates the file in gzip format to save space (saved by atleast 80%)
#Places the output files in the same folder #TODO - make changes to save in different folders - Done
  
FullfileName = sys.argv[1]
numargs = len(sys.argv)
if numargs>4:
 smallx = sys.argv[2]
 smally = sys.argv[3]
 largex = sys.argv[4]
 largey = sys.argv[5]
 #sessionid = sys.argv[6]


if not os.path.isfile(FullfileName):
    sys.exit()
JustFileName = FullfileName.split('\\')[-1]

FileNameWithoutExtension = JustFileName.split('.',1)[0]
FileNameExtension = FullfileName.split('.',1)[1]
if FileNameExtension.lower() != 'jpg':
 sys.exit()
#print FileNameWithoutExtension
#print FileNameExtension
#print JustFileName
#print FullfileName
try:
 img = cv2.imread(FullfileName)
 if numargs>4:
  img = img[  int(smally.split(".")[0]):int(largey.split(".")[0]),int( smallx.split(".")[0]):int(largex.split(".")[0]) ]
 gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
 sift = cv2.SIFT()
 kp ,des = sift.detectAndCompute(gray,None)
 #print des
 orgkeypoints=len(des)
 #print 'came here - Original no of keypoints ' + str(len(des))
 if len(des) > 1500:
  #Applying filter to reduce noise
  #blur = cv2.bilateralFilter(img,9*8,100*8,100*8)
  if (orgkeypoints/1000) < 3:
  	blur = cv2.medianBlur(img, (orgkeypoints/1000)*2+3)
  elif (orgkeypoints/1000) < 4:	
  	blur = cv2.medianBlur(img, (orgkeypoints/1000)*2-1)
  else:	
   blur = cv2.medianBlur(img, 9)
  gray= cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)
  sift = cv2.SIFT()
  kp ,des = sift.detectAndCompute(gray,None)
 
 for item in des:
  i=0
  for dimvalue in item:
   sys.stdout.write(str(dimvalue))
   if i != 127:
    sys.stdout.write('+')
   i=i+1
  sys.stdout.write('\n')
 #if numargs > 4: 
 # if not os.path.exists("out/"+sessionid+"/inputImage"):
 #  os.makedirs("out/"+sessionid+"/inputImage")
 # cv2.imwrite("out/"+sessionid+"/inputImage/cropped.jpg",img)

 #print len(des)
except:
 #print "Unexpected error:", sys.exc_info()[0]
 pass
