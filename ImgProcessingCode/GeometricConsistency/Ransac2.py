import sys
import numpy as np
import cv2
from matplotlib import pyplot as plt
import random
import math
import os
import urllib

InputPath = "input"
DatasetPath = "http://s3-us-west-2.amazonaws.com/pdsoxfordimages"
#DatasetPath = "/home/sid/Downloads/oxfordDataset/oxbuild_images"

OutputPath = "output"

def eucledianDistance(a,b):
 sum = 0
 for i in xrange(1,127):
  sum = sum + (a[i]-b[i])*(a[i]-b[i])
 return math.sqrt(sum) 

def drawMatches(img1, kp1, img2, kp2, matches,mask,DrawImage=1):

    # Create a new output image that concatenates the two images together
    # (a.k.a) a montage
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]

    out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')

    # Place the first image to the left
    out[:rows1,:cols1,:] = np.dstack([img1, img1, img1])

    # Place the next image to the right of it
    out[:rows2,cols1:cols1+cols2,:] = np.dstack([img2, img2, img2])

    # For each pair of points we have between both images
    # draw circles, then connect a line between them
    print len(matches)
    counter  =0 
    for mat in matches:
        # Get the matching keypoints for each of the images
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        # x - columns
        # y - rows
        (x1,y1) = kp1[img1_idx].pt
        (x2,y2) = kp2[img2_idx].pt

        # Draw a small circle at both co-ordinates
        # radius 4
        # colour blue
        # thickness = 1
        cv2.circle(out, (int(x1),int(y1)), 4, (255, 0, 0), 1)   
        cv2.circle(out, (int(x2)+cols1,int(y2)), 4, (255, 0, 0), 1)

        # Draw a line in between the two points
        # thickness = 1
        # colour blue
        #        print int(x1),int(y1), int(x2),int(y2)
        degree = math.degrees(math.atan2((y2-y1),(x2-x1)))
        #cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (random.randint(0,255), random.randint(0,255), random.randint(0,255)), 2)
        
		#using static angle here to draw outliers and inliers in different colors
        if mask[counter][0] != 0:
         cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (random.randint(0,255), random.randint(0,255), random.randint(0,255)), 1)
         #print degree,int(x1),int(y1), int(x2),int(y2)
         cv2.putText(out, str(int(degree)) , (int(x1),int(y1)),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)
         #cv2.putText(out, str(x2)+','+str(y2) , (int(x2+cols1),int(y2)),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0))
        else:
         #cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (255,255,255), 1)
         cv2.putText(out, str(int(degree)) , (int(x2+cols1),int(y2)),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)
        
        counter = counter + 1

    if DrawImage == 1:
     # Show the image
     cv2.namedWindow("image",cv2.WINDOW_NORMAL)
     cv2.imshow("image", out)
     cv2.waitKey(0)	
     #cv2.imshow('Matched Features', out)
     #cv2.waitKey(0)
     #cv2.destroyAllWindows()
    return out 

def FindClosestMatches( img1,kp1,des1,sift,path2 , DrawImage = 0 ,writeToFile = -1):
 #img1 = cv2.imread('images/'+'paris_moulinrouge_000106.jpg',0)
 #img1 = cv2.imread('images/'+'paris_defense_000047.jpg',0)
 #img1 = cv2.imread('images/'+'paris_louvre_000142.jpg',0)          # queryImage
 #img1 = cv2.imread('images/'+'paris_eiffel_000005.jpg',0)          # queryImage
 #img1 = cv2.imread('images/'+'defense_1.jpg',0)
 #img2 = cv2.imread('images/'+'paris_moulinrouge_000103.jpg',0)
 #img2 = cv2.imread('images/'+'paris_defense_000124.jpg',0) # trainImage
 #img2 = cv2.imread('images/'+'paris_louvre_000141.jpg',0) # trainImage
 #img2 = cv2.imread('images/'+'paris_eiffel_000028.jpg',0) # trainImage
 #img2 = cv2.imread('images/'+'defense_2.jpg',0)

 req = urllib.urlopen(path2)
 arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
 img2 = cv2.imdecode(arr,0)

 #img2 = cv2.imread(path2,0)
 # Initiate SIFT detector
 
 
 # find the keypoints and descriptors with SIFT
 kp2, des2 = sift.detectAndCompute(img2,None)
 '''
 for i in des1:
  sum=0
  for j in xrange(128):
   sum=sum+i[j]
  for j in xrange(128):
   i[j]= math.sqrt( i[j]/sum )
 for i in des2:
  sum=0
  for j in xrange(128):
   sum=sum+i[j]
  for j in xrange(128):
   i[j]=math.sqrt(i[j]/sum)
 '''
   
 FLANN_INDEX_KDTREE = 0
 index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
 search_params = dict(checks = 50)
 
 flann = cv2.FlannBasedMatcher(index_params, search_params)
 
 matches = flann.knnMatch(des1,des2,k=2)
 Rmatches = flann.knnMatch(des2,des1,k=2)
 
 # store all the good matches as per Lowe's ratio test.
 good = []
 Rgood = []
 newgood=[]
 pts1 = []
 pts2 = []
 
 print 'total number of matches initially ',len(matches)
 
 #ratio test
 for m,n in matches:
     if m.distance < 0.8*n.distance:
      good.append(m)
      #pts2.append(kp2[m.trainIdx].pt)
      #pts1.append(kp1[m.queryIdx].pt)
 for m,n in Rmatches:
     if m.distance < 0.8*n.distance:
      Rgood.append(m)
      #pts2.append(kp2[m.trainIdx].pt)
      #pts1.append(kp1[m.queryIdx].pt)
 
 print 'matches after ratio test ',len(good)
 	 
 symmgood = []
 #symmetry test
 for m in good:
  for n in Rgood:
   if m.trainIdx == n.queryIdx:
    if m.queryIdx == n.trainIdx: 
     symmgood.append(m)
    else:
     ed1 = eucledianDistance(des1[m.queryIdx],des2[m.trainIdx])
     ed2 = eucledianDistance(des2[n.queryIdx],des1[n.trainIdx])
     print 'eucledianDistance ',ed1,ed2
     if ( ed1/ed2 > 0.8 and ed1<ed2 ) or ( ed2/ed1 > 0.8 and ed2<ed1 ):
      print 'hey .. edge case :)'
      symmgood.append(m)	
    # if 
 #for m in good:
 # symmgood.append(m)
 
 print 'vectors after symmetric check ',len(symmgood)
 
 for m in symmgood:
  pts2.append(kp2[m.trainIdx].pt)
  pts1.append(kp1[m.queryIdx].pt)
 
 pts2 = np.float64(pts2)
 pts1 = np.float64(pts1)
 mask = []
 F, mask = cv2.findFundamentalMat(pts1,pts2,cv2.FM_RANSAC,10.0,0.99)
 
 
 print len(mask)
 sum=0
 for i in mask:
  sum = sum+ (1 if not i==0 else 0)
 print 'vectors after ransac check ',sum
 
 if DrawImage == 1 or writeToFile != -1:
  img3 = drawMatches(img1,kp1,img2,kp2,symmgood,mask,DrawImage)
 if writeToFile != -1:
  cv2.imwrite( OutputPath+ '/'+str(writeToFile)+'.jpg',img3)
 return sum
 

AllFilesDelimited = sys.argv[1]
InputimagePath = sys.argv[2]

if not os.path.exists(OutputPath):
    os.makedirs(OutputPath)  
SearchImages=[]
out=[]
print "came here"
#for f in os.listdir(InputPath):
 #if not os.path.isdir(f):
inputimage= InputimagePath
 #break
for f in AllFilesDelimited.split(":"):
 #if not os.path.isdir(f):
 SearchImages.append(DatasetPath+'/'+f)

print SearchImages
print out
'''
if not os.path.exists(OutputPath):
    os.makedirs(OutputPath)  
SearchImages=[]
out=[]
for f in os.listdir(InputPath):
 if not os.path.isdir(f):
  inputimage= InputPath+ '/'+f
  break
for f in os.listdir(DatasetPath):
 if not os.path.isdir(f):
  SearchImages.append(DatasetPath+'/'+f)
'''
sift = cv2.SIFT()
img1 = cv2.imread(inputimage,0)
kp1, des1 = sift.detectAndCompute(img1,None)

print "came here aswell after reading input points"

for img in SearchImages:
 out.append( (FindClosestMatches(img1,kp1, des1,sift,img,0),img))

out.sort(reverse=True)
#best match will be the same image at index 0
FindClosestMatches(img1,kp1, des1,sift,out[0][1],0,0)
FindClosestMatches(img1,kp1, des1,sift,out[1][1],0,1)
'''FindClosestMatches(img1,kp1, des1,sift,out[2][1],0,2)
FindClosestMatches(img1,kp1, des1,sift,out[3][1],0,3)
FindClosestMatches(img1,kp1, des1,sift,out[4][1],0,4)'''
