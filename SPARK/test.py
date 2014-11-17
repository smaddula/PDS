import numpy as np
from cStringIO import StringIO
import os
import module
data = [1, 2, 3, 4, 5]
from pyspark import SparkConf, SparkContext
conf = (SparkConf()
         .setMaster("local")
         .setAppName("My app")
         .set("spark.executor.memory", "1g"))
sc = SparkContext( conf = conf)

def red (a , b):
	print str(a)+" "+str(b)
	return a*a+b*b

distData = sc.parallelize(data)
x= distData.map(lambda a: a).reduce(lambda a,b: red(a,b))
print x
