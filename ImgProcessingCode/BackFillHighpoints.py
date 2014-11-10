import cv2
import numpy as np
import gzip
import os

basepath = 'C:\Work\PDS\SampleImages\AllFiles'
outputpathData = 'C:\Work\PDS\SampleImages\AllFiles\OutputData'
outputpathImages = 'C:\Work\PDS\SampleImages\AllFiles\OutputImages'
outputpathFiltered = 'C:\Work\PDS\SampleImages\AllFiles\Blur'

for fname in os.listdir(outputpathData):
 FullfileName = os.path.join(basepath, fname)
 JustFileName = FullfileName.split('\\')[-1]
 FileNameSplit =  JustFileName.split('_')
 noofpoints = FileNameSplit[4].split('.')[0]
 #print noofpoints + ' '+fname
 if int(noofpoints) < 4000:
  #print 'Ignored Reached end of the file'
  continue 
 os.remove(os.path.join(outputpathData,fname))
 FileNameWithoutExtension = FileNameSplit[0]+'_'+FileNameSplit[1]+'_'+FileNameSplit[2]
 JustFileName = FileNameWithoutExtension +'.jpg'
 FullfileName = basepath+'\\'+JustFileName
 #print FullfileName + ' Reached end of the file'
 #continue
 try: 
  img = cv2.imread(FullfileName)
  gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  sift = cv2.SIFT()
  kp ,des = sift.detectAndCompute(gray,None)
  orgkeypoints=len(des)
  
  print 'came here - Original no of keypoints for file name '+FullfileName+'is ' + str(len(des)) + ' '+noofpoints
  if len(des) < 700:
   des = np.vstack((des,des))
   print 'new no of keypoints '+str(len(des))
  elif len(des) > 1500:
   #Applying filter to reduce noise
   #blur = cv2.bilateralFilter(img,9*8,100*8,100*8)
   if (orgkeypoints/1000) < 3:
   	blur = cv2.medianBlur(img, (orgkeypoints/1000)*2+3)
   elif (orgkeypoints/1000) < 4:	
   	blur = cv2.medianBlur(img, (orgkeypoints/1000)*2+1)
   else:	
   	blur = cv2.medianBlur(img, 9)	
   #cv2.imshow("hey",img)
   gray= cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)
   sift = cv2.SIFT()
   kp ,des = sift.detectAndCompute(gray,None)
   img=cv2.drawKeypoints(gray,kp,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
   print 'blurred image number of keypoints - '+str(len(des))
   #cv2.imwrite('C:\\Work\\KeyPointsblur.jpg',img)
   #cv2.imwrite( outputpathFiltered+'\\'+FileNameWithoutExtension+'_insterestpoints_'+str(len(kp))+'.'+FileNameExtension,blur)

  img=cv2.drawKeypoints(gray,kp,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
  #cv2.imwrite( outputpathImages+'\\'+FileNameWithoutExtension+'_insterestpoints_'+str(len(kp))+'.'+FileNameExtension,img)
  #f = gzip.open(outputpathData+'\\'+FileNameWithoutExtension+'_points_'+str(len(kp))+'.txt.gz','wb')
  #cv2.imwrite( outputpathImages+'\\'+FileNameWithoutExtension+'_insterestpoints_'+str(len(kp))+'.'+FileNameExtension,img)
  f = gzip.open(outputpathData+'\\'+FileNameWithoutExtension+'_points_'+str(len(kp))+'.txt.gz','wb')
  
  for item in des: 
   for dimvalue in item:
    f.write(str(dimvalue)+' ')
   f.write(FileNameWithoutExtension+'\n')
  f.close()
 except:
  pass 
 