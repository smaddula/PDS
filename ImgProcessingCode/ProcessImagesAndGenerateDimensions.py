import cv2
import numpy as np
import gzip
import os

#Takes input a directory and generates a text file with feature with all the jpg files present inside the folder.
#Doesnot recursively dive into the subfolders
#Generates the file in gzip format to save space (saved by atleast 80%)
#Places the output files in the same folder #TODO - make changes to save in different folders - Done

DoSmoothing = 1

basepath = '/home/sid/Downloads/oxfordDataset/OxfordJunk/graffiti'
outputpathImages = '/home/sid/Downloads/oxfordDataset/OutputImages'
outputpathFiltered = '/home/sid/Downloads/oxfordDataset/Blur'
writetosinglefile = 1
if writetosinglefile == 1:
 outputpathData = '/home/sid/Downloads/oxfordDataset/OxfordJunkVectors'
else:
 outputpathData = '/home/sid/Downloads/oxfordDataset/OutputDataSingle'

if not os.path.exists(outputpathData):
    os.makedirs(outputpathData)

if not os.path.exists(outputpathImages):
    os.makedirs(outputpathImages)

	
if not os.path.exists(outputpathFiltered):
    os.makedirs(outputpathFiltered)


if writetosinglefile == 1:
 f = open(outputpathData+'/Output.txt','wb')
	
count = 0
blurredimages = 0
totalvectors = 0
for fname in os.listdir(basepath):
 #if count == 10:
 # break
 count = count +1
 FullfileName = os.path.join(basepath, fname)
 if os.path.isdir(FullfileName):
  continue 
 JustFileName = FullfileName.split('/')[-1]
 FileNameWithoutExtension = JustFileName.split('.',1)[0]
 FileNameExtension = FullfileName.split('.',1)[1]
 if FileNameExtension.lower() != 'jpg':
  continue
 try: 
  img = cv2.imread(FullfileName)
  gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  sift = cv2.SIFT()
  kp ,des = sift.detectAndCompute(gray,None)
  orgkeypoints=len(des)
  
  print 'no of keypoints ' + str(len(des)) , count,fname
  #if len(des) < 700:
  #des = np.vstack((des,des))
  # print 'new no of keypoints '+str(len(des))
  #elif len(des) > 1500:
  if len(des) > 1500 and DoSmoothing == 1:
   #Applying filter to reduce noise
   #blur = cv2.bilateralFilter(img,9*8,100*8,100*8)
   blurredimages = blurredimages + 1
   if (orgkeypoints/1000) < 3:
   	blur = cv2.medianBlur(img, (orgkeypoints/1000)*2+3)
   elif (orgkeypoints/1000) < 4:	
   	blur = cv2.medianBlur(img, (orgkeypoints/1000)*2-1)
   else:	
    blur = cv2.medianBlur(img, 9)
   #blur = cv2.medianBlur(img, (orgkeypoints/1000)*2-9)	
   #cv2.imshow("hey",img)
   gray= cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)
   sift = cv2.SIFT()
   kp ,des = sift.detectAndCompute(gray,None)
   #img=cv2.drawKeypoints(gray,kp,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
   print 'blurred image number of keypoints - '+str(len(des))
   #cv2.imwrite('C:\\Work\\KeyPointsblur.jpg',img)
   if count < 200:
    cv2.imwrite( outputpathFiltered+'/'+FileNameWithoutExtension+'_insterestpoints_'+str(len(kp))+'.'+FileNameExtension,blur)

  #img=cv2.drawKeypoints(gray,kp,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
  #cv2.imwrite( outputpathImages+'/'+FileNameWithoutExtension+'_insterestpoints_'+str(len(kp))+'.'+FileNameExtension,img)
  #f = gzip.open(outputpathData+'\\'+FileNameWithoutExtension+'_points_'+str(len(kp))+'.txt.gz','wb')
  #cv2.imwrite( outputpathImages+'\\'+FileNameWithoutExtension+'_insterestpoints_'+str(len(kp))+'.'+FileNameExtension,img)
  if writetosinglefile == 0 :
   f = gzip.open(outputpathData+'/'+FileNameWithoutExtension+'_points_'+str(len(kp))+'.txt.gz','wb')
  
  totalvectors = totalvectors + len(des)
  for item in des: 
   for dimvalue in item:
    f.write(str(dimvalue)+' ')
   f.write(FileNameWithoutExtension+'\n')
  if writetosinglefile == 0:
   f.close()
 except:
  pass 

print 'total number of vectors ',totalvectors
print 'total no of images compressed ',blurredimages
if writetosinglefile == 1:
 f.close()

