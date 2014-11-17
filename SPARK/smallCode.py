from __future__ import division
import numpy as np
from cStringIO import StringIO
import os
import module

numDim = 128

def addVec(self,r):
	a = module.InterestPoint_Info()
	a.key = self.key
	for n in xrange(0,numDim):
		a.vector[n] = self.vector[n] + r.vector[n]
	return a


def divide(self,val):
	a = module.InterestPoint_Info()
	a.key = self.key
	for n in xrange(0,numDim):
		a.vector[n] =  self.vector[n]/val
	return a

def InitializeAndReturnPair(string,first=False):
	vec = module.InterestPoint_Info(string,first)
	return vec.key,vec


def FindSquareDeviation(meanVals,self):
	keyMean = meanVals[self.key]
	a=module.InterestPoint_Info()
	a.key = self.key;
	for n in xrange(0,numDim):
		a.vector[n] = (keyMean.vector[n]-self.vector[n])*(keyMean.vector[n]-self.vector[n])
	a.filename = "No_Name"
	return a 

def FindMaxVarAndDimensionID(interestpoint_info,meanVals):
	a = module.DimSplit(0,0)
	maxvalue=0
	for n in xrange(0,numDim):
		if maxvalue < interestpoint_info.vector[n]:
			maxvalue = interestpoint_info.vector[n]
			a.dimId = n
	a.splitVal = meanVals[interestpoint_info.key].vector[a.dimId]
	return a
	
def SplitVectors(dimsplitVals, interestpoint_info):
	a = module.InterestPoint_Info()
	interestpoint_info.clone(a)
	splitdimension = dimsplitVals[interestpoint_info.key].dimId
	splitval = dimsplitVals[interestpoint_info.key].splitVal
	if (interestpoint_info.vector[splitdimension] > splitval):
		a.key=2*interestpoint_info.key+1
	else:
		a.key=2*interestpoint_info.key
	return a.key,a

#configuring spark
from pyspark import SparkConf, SparkContext
conf = (SparkConf()
         .setMaster("local")
         .setAppName("My app")
         .set("spark.executor.memory", "1g"))
sc = SparkContext( conf = conf)
sc.addPyFile(os.path.join("/home/sid/Downloads/spark/pdsWork/module.py"))

#inp = sc.textFile("Testinput.txt")
#MapOutput = inp.map(lambda s: InitializeAndReturnPair(s,False))

f=open('division.txt','wb')

inp = sc.textFile("IO/testlargefile.txt")
MapOutput = inp.map(lambda s: InitializeAndReturnPair(s,True))
numIter = 2
for loop in xrange(0,numIter):

	MapOutput.cache()	

	#counting the distinct keys returned from the map -> to make sure this matches with the reduce we have written below the print
	#Counting distinct by converting to set which can only hold distinct elements then printing length . 
	#Commented the lines below since things are working fine
	#out = list(set(MapOutput.map(lambda a: a[1].key).collect()))
	#print len(out)

	# Finding Mean by adding vectors and dividing them with number of vectors per each key

	CountPerKey = MapOutput.countByKey()
	print len(CountPerKey)
	Mean = MapOutput.reduceByKey(lambda a,b : addVec(a,b)).map(lambda s: divide(s[1],CountPerKey[s[0]])).collect()
	MeanDict=dict()
	for n in Mean:
		MeanDict[n.key] = n
	

	#finding Variance
	splitvariance = MapOutput.map(lambda a: (a[0],FindSquareDeviation(MeanDict,a[1])) ).reduceByKey(lambda x,y : addVec(x,y)).map(lambda l:(l[0],FindMaxVarAndDimensionID(l[1],MeanDict)) ).collect()
	print "----------------Length of the mean---------------"
	print len(Mean)
#	print "----------------Mean-----------------------------"
#	print Mean
	print "----------------Mean Dictionary------------------"
	for n in Mean:
		print n
	print "----------------Split----------------------------"
	print splitvariance
	f.write(str(splitvariance))

	splitDict = dict()
	for n in splitvariance:
		splitDict[n[0]] = n[1]

#	SplitVals = MapOutput.map(lambda a: SplitVectors(splitDict, a[1])).collect()
	MapOutput = MapOutput.map(lambda a: SplitVectors(splitDict, a[1]))
	print "-------------Values After the Split----------------"

#MapOutput.saveAsTextFile("outputtt")
#Doing this in nasty way since the feature is still in development
#http://apache-spark-user-list.1001560.n3.nabble.com/Write-1-RDD-to-multiple-output-paths-in-one-go-tc14174.html

MapOutput.cache()
keyStart=2**numIter
for n in xrange(0,2**numIter):
	key = keyStart+n
	MapOutput.filter(lambda x: x[0] == key).saveAsTextFile("diroutput/"+str(key))

