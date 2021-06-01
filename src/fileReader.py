import random
import os
from pathlib import Path


def generateRandomData():
	'''
	test only
	'''
	n=10
	dim3D = False
	points = []
	if dim3D:
		### generate random points
		for i in range(0, n):
			points.append((random.uniform(0, i + 2), random.uniform(0, i + 2), random.uniform(0, i + 2)))
	###
	### fixed list
	# x = [1, 2, 3, 4, 5]
	# y = [1, 2, 3, 4, 5]
	# y2 = [1, 4, 9, 16, 25]
	###
	else:
		### generate random points
		for i in range(0, n):
			points.append((random.uniform(0, i + 2), random.uniform(0, i + 2)))
	###
	### fixed list
	# x = [1, 2, 3, 4, 5]
	# y = [1, 2, 3, 4, 5]
	# y2 = [1, 4, 9, 16, 25]
	###
	return points

def readAFile(file):
	'''
	:param file:
	:return speakers,data:
	'''
	file1 = open(file, 'r') 	# open the file
	lines = file1.readlines()
	speakers=[]
	data=[]
	for i in lines:
		s=i.strip("\n")
		s=s.split()
		#print(s)
		if len(s)==4:		# 3D vectors
			speakers.append(s[0])	# uttId
			data.append((float(s[1]),float(s[2]),float(s[3])))	# vectors
		elif len(s)==3:		# 2D vectors
			speakers.append(s[0])
			data.append((float(s[1]),float(s[2])))
	file1.close()
	return speakers,data

def reading(file):
	'''
	test only
	'''
	my_file =Path(file)
	erase=False
	data=[]
	if my_file.exists() and erase==False:
		print("ALREADY")
		data = readAFile(file)
	else:
		data=generateRandomData()
		exportData(data, file)
	return data


def exportData(data, file):
	'''
	depreciated
	save vectors
	:param data:
	:param file:
	:return:
	'''
	file1 = open(file, 'w')
	for i in data:
		for j in i:
			s = str(j) + " "
			file1.write(s)
		file1.write("\n")
	file1.close()

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







