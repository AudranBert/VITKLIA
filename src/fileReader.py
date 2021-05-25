import random
import os
from pathlib import Path


def generateRandomData():
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
	file1 = open(file, 'r')
	lines = file1.readlines()
	data=[]
	for i in lines:
		s=i.strip("\n")
		s=s.split()
		print(s)
		if len(s)==3:
			data.append((float(s[0]),float(s[1]),float(s[2])))
		elif len(s)==2:
			data.append((float(s[0]),float(s[1])))
	file1.close()
	return data

def reading(file):
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
	file1 = open(file, 'w')
	for i in data:
		for j in i:
			s = str(j) + " "
			file1.write(s)
		file1.write("\n")
	file1.close()


if __name__ == "__main__":
	print("Reading")







