_length=0
_width=0

def joiner(operation,arr):
	ret=""
	if(len(arr)==0):
		return ''
	if(len(arr)==1):
		return '(%s)' %(arr[0])
	ret='(%s %s %s)' %(arr[0],operation,arr[1])
	index=2
	for i in arr[index:]:
		ret='(%s %s %s)'	%(ret,operation,i)
	return ret
class board:
	def __init__(self,board):
		self.board=board
		self.X=[]

	def adjacent(self,x,y):
		xval=x-1
		adjlist=[]
		while(xval<x+2):
			yval=y-1
			while(yval<y+2):
				if(not (x==xval and y==yval) and (xval>=0 and yval>=0) and (xval<_length and yval<_width)):
					adjlist.append(self.board[xval][yval])
				yval+=1
			xval+=1
		return adjlist

	def formPremise(self,x,y):
		node=self.board[x][y]
		if(node.value=='NH'):
			return ('NOT '+str(node))
		if(node.value!='X'):
			num=int(node.value)
			arr=self.adjacent(node.x,node.y)
			narr=[]
			barr=[]
			if(num>4):
				for i in arr:
					barr.append('~'+str(i))
				narr=select(barr,8-num)	
			else:
				narr=select(arr,num)			
			kb=[]
			for comb in narr:
				premise=[]
				for i in comb:
					premise.append(str(i))
						newpremise=[]
				for i in premise:
					if(i.startswith('~')):
						newpremise.append(' NOT '+i[1:])
					else:
						newpremise.append(i)
				#kb.append(' AND '.join(newpremise))
				for i in newpremise:
					arr=i.split()
					val=arr[0]
					if(len(arr)==2):
						val=arr[1]
					if val not in self.X:
						newpremise.remove(i)
				if(newpremise):
					kb.append(joiner('AND',newpremise))
			#print "KB ",str(node),kb
			#return '('+(' OR '.join(kb))+') AND NOT ('+str(node)+")"
			#return ' OR '.join(kb)
			return joiner('OR',kb)
		"""Given n times in the list, take self.value items"""	
		return ''


def shallow_copy(arr):
	narr=[]
	for i in arr:
		narr.append(i)
	return narr

def all_perm(arr):
	garr=[]
	if(len(arr)<=1): return [arr]
	for i in arr:
		narr=shallow_copy(arr)
		narr.remove(i)
		for p in all_perm(narr):
			nperm=[i]
			nperm.extend(p)
			garr.append(nperm)
	return garr
		
def all_perm2(arr,c):
	garr=[]
	if(len(arr)<=1 or c<=1): return [arr]
	for i in arr:
		narr=shallow_copy(arr)
		narr.remove(i)
		for p in all_perm2(narr,c-1):
			nperm=[i]
			nperm.extend(p)
			garr.append(nperm)
	return garr

def select(arr,count):
	"""Returns all subarrays of array with size count"""
	if(count<1):
		return [[]]
	if(len(arr)<count or len(arr)==0):
		return [[]]
	if(len(arr)==count):
		return [arr]
	garr=[]
	for i in select(arr[1:],count):
		if(i!=[] and i not in garr):
			garr.append(i)
	for i in select(arr[1:],count-1):
		narr=[arr[0]]
		narr.extend(i)
		if(narr not in garr):
			garr.append(narr)
	return garr

class node:
	def __init__(self,x,y,value):
		self.x=x
		self.y=y
		self.value=value
	
	def __str__(self):
		return "P"+str(self.x)+str(self.y)

def getInput(fname):
	global _length,_width
	fd=open(fname,'rb')
	brd=[]
	a=fd.readline()
	a=a.strip()
	arr=a.split(',')
	_length,_width=int(arr[0]),int(arr[1])
	xpos=0
	for i in fd:
		b=[]
		i=i.strip()
		arr=i.split(',')
		ypos=0
		for item in arr:
			value=item
			try:
				value=int(item)
			except ValueError:
				pass
			b.append(node(xpos,ypos,value))
			ypos+=1
		xpos+=1	
		brd.append(b)
	return brd

b=board(getInput('input.txt'))
for i in b.board:
	for j in i:
		if(j.value=='X'):
			b.X.append(str(j))
kb=[]
for i in xrange(_length):
	for j in xrange(_width):
		foo= b.formPremise(i,j)
		if(foo):
			kb.append('NOT %s' %str(b.board[i][j]))
		if(type(foo)==type([])):
			kb.append(' OR '.join(foo))
		else:
			kb.append(foo)

for i in  kb:
	if i:
		print i
