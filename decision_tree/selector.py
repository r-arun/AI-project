from random import randint
import sys
size = int(sys.argv[1])
total = 690
pr = float(size)/690
pr = int(pr*100)
fd = open('crx.data','rb')
for i in fd:
	i=i.strip()
	r=randint(0,100)
	if(r<pr):
		print i
	
