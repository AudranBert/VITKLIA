import random


def generateRandomData():
	n=10
	dim3D = False
	points = []
	if dim3D:
		### generate random points
		for i in range(0, n):
			points.append((random.randint(0, i + 2), random.randint(0, i + 2), random.randint(0, i + 2)))
	###
	### fixed list
	# x = [1, 2, 3, 4, 5]
	# y = [1, 2, 3, 4, 5]
	# y2 = [1, 4, 9, 16, 25]
	###
	else:
		### generate random points
		for i in range(0, n):
			points.append((random.randint(0, i + 2), random.randint(0, i + 2)))
	###
	### fixed list
	# x = [1, 2, 3, 4, 5]
	# y = [1, 2, 3, 4, 5]
	# y2 = [1, 4, 9, 16, 25]
	###
	return points

def reading(file):
	data=generateRandomData()
	return data

if __name__ == "__main__":
	print("Reading")







