import cv2
import sys
import numpy
imgpath = sys.argv[1]
img = cv2.imread(imgpath)
smallx = sys.argv[2]
smally = sys.argv[3]
largex = sys.argv[4]
largey = sys.argv[5]
print int(smally.split(".")[0]),int(largey.split(".")[0]),int( smallx.split(".")[0]),int(largex.split(".")[0])
img1 = img[  int(smally.split(".")[0]):int(largey.split(".")[0]),int( smallx.split(".")[0]):int(largex.split(".")[0]) ]
cv2.imwrite("out.jpg",img1)

