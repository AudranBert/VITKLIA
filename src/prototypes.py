import math

import plotCreator
import fileReader
import tqdm
from tqdm import trange


def kernel(i,j):
	y = 1  # factor to determine ??
	return math.exp(-1 * y * math.dist(i, j))



def sum1MMD(z, m):
	sum=0
	for i in range(0,m):
		for j in range (0,m):
			#if (i<len(z) and j<len(z)):
			sum=sum+kernel(z[i],z[j])
	return (1/(m*m))*sum

def sum2MMD(z, x, m, n):
	sum=0
	for i in range(0,m):
		for j in range (0,n):
			#if (i < len(z)):
			sum=sum+kernel(z[i],x[j])
	return (2/(m*n))*sum

def sum3MMD(x, n):
	sum=0
	for i in range(0,n):
		for j in range (0,n):
			sum=sum+kernel(x[i],x[j])
	return (1/(n*n))*sum

def classify(vectors,utt):
	loc = []
	newutt = []
	ctutt = 0
	for i in utt:
		idL = i.split("-", 1)
		id = idL[0]
		ct = 0
		find = False
		for j in loc:
			if j == id:
				newutt[ct].append(vectors[ctutt])
				find = True
				break
			ct += 1
		if find == False:
			loc.append(id)
			newutt.append([])
			newutt[len(newutt) - 1].append(vectors[ctutt])
		ctutt += 1
	for i in newutt:
		print(i)
	return  newutt

def prototypes(vectors,utt,nbPrototypes=2):

	z=[]
	proto=[]
	criti=[]
	while len(proto)!=nbPrototypes:
		#print("---------------------")
		MMD=[]
		for i in range (0,len(vectors)):
			z.append(vectors[i])
			#print(z)
			mmd2 = sum1MMD(z, len(z)) - sum2MMD(z, vectors, len(z), len(vectors)) + sum3MMD(vectors, len(vectors))
			#print(sum1MMD(z, nbPrototypes))
			z.pop()
			MMD.append(mmd2)
		min = -1
		max=-1
		for i in range (0,len(MMD)):
			if (min==-1  and  (vectors[i] not in proto)):
				min = i
			elif (MMD[min]>MMD[i]  and (vectors[i] not in proto)):
				min=i
			if (max==-1  and  (vectors[i] not in criti)):
				max = i
			elif (MMD[max]<MMD[i]  and (vectors[i] not in criti)):
				max=i
		if (min!=-1):
			proto.append(vectors[min])
			z.append(vectors[min])
		if(max!=-1):
			criti.append(vectors[max])
		#print(MMD)
		#print("min :", min, " : ",MMD[min])
		#print("max :",max, " : ", MMD[max])
		#print(z)
	return proto,criti

def prototypesEachSpeaker(vectors,utt,grid):
	newutt=classify(vectors,utt)
	nbPrototypes=len(newutt)
	z=[]
	proto=[]
	criti=[]
	#ct=0
	print("Prototypes and criticisms...")
	for ct in trange(nbPrototypes) :
		#print("---------------------")
		MMD=[]
		for i in range(len(newutt[ct])):
			z.append(newutt[ct][i])
			#print(z)
			mmd2 = sum1MMD(z, len(z)) - sum2MMD(z, newutt[ct], len(z), len(newutt[ct])) + sum3MMD(newutt[ct], len(newutt[ct]))
			#print(sum1MMD(z, nbPrototypes))
			# if(i>60):
			# 	print("--------------")
			# 	print(sum1MMD(z, len(z)))
			# 	print(sum2MMD(z, newutt[ct], len(z), len(newutt[ct])))
			# 	print(sum3MMD(newutt[ct], len(newutt[ct])))
			# 	print("--------------")
			z.pop()
			MMD.append(mmd2)
		min = -1
		max=-1
		for i in range (0,len(MMD)):
			if (min==-1  and  (newutt[ct][i] not in proto)):
				min = i
			elif (MMD[min]>MMD[i]  and (newutt[ct][i] not in proto)):
				min=i
			if (max==-1  and  (newutt[ct][i] not in criti)):
				max = i
			elif (MMD[max]<MMD[i]  and (newutt[ct][i] not in criti)):
				max=i
		if (min!=-1):
			proto.append(newutt[ct][min])
			z.append(newutt[ct][min])
		if(max!=-1):
			criti.append(newutt[ct][max])
		#print(MMD)
		#print("min :", min, " : ",MMD[min])
		#print("max :",max, " : ", MMD[max])
		#print(z)
		#ct=ct+1
	if grid:
		gridSearch(proto,criti)
	return proto,criti

def gridSearch(proto,crit):
	sum=0
	for i in range(len(proto)):
		sum+=math.dist(proto[i],crit[i])
	print("Grid search:")
	print(sum)

if __name__ == "__main__":
	'''
	test only
	'''
	print("main")






