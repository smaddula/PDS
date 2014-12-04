import re
import sys

divisionfile = sys.argv[1]

f = open(divisionfile,"r")
division=f.readline()

divisionDimension = []
divisionValue = []

for treesplit in re.findall("dimID\-\d+\ splitVal\-\d+\.\d+",division):
 dimval = re.findall("\d+\.?\d*",treesplit)
 divisionDimension.append(dimval[0])
 divisionValue.append(dimval[1])

print divisionDimension
print divisionValue



