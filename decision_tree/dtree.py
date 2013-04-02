from random import randint
import sys
import math
fname = '/home/arun/Documents/ai_project/crx.data'
#fd = open(fname,'rb')
data=[]
attribute_count=0
root = None


class Node:
	def __init__(self):
		self.attribute = -1 #have a global index of attributes
		self.child= {} #pointers to child Nodes based on the value of the attribute taken
		self.label = ''

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
			
def classify(data,index):
	'''given index for each value in index return a dict that has key as index_value and value as subset of data with index at index_value'''
	s={}
	for row in data:
		v = row[index]
		if(not s.has_key(v)):
			s[v]=[]
		s[v].append(row)
	return s

def information_gain(data,index):
	'''given data as list of lists and the index of the attribute set to consider determine the information gain using index as the splitter'''
	_e = entropy(data)
	ig_diff = 0.0
	_size = len(data)
	s = classify(data,index)
	for v in s.keys():
		e = entropy(s[v])
		ig_diff +=  float(len(s[v]))/_size * e
	return _e - ig_diff

def readFromFile(fname):
	global attribute_count
	global data
	fd = open(fname,'rb')
	for i in fd:
		i=i.strip()
		arr = i.split(',')
		attribute_count = len(arr)
		#cont =[1,2,7,10,13,14]
		cont=[]
		new_arr=[]
		"""for i in cont:
			if(arr[i]!='?'):
				arr[i]=float(arr[i])
		"""
		for ind in xrange(len(arr)):
			if(ind not in cont):
				new_arr.append(arr[ind])
		data.append(new_arr)
	fd.close()

def dfs(node,parent=None):
	m = node.child
	print "EXPLORING NODE ",node.attribute, node.label
	print "TEST",m.keys()
	for i in m.keys():
		print "Going for ",node.attribute,"= ",i,
		if(parent):
			print "PARENT",parent.label,parent.attribute
		else:
			print " Root"
		dfs(m[i],node)
		
def process(row,node):
	if(node.label!=''):
		return node.label
	v = row[node.attribute]
	if(not  node.child.has_key(v)):
		#this is a data noise
		_arr = node.child.keys()
		_v = randint(0,len(_arr)-1)
		v = _arr[_v]
	return process(row,node.child[v])

def contToDiscrete(data):
	dic = {}
	threshold = 0.8
	divs = 2
	_min=-100
	_max=2**100
	contp,contn=0
	for (name,value) in data:
		f = float(name)
		if(f<_min): _min=f
		if(_max<_f): _max = f
		if(value=='y'):
			if(contp>0): contp+=1
			else: contp=1
		if(value=='n'):
			if(contn>0): contn+=1
			else: contn=1
	
def shallowcopy(arr):
	barr=[]
	for i in arr:
		barr.append(i)
	return barr
	
def train(data,node,blist):
	'''classify the data at node '''
	attlist = shallowcopy(blist)
	if(len(attlist)==1):
		counter={}
		_max_key=-1
		_max=-1
		for i in data:
			key = i[-1]
			if(not counter.has_key(key)):
				counter[key]=0
			counter[key]+=1
			if(_max<counter[key]):
				_max = counter[key]
				_max_key= key
		node.attribute = attlist[0]
		node.label=_max_key
		return node
	max_ig = -2000
	max_ind = -1
	for i in attlist:
		ig = information_gain(data,i)
		if(ig>max_ig):
			max_ig = ig
			max_ind = i
	s = classify(data,max_ind)
	node.attribute = max_ind
	attlist.remove(max_ind)
	if(max_ind<0):
		print "Exception situation: max_ind",max_ind
	for i in s.keys():
		c = Node()
		e = entropy(s[i])
		if(e==0):
			c.label =s[i][0][-1]
		else:
			c = train(s[i],c,attlist)
		node.child[i]=c
	return node

if(__name__=="__main__"):
	readFromFile('train_discrete')
	root = Node()
	root = train(data,root,range(0,attribute_count-1))
	fd = open(sys.argv[1],'rb')
	for i in fd:
		i=i.strip()
		row = i.split(',')
		print "%s,%s" %(i,process(row,root))
