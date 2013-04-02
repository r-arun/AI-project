from random import randint
import sys
import math
def binary_search2(arr,start,end,value):
	if(start>end): return None
	if(start==end): 
		if(arr[start]<= value):
			return start
		return None
	midpoint = (start+end+1)/2
	v = arr[midpoint]
	if(v > value):
		return binary_search2(arr,start,midpoint-1,value)
	else:
		return binary_search2(arr,midpoint,end,value)

def entropy(data):
	'''data is a list of lists
		every list has its last member as the class.
		Use this info to calculate entropy in a straight forward way'''
	classes={}
	_total =0
	for row in data:
		_class = row[-1];
		if(not classes.has_key(_class)):
			classes[_class]=0
		classes[_class]+=1
		_total+=1
	_entropy = 0.0
	for i in classes.keys():
		p = float(classes[i])/_total
		_entropy += -p*math.log(p,2)
	return _entropy

def dominant(store):
	_dic={}
	_max_v=0
	_max_ind=0
	for item in store:
		_v=item[-1]
		if(not _dic.has_key(_v)):
			_dic[_v]=0
		_dic[_v]+=1
		if(_dic[_v]>_max_v):
			_max_v = _dic[_v]
			_max_ind = _v
	#print "RET",_max_ind,store
	return _max_ind
	
def binary_search(store,start,end,threshold,threshold2):
	if(start+1==end or start>=end): return [(start,end,store[start][-1])]
	if(entropy(store[start:end])<=threshold or end-start+1<threshold2):
		d = dominant(store[start:end])
		return [(start,end,d)]
	midpoint = (start+end)	/2
	#index = binary_search2(store,0,len(store)-1,midpoint)
	if(midpoint == None): 	return (None,None)
	t1 = entropy(store[start:midpoint])
	t2 = entropy(store[midpoint:end])
	a1,a2=None,None
	if(t1<=threshold):
		d = dominant(store[start:midpoint])
		a1 = (start,midpoint,d)
	else:
		a1= binary_search(store,start,midpoint,threshold,threshold2)
	if(t2<=threshold):
		d = dominant(store[midpoint:end])
		a2= (midpoint,end,d)
	else:
		a2= binary_search(store,midpoint,end,threshold,threshold2)
	if(type(a1)!=type([])):
		a1=[a1]
	if(type(a2)!=type([])):
		a2=[a2]
	a = []
	for i in a1:
		a.append(i)
	for i in a2:
		a.append(i)
	return a

fd=open('train_cont','rb')
origstore=[]
bigstore =[]
cont =[1,2,7,10,13,14]
cont_category=[]
for i in fd:
	i=i.strip()
	arr = i.split(',')
	barr = []
	for i in cont:
		val = arr[i]
		if(val !='?' ):
			val=float(arr[i])
		barr.append(val)
	barr.append(arr[-1])
	bigstore.append(barr)
	origstore.append(arr)

for _i in xrange(len(bigstore[0])-1):
	store=[]
	for _j in bigstore:
		store.append((_j[_i],_j[-1]))
	store.sort()
	_min=store[0][0]
	_max=store[-1][0]
	splits= binary_search(store,0,len(store)-1,0.6,24)
	new_splits=[]
	ind = 0
	current_start = ind
	while(ind<len(splits)-1):
		if( current_start==-1):
			current_start = ind
		if(splits[ind][2] != splits[ind+1][2]):
			new_splits.append((store[splits[current_start][0]][0],store[splits[ind][1]][0],splits[ind][2]))
			current_start = -1
		ind+=1
	if(current_start):
		new_splits.append((store[splits[current_start][0]][0],store[splits[-1][1]][0],splits[-1][2]))
	else:
		new_splits.append((store[splits[-1][0]][0],store[splits[-1][1]][0],splits[-1][2]))
	cont_category.append(new_splits)
	freq ={}
	mark=[]
	for _rowi in xrange(len(bigstore)):
		row = bigstore[_rowi]
		val = row[_i]
		if(row[_i]=='?'):
			mark.append(_rowi)
			continue
		val = float(row[_i])
		for i in xrange(len(new_splits)):
			start,end,_class = new_splits[i]
			if(start<=val<=end):
				row[_i]=str(i)
				if(not freq.has_key(str(i))) :
					freq[str(i)]=0
				freq[str(i)]+=1
				t=randint(1,10)
				if(t<6):
					break
	for i in mark:
		r = randint(0,690)
		a = freq.keys()
		a.sort()
		sum =0 
		for j in a:
			sum+=freq[j]
			if(sum>=r):
				bigstore[i][_i]=j
				break
discrete =[0,3,4,5,6,8,9,11,12]
def findCompartment(value,index):
	new_splits = cont_category[index]
	val = None
	if(value<new_splits[0][0]):
		return str(0)
	if(value>new_splits[-1][1]):
		return str(len(cont_category)-1)
	for i in xrange(len(new_splits)):
		start,end,_class = new_splits[i]
		if(start<=value<=end):
			t=randint(1,10)
			val = str(i)
			if(t<6):
				break
	return val	

def fill_missing_values(data):
	for row in data:
		for i in xrange(len(row)):
			if(row[i]=='?'):
				while(True):
					r = randint(0,len(data)-1)
					if(data[r][i]!='?'):
						row[i]=data[r][i]
						break
	return data

def discretize(fname):
	fd=open(fname,'rb')
	darr=[]
	for i in fd:
		i = i.strip()
		arr = i.split(',')
		for ind in xrange(len(arr)):
			if(ind in cont and arr[ind]!='?'):
				arr[ind]=findCompartment(float(arr[ind]),cont.index(ind))
		darr.append(arr)
	darr = fill_missing_values(darr)
	for row in darr:
		row = row[:-1]
		print ','.join(row)

for i in xrange(len(origstore)):
	for ind in xrange(len(origstore[0])):
		if(ind in cont):
			origstore[i][ind]=bigstore[i][cont.index(ind)]
		else:
			val = origstore[i][ind]
			if(val=='?'):
				while(True):
					r=randint(0,len(origstore))
					newval=origstore[r][ind]
					if(newval!='?'):
						val=newval
						break
			origstore[i][ind]=val
discretize(sys.argv[1])
