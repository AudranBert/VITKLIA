import random
import os
import prototypes
from pathlib import Path





def readUtt(vectorFile):
	'''
	read vectors with their utterances ids
	:param vectorFile:
	:return:
	'''
	utt = []
	vectors = []
	file = open(vectorFile, "r")
	for line in file:
		line=line.strip("\n")
		line = line.strip("\t")
		line=line.strip()
		l=line.split(" ")
		utt.append(l[0])
		l.pop(0)
		vectors.append([])
		for i in l:
			vectors[-1].append(float(i))
	file.close()
	return utt,vectors

def readFiles(vectorFile,protoFile,critFile):
	'''
	read vectors, utterances, prototypes and criticisms in files
	:param vectorFile:
	:param protoFile:
	:param critFile:
	:return:
	'''
	proto=[]
	crit=[]
	utt = []
	vectors = []
	utt,vectors=readUtt(vectorFile)
	#print(vectors)
	file = open(protoFile, "r")
	for line in file:
		line=line.strip("\n")
		line = line.strip("\t")
		line=line.strip()
		l=line.split(" ")
		proto.append([])
		proto[-1].append(l[0])
		for i in l[1:]:
			proto[-1].append(float(i))
	file.close()
	file = open(critFile, "r")
	for line in file:
		line=line.strip("\n")
		line = line.strip("\t")
		line=line.strip()
		l=line.split(" ")
		crit.append([])
		crit[-1].append(l[0])
		for i in l[1:]:
			crit[-1].append(float(i))
	file.close()

	return utt,vectors,proto,crit

def exportFiles(utt,vectors,proto,crit,vectorFile,protoFile,critFile):
	'''
	export vectors, utterances, prototypes and criticisms in files
	:param utt:
	:param vectors:
	:param proto:
	:param crit:
	:param vectorFile:
	:param protoFile:
	:param critFile:
	:return:
	'''
	exportUtt(utt,vectors,vectorFile)
	fileProto = open(protoFile, "w")
	fileCrit = open(critFile, "w")
	for i in proto:
		u = i[0]
		line = u + " "
		for j in i[1:]:
			line+=str(j)+ " "
		line +=" \n"
		fileProto.write(line)
	fileProto.close()
	for i in crit:
		u = i[0]
		line = u + " "
		for j in i[1:]:
			line+=str(j)+ " "
		line +=" \n"
		fileCrit.write(line)
	fileCrit.close()
	print("export")

def exportUtt(utt,vectors,vectorFile):
	file=open(vectorFile,"w")
	for i in range (len(vectors)):
		for j in range(len(vectors[i])):
			u=utt[i][j]
			line = u + " "
			for z in vectors[i][j]:
				line+=str(z)+" "
			line+=" \n"
			file.write(line)
	file.close()


def exportData(utt,data, file):
	'''
	save utt and vectors
	:param utt:
	:param data:
	:param file:
	:return:
	'''
	file1 = open(file, 'w')
	ct=0
	for i in data:
		file1.write(utt[ct]+" ") 	# write uttId
		for j in i:					# write vectors
			s = str(j) + " "
			file1.write(s)
		file1.write("\n")
		ct+=1
	file1.close()

if __name__ == "__main__":
	print("Reading")







