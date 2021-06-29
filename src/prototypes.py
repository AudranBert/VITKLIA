import math

import plotCreator
import fileManager
import tqdm
from tqdm import trange
import time
import numpy as np

kernelMode="cosinus"

def kernel(i,j):
	y = 1  # factor to determine ??
	return np.dot(i,j)/(np.linalg.norm(i)*np.linalg.norm(j))

def kernelTest(i,j):
	y = 1  # factor to determine ??
	return math.exp(-1 * y *np.dot(i,j)/(np.linalg.norm(i)*np.linalg.norm(j)))

def kernelEuclidienne(i,j):
	y = 1  # factor to determine ??
	return math.exp(-1 * y * math.dist(i, j))

def sum1MMD(z, m):
	sum=0
	for i in range(0,m):
		for j in range (0,m):
			#if (i<len(z) and j<len(z)):
			if kernelMode=="cosinus":
				sum=sum+kernel(z[i],z[j])
			elif kernelMode=="test":
				sum = sum + kernelTest(z[i], z[j])
			else:
				sum = sum + kernelEuclidienne(z[i], z[j])
	return (1/(m*m))*sum

def sum2MMD(z, x, m, n):
	sum=0
	for i in range(0,m):
		for j in range (0,n):
			#if (i < len(z)):
			if kernelMode=="cosinus":
				sum=sum+kernel(z[i],x[j])
			elif kernelMode == "test":
				sum = sum + kernelTest(z[i], x[j])
			else:
				sum = sum + kernelEuclidienne(z[i], x[j])
	return (2/(m*n))*sum

def sum3MMD(x, n):
	sum=0
	for i in range(0,n):
		for j in range (0,n):
			if kernelMode=="cosinus":
				sum=sum+kernel(x[i],x[j])
			elif kernelMode=="test":
				sum = sum + kernelTest(x[i], x[j])
			else:
				sum = sum + kernelEuclidienne(x[i], x[j])
	return (1/(n*n))*sum

def classify(utt,vectors):
	loc = []
	nutt=[]
	newutt = []
	ctutt = 0
	for i in utt:
		idL = i.split("-", 1)
		id = idL[0]
		ct = 0
		find = False
		for j in loc:
			if j == id:
				nutt[ct].append(i)
				newutt[ct].append(vectors[ctutt])
				find = True
				break
			ct += 1
		if find == False:
			loc.append(id)
			newutt.append([])
			nutt.append([])
			nutt[-1].append(i)
			newutt[len(newutt) - 1].append(vectors[ctutt])
		ctutt += 1
	#for i in newutt:
	#	print(i)
	return  newutt,nutt

def prototypes(utt,vectors,nbPrototypes=2,grid=True,kernelM="euclidienne"):
	global kernelMode
	kernelMode=kernelM
	print("Prototypes and criticisms...")
	time.sleep(0.2)
	nbPrototypes=nbPrototypes
	z=[]
	proto=[]
	criti=[]

	sum3 = sum3MMD(vectors, len(vectors))
	newvectors,newutt=classify(utt,vectors)
	for ct in trange(nbPrototypes) :
		#print("---------------------")
		MMD=[]
		for i in range(len(newvectors)):
			MMD.append([])
			for j in range(len(newvectors[i])):
				z.append(newvectors[i][j])
				#print(z)
				mmd2 = sum1MMD(z, len(z)) - sum2MMD(z, vectors, len(z), len(vectors)) + sum3
				z.pop()
				MMD[-1].append(mmd2)
		min = [-1,-1]
		max=[-1,-1]
		for i in range (len(MMD)):
			for j in range (len(MMD[i])):
				if ((min[0]==-1 or MMD[min[0]][min[1]]>MMD[i][j])  and  ([i,j] not in proto)):
					min = [i,j]
				if ((max[0]==-1 or MMD[max[0]][max[1]]<MMD[i][j]) and  ([i,j] not in criti)):
					max = [i,j]
		if (min[0]!=-1):
			proto.append([])
			proto[-1].append(newutt[min[0]][min[1]])
			for i in newvectors[min[0]][min[1]]:
				proto[-1].append(i)
			z.append(newvectors[min[0]][min[1]])
		if(max[0]!=-1):
			criti.append([])
			criti[-1].append(newutt[max[0]][max[1]])
			for i in newvectors[max[0]][max[1]]:
				criti[-1].append(i)
	g=-1
	g2=-1
	if grid:
		g,g2=gridSearch(newvectors,proto,criti)
	return newvectors,newutt,proto,criti,g,g2

def prototypesEachSpeaker(utt,vectors,grid,kernelM):
	global kernelMode
	kernelMode=kernelM
	print("Prototypes and criticisms...")
	time.sleep(0.2)
	newvectors,newutt=classify(utt,vectors)
	nbPrototypes=len(newutt)
	z=[]
	proto=[]
	criti=[]
	#ct=0

	for ct in trange(nbPrototypes) :
		#print("---------------------")
		MMD=[]
		sum3=sum3MMD(newvectors[ct], len(newvectors[ct]))
		for i in range(len(newvectors[ct])):
			z.append(newvectors[ct][i])
			#print(z)
			mmd2 = sum1MMD(z, len(z)) - sum2MMD(z, newvectors[ct], len(z), len(newvectors[ct])) + sum3
			z.pop()
			MMD.append(mmd2)
		min = -1
		max=-1
		for i in range (0,len(MMD)):
			if ((min==-1 or MMD[min]>MMD[i])  and  (newvectors[ct][i] not in proto)):
				min = i
			if ((max==-1 or MMD[max]<MMD[i]) and  (newvectors[ct][i] not in criti)):
				max = i
		if (min!=-1):
			proto.append([])
			proto[-1].append(newutt[ct][min])
			for i in newvectors[ct][min]:
				proto[-1].append(i)
			z.append(newvectors[ct][min])
		if(max!=-1):
			criti.append([])
			criti[-1].append(newutt[ct][max])
			for i in newvectors[ct][max]:
				criti[-1].append(i)
	g=-1
	g2=-1
	if grid:
		g,g2=gridSearch(newvectors,proto,criti)
	return newvectors,newutt,proto,criti,g,g2

def gridSearch(newutt,proto,crit):
	sum=0
	for i in range(len(proto)):
		sum+=math.dist(newutt[proto[i][0]][proto[i][1]],newutt[crit[i][0]][crit[i][1]])
	print("Grid search:")
	intra=0
	if len(proto)!=0:
		intra=sum/len(proto)
		print("intra class:",sum/len(proto))
	sum=0
	for i in range(len(proto)):
		for j in range(len(proto)):
			sum+=math.dist(newutt[proto[i][0]][proto[i][1]],newutt[proto[j][0]][proto[j][1]])
	inter=0
	if len(proto)!=0:
		inter=sum/(len(proto)*len(proto))
		print("inter class:",sum/(len(proto)*len(proto)))
	return intra,inter
if __name__ == "__main__":
	'''
	test only
	'''
	print("main")






