import math

import plotCreator
import run
import fileManager
import tqdm
from tqdm import trange
import time
import numpy as np

kernelMode="cosinus"

def kernel(i,j):
	'''
	kernel cosinus function
	:param i:
	:param j:
	:return:
	'''
	y = 1  # factor to determine ??
	return np.dot(i,j)/(np.linalg.norm(i)*np.linalg.norm(j))

def kernelTest(i,j):
	'''
	kernel test function: allows you to test whatever you want
	:param i:
	:param j:
	:return:
	'''
	y = 1  # factor to determine ??
	return math.exp(-1 * y *np.dot(i,j)/(np.linalg.norm(i)*np.linalg.norm(j)))

def kernelEuclidean(i,j):
	'''
	kernel euclidean function
	:param i:
	:param j:
	:return:
	'''
	y = 1  # factor to determine ??
	return math.exp(-1 * y * math.dist(i, j))

def sum1MMD(z, m):
	'''
	the first sum of the MMD calculation
	:param z:
	:param m:
	:return:
	'''
	sum=0
	for i in range(0,m):
		for j in range (0,m):
			#if (i<len(z) and j<len(z)):
			if kernelMode=="cosinus":
				sum=sum+kernel(z[i],z[j])
			elif kernelMode=="test":
				sum = sum + kernelTest(z[i], z[j])
			else:
				sum = sum + kernelEuclidean(z[i], z[j])
	# if ((1/(m*m))*sum==1):
	# 	print("m*m=",m*m)
	# 	print("sum=",sum)
	return (1/(m*m))*sum

def sum2MMD(z, x, m, n,gmmNb=None):
	'''
	the second sum of the MMD calculation
	:param z:
	:param x:
	:param m:
	:param n:
	:param gmmNb:
	:return:
	'''
	sum=0
	b = 1
	a = 1
	sizeTot = m * n
	if gmmNb != None:
		sizeTot = 0
		for i in gmmNb:
			sizeTot += i
		sizeTot*=m
	for i in range(0,m):
		for j in range (0,n):
			if gmmNb != None:
				b=gmmNb[j]
			if kernelMode=="cosinus":
				sum=sum+kernel(z[i],x[j])*b
			elif kernelMode == "test":
				sum = sum + kernelTest(z[i], x[j])*b
			else:
				sum = sum + kernelEuclidean(z[i], x[j])*b
	return (2/(sizeTot))*sum

def sum3MMD(x, n,gmmNb=None):
	'''
	the third sum of the MMD calculation
	:param x:
	:param n:
	:param gmmNb:
	:return:
	'''
	sum=0
	b=1
	a=1
	sizeTot=n*n
	if gmmNb!=None:
		sizeTot=0
		for i in gmmNb:
			sizeTot+=i
	for i in range(0,n):
		if gmmNb != None:
			a = gmmNb[i]
		for j in range (0,n):
			if gmmNb != None:
				b=gmmNb[j]
			if kernelMode=="cosinus":
				sum=sum+kernel(x[i],x[j])*a*b
			elif kernelMode=="test":
				sum = sum + kernelTest(x[i], x[j])*a*b
			else:
				sum = sum + kernelEuclidean(x[i], x[j])*a*b
	return (1/(sizeTot))*sum

def sum1Witness(point,x,n):
	'''
	the first sum of the witness function
	:param point:
	:param x:
	:param n:
	:return:
	'''
	sum = 0
	for i in range(n):
		if kernelMode == "cosinus":
			sum += kernel(point, x[i])
		elif kernelMode == "test":
			sum += kernelTest(point, x[i])
		else:
			sum += kernelEuclidean(point, x[i])
	return (1/n)*sum

def sum2Witness(point,z,m):
	'''
	the second sum of the witness function
	:param point:
	:param z:
	:param m:
	:return:
	'''
	sum = 0
	for i in range(m):
		if kernelMode == "cosinus":
			sum += kernel(point, z[i])
		elif kernelMode == "test":
			sum += kernelTest(point, z[i])
		else:
			sum += kernelEuclidean(point, z[i])
	return (1/m)*sum

def changePrototypesFormat(proto):
	'''
	:param proto: a list of prototypes (utt id, dim1, dim2...)
	:return: a list of utterances and of prototypes ordered by speakers and converted to vectors format (dim1, dim2...)
	'''
	classifiedProto=[]
	classifiedUtt=[]
	speakerList=[]
	for i in proto:
		if run.uttToSpk(i[0]) in speakerList:
			#print(run.uttToSpk(i[0]))
			j=speakerList.index(run.uttToSpk(i[0]))
			classifiedProto[j].append(i[1:])
			classifiedUtt[j].append(i[0])
		else:
			classifiedProto.append([])
			classifiedProto[-1].append(i[1:])
			speakerList.append(run.uttToSpk(i[0]))
			classifiedUtt.append([])
			classifiedUtt[-1].append(i[0])
	return classifiedUtt,classifiedProto

def grouped(classifiedUtt,classifiedVectors,nbPrototypes=2,grid=True,kernelM="euclidienne",groupSize=10,gmm=None,reducted=False):
	'''
	subdivide the vectors in multiples groups to compute faster
	:param classifiedUtt: an list ordered by speaker of utterances
	:param classifiedVectors: an list ordered by speaker of vectors
	:param nbPrototypes: number of prototypes for each speaker
	:param grid: activate grid search
	:param kernelM: select the kernel function to use
	:param groupSize: number of speakers in each group
	:param gmm: is gmm have been used
	:param reducted:
	:return: a list of prototypes and criticisms
	'''
	sizeTot=len(classifiedVectors)
	groupNb=sizeTot/groupSize
	groupNb=math.ceil(groupNb)
	lProto=[]
	lCrit=[]
	ct=0
	for i in range(groupNb):
		subUtt=[]
		subVectors=[]
		for j in range(groupSize):
			if (ct)<len(classifiedVectors):
				subVectors.append(classifiedVectors[ct])
				subUtt.append(classifiedUtt[ct])
				ct+=1
		subProto,subCrit,g,g2=prototypesEachSpeaker(subUtt,subVectors,nbPrototypes,grid,kernelM,gmm)

		for i in subProto:
			lProto.append(i)
		for i in subCrit:
			lCrit.append(i)
	if reducted:
		utt,vectors=changePrototypesFormat(lProto)
		lProto,tmp,g,g2=prototypes(utt,vectors,10,grid,kernelM)
	return lProto,lCrit,g,g2

def prototypesEachSpeaker(newutt,newvectors,nbPrototypes=2,grid=True,kernelM="euclidienne",gmm=None):
	'''
	:param newutt: an list ordered by speaker of utterances
	:param newvectors: an list ordered by speaker of vectors
	:param nbPrototypes: number of prototypes for each speaker
	:param grid: activate grid search
	:param kernelM:	select the kernel function to use
	:param gmm:	is gmm have been used
	:return: list of prototypes and criticisms
	'''
	global kernelMode
	kernelMode=kernelM
	print("Prototypes and criticisms...")
	time.sleep(0.2)
	nbPrototypesTot=len(newutt)
	z=[]
	proto=[]
	criti=[]
	grp=[]
	grc=[]
	#ct=0
	uttP=[]
	uttC=[]
	for ct in trange(nbPrototypesTot):
		print("SPK=",ct)
		print(run.uttToSpk(newutt[ct][0]))
		sum3 = sum3MMD(newvectors[ct], len(newvectors[ct]))
		for j in range(nbPrototypes):	# select the prototypes
			print("J=",j)
			#print("---------------------")
			MMD=[]
			for i in range(len(newvectors[ct])):	# for each point
				mmd2=-1
				if newvectors[ct][i] not in z:
					z.append(newvectors[ct][i])		# add the point to the list of prototypes
					# calculate the mmd
					if gmm!=None:
						mmd2 = sum1MMD(z, len(z)) - sum2MMD(z, newvectors[ct], len(z), len(newvectors[ct]),gmm[ct]) + sum3
					else:
						mmd2 = sum1MMD(z, len(z)) - sum2MMD(z, newvectors[ct], len(z), len(newvectors[ct])) + sum3
						# print(mmd2,"=", sum1MMD(z, len(z)),"-",sum2MMD(z, newvectors[ct], len(z), len(newvectors[ct])),"+",sum3)
					z.pop()		# remove the point from the list of prototypes
				MMD.append(mmd2)	# add the score to the list
			min = -1
			for i in range (0,len(MMD)):	# search the min from the score list
				if ((min==-1 or MMD[min]>MMD[i])  and  (newvectors[ct][i] not in proto)) and MMD[i]!=-1:
					min = i
			if (min!=-1):	# add the prototype to the list
				print("MIN: ",MMD[min])
				proto.append(newvectors[ct][min])
				uttP.append(newutt[ct][min])
				grp.append([ct,min])
				# for i in newvectors[ct][min]:
				# 	proto[-1].append(i)
				z.append(newvectors[ct][min])
			MMD.clear()
		print("z=",z)
		for j in range(nbPrototypes):	# select the criticisms
			witness = []
			#print("len=",len(z))
			for i in range(len(newvectors[ct])):	# calculate the witness value for each point
				# witness function
				#if newutt[ct][i]=="id10038-7Gd4Fz2UNxQ-00009":
				# print("start")
				# print("len=",len(z))
				# print("z=",z)
				wX=0
				if newvectors[ct][i] not in z:
					wX = sum1Witness(newvectors[ct][i], newvectors[ct], len(newvectors[ct])) - sum2Witness(newvectors[ct][i], z, len(z))
					print(newutt[ct][i],":",abs(wX),"=",wX,"=", sum1Witness(newvectors[ct][i], newvectors[ct], len(newvectors[ct])),"-",sum2Witness(newvectors[ct][i], z, len(z)))
					#wX=abs(wX)
				witness.append(wX)
			max = -1
			for i in range(len(witness)):	# for each witness value
				if ((max == -1 or witness[max] < witness[i]) and (newvectors[ct][i] not in criti)):		# if witness value > max
					max = i
			if (max != -1):		# add the max to the crit list
				# print("Tot:",len(newvectors[ct]))
				print("MAX: ",newutt[ct][max], witness[max])
				# print("z=", z)
				criti.append(newvectors[ct][max])
				uttC.append(newutt[ct][max])
				grc.append([ct, max])
				# if wX=abs(Wx) is in comment:
				z.append(newvectors[ct][max])
				#
			witness.clear()
		z.clear()
			# print("------")



	# for i in newvectors[ct][max]:
	# 	criti[-1].append(i)
	lproto=[]
	lcrit=[]

	for i in range(len(uttP)):	# make the prototypes and criticisms list
		lproto.append([])
		lproto[-1].append(uttP[i])
		for j in proto[i]:
			lproto[-1].append(j)
		lcrit.append([])
		lcrit[-1].append(uttC[i])
		for j in criti[i]:
			lcrit[-1].append(j)
	g = -1
	g2 = -1
	if grid:
		g, g2 = gridSearch(newvectors, grp, grc)
	return lproto,lcrit,g,g2

def gridSearch(newutt,proto,crit):
	'''
	calculate the distance between each proto and their classes and between each classes
	:param newutt:
	:param proto:
	:param crit:
	:return:
	'''
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

def prototypes(newutt,newvectors,nbPrototypes=2,grid=True,kernelM="euclidienne"):
	'''
	calculate prototypes for a given class
	:param newutt:
	:param newvectors:
	:param nbPrototypes:
	:param grid:
	:param kernelM:
	:return:
	'''
	global kernelMode
	kernelMode=kernelM
	print("Prototypes and criticisms...")
	time.sleep(0.2)
	nbPrototypes=nbPrototypes
	z=[]
	proto=[]
	criti=[]
	vectors=[]
	for i in newvectors:
		for j in i:
			vectors.append(j)
	sum3 = sum3MMD(vectors, len(vectors))
	for ct in trange(nbPrototypes) :
		#print("---------------------")
		MMD=[]
		for i in range(len(newvectors)):
			MMD.append([])
			for j in range(len(newvectors[i])):
				z.append(newvectors[i][j])
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
	return proto,criti,g,g2


if __name__ == "__main__":
	'''
	test only
	'''
	print("main")






