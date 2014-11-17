import numpy as np
from cStringIO import StringIO

numDim = 128
class InterestPoint_Info:
	def __str__(self):
		file_str = StringIO()
		file_str.write(str(self.key)) 
		file_str.write(" ")
		for n in self.vector:
			file_str.write(str(n)) 
			file_str.write(" ")
		file_str.write(self.filename) 
		return file_str.getvalue()
	def clone(self,r):
		r.key = self.key
		r.filename = self.filename
		for n in xrange(0,numDim):
			r.vector[n] = self.vector[n]
	def __repr__(self):
		return str(self) 
	def __init__(self,txt="",initial=False):
		if len(txt)==0:
			self.vector = np.arange(numDim,dtype=np.float)
			self.filename = "no Name"
			self.key = 0
			return
    		split_text = txt.split()
		if initial == False:
			self.key = int(split_text[0].split(".")[0])
    			self.vector = np.array([float(v) for v in split_text[1:numDim+1]])
			self.filename=split_text[numDim+1]
		else:
			self.key = 1
    			self.vector = np.array([float(v) for v in split_text[0:numDim]])
			self.filename=split_text[numDim]

class DimSplit:
	def __init__(self,dimId,splitVal):
		self.dimId = dimId
		self.splitVal = splitVal
	def __str__(self):
		return "dimID-" + str(self.dimId)+" splitVal-"+str(self.splitVal)
	def __repr__(self):
		return str(self) 
