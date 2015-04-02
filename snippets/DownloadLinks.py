import urllib
testfile = urllib.URLopener()
f = open('C:\Work\PDS\SampleImages\BuildingImagesLinks.txt','r')
name=0
for line in f:
 try:
  FileNameExtension = line.rsplit('.',1)[1].split('\n')[0].lower()
  if FileNameExtension == 'jpg':
	testfile.retrieve(line,'C:\Work\PDS\SampleImages\RenamingToNumber\\'+str(name)+'.'+FileNameExtension)
	name=name+1
 except:
  pass