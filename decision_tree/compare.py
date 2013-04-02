from random import randint
import sys
f1 = sys.argv[1]
f2 = sys.argv[2]
fd = open(f1,'rb')
arr1 = []
for i in fd:
	i =i.strip()
	arr1.append(i[-1])
fd = open(f2,'rb')
arr2 = []
for i in fd:
	i =i.strip()
	arr2.append(i[-1])
counter = 0
total = 0
for i,j in zip(arr1,arr2):
	total +=1
	if(i==j): counter +=1
	#else: print "Mismatch",total
#print counter,total,float(counter)/total
print float(counter)/total*100
