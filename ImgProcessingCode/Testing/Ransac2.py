import numpy as np
import cv2
from matplotlib import pyplot as plt
import random

def drawKeyPoints(img, template, skp, tkp, num=-1):
    h1, w1 = img.shape[:2]
    h2, w2 = template.shape[:2]
    nWidth = w1+w2
    nHeight = max(h1, h2)
    minHeight = min(h1,h2)
    hdif = (nHeight-minHeight)/2
    newimg = np.zeros((nHeight, nWidth, 3), np.uint8)
    newimg[0:h2, :w2] = template
    newimg[:h1, w2:w1+w2] = img

    maxlen = min(len(skp), len(tkp))
    if num < 0 or num > maxlen:
        num = maxlen
    for i in range(num):
        pt_a = (int(tkp[i].pt[0]), int(tkp[i].pt[1]+hdif))
        pt_b = (int(skp[i].pt[0]+w2), int(skp[i].pt[1]))
        cv2.line(newimg, pt_a, pt_b, (255, 0, 0))
    return newimg


def drawMatches(img1, kp1, img2, kp2, matches):
    """
    My own implementation of cv2.drawMatches as OpenCV 2.4.9
    does not have this function available but it's supported in
    OpenCV 3.0.0

    This function takes in two images with their associated 
    keypoints, as well as a list of DMatch data structure (matches) 
    that contains which keypoints matched in which images.

    An image will be produced where a montage is shown with
    the first image followed by the second image beside it.

    Keypoints are delineated with circles, while lines are connected
    between matching keypoints.

    img1,img2 - Grayscale images
    kp1,kp2 - Detected list of keypoints through any of the OpenCV keypoint 
              detection algorithms
    matches - A list of matches of corresponding keypoints through any
              OpenCV keypoint matching algorithm
    """

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
        print int(x1),int(y1), int(x2),int(y2)
        cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (random.randint(0,255), random.randint(0,255), random.randint(0,255)), 1)


    # Show the image
    cv2.namedWindow("image",cv2.WINDOW_NORMAL)
    cv2.imshow("image", out)
    cv2.waitKey(0)	
    #cv2.imshow('Matched Features', out)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

img1 = cv2.imread('paris_defense_000047.jpg',0)          # queryImage
#img1 = cv2.imread('paris_eiffel_000005.jpg',0)          # queryImage

#img2 = cv2.imread('paris_defense_000124.jpg',0) # trainImage
img2 = cv2.imread('paris_eiffel_000028.jpg',0) # trainImage


# Initiate SIFT detector
sift = cv2.SIFT()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

for i in des1:
 sum=0
 for j in xrange(128):
  sum=sum+i[j]
 for j in xrange(128):
  i[j]=i[j]/sum
for i in des2:
 sum=0
 for j in xrange(128):
  sum=sum+i[j]
 for j in xrange(128):
  i[j]=i[j]/sum

  
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)

flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(des1,des2,k=2)

# store all the good matches as per Lowe's ratio test.
good = []
for m,n in matches:
    if m.distance < 0.7*n.distance:
        good.append(m)
img3 = drawMatches(img1,kp1,img2,kp2,good)
#img3 = drawKeyPoints(img1,img2, kp1,kp2,good)
#cv2.namedWindow("image",cv2.WINDOW_NORMAL)
#cv2.imshow("image", img3)
#cv2.waitKey(0)
#plt.imshow(img3, 'gray'),plt.show()