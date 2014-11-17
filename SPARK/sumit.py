from __future__ import division
import numpy as np
from cStringIO import StringIO
import os
import module

numDim = 2

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

inp = sc.textFile("Testinput.txt")
MapOutput = inp.map(lambda s: InitializeAndReturnPair(s,False))

print MapOutput.collect()


#inp = sc.textFile("IO/largefile.txt")
#MapOutput = inp.map(lambda s: InitializeAndReturnPair(s,True))

for loop in xrange(0,1):

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
#	print Mean
	

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

	splitDict = dict()
	for n in splitvariance:
		splitDict[n[0]] = n[1]

#	SplitVals = MapOutput.map(lambda a: SplitVectors(splitDict, a[1])).collect()
	MapOutput = MapOutput.map(lambda a: SplitVectors(splitDict, a[1]))
	print "-------------Values After the Split----------------"
	print MapOutput.collect()
#MapOutput.saveAsTextFile("outputtt")
