
f = open('AllItems.txt', 'r')

dic_count_keys = dict()
for line in f:
	key = int( line.split()[0].split(".")[0])
	if key in dic_count_keys:
		dic_count_keys[key] = dic_count_keys[key]+1
	else:
		dic_count_keys[key]=1

for i in dic_count_keys:
	print str(i)+" "+str(dic_count_keys[i])
