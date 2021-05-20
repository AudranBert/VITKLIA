import re

import matplotlib.pyplot as plt
import numpy as np
from playsound import playsound
import math
import random

n=10		#number of point
xy = []
dim3D=False
s=[]		#sound list
#s=["../ressources/1.wav","","","",""]
for i in range (0,n):
	s.append("../ressources/1.wav")


def playSound(i):
	if (i >= 0):  # if a point have been found
		print("The point is :", xy[i])
		if (i <= len(s)):  # if a sound exist
			print("play")
			# playsound(s[point])

def find3DCoords(event, ax):
	pressed = ax.button_pressed
	ax.button_pressed = -1  # some value that doesn't make sense.
	coords = ax.format_coord(event.xdata, event.ydata)  # coordinates string in the form x=value, y=value, z= value
	ax.button_pressed = pressed
	temp = re.findall(r"[-+]?\d*\.\d+|\d+", coords)
	res=list(map(float,temp))
	print(res)
	return res

def onclick2D(event,ax):		#click on the plot
	if event.inaxes!=None:	#inside the plot
		print(event.xdata," ",event.ydata)
		point=-1
		for i in range (0,n):	#search the nearest point
			minX=event.xdata-0.5
			maxX=event.xdata+0.5
			minY=event.ydata-0.5
			maxY=event.ydata+0.5
			if (xy[i][0]>=minX and xy[i][0]<=maxX and xy[i][1]>=minY and xy[i][1]<=maxY):	#near enough
				if(point!=-1):		#if a point have been already found
					#print(i," vs ",point)
					distanceEvent=math.sqrt(pow(xy[i][0]-event.xdata,2)+pow(xy[i][1]-event.ydata,2))	#distance between the event and the point we are looking at
					distancePoint=math.sqrt(pow(xy[point][0]-event.xdata,2)+pow(xy[point][1]-event.ydata,2))	#distance between the event and the closest pont we have found
					#print(distanceEvent," vs ",distancePoint)
					if(distancePoint>distanceEvent): 		#find the nearest
						point=i
				else:
					point=i
		playSound(point)

	
def onclick3D(event,ax):		#click on the plot
	if event.inaxes!=None:	#inside the plot
		coords=find3DCoords(event, ax)
		point=-1
		for i in range (0,n):	#search the nearest point
			minX=coords[0]-1
			maxX=coords[0]+1
			minY=coords[1]-1
			maxY=coords[1]+1
			minZ = coords[2] - 1
			maxZ =coords[2] + 1
			if (xy[i][0]>=minX and xy[i][0]<=maxX and xy[i][1]>=minY and xy[i][1]<=maxY and xy[i][2]>=minZ and xy[i][2]<=maxZ):	#near enough
				if(point!=-1):		#if a point have been already found
					#print(i," vs ",point)
					distanceEvent=math.sqrt(pow(xy[i][0]-coords[0],2)+pow(xy[i][1]-coords[1],2)+pow(xy[i][2]-coords[2],2))	#distance between the event and the point we are looking at
					distancePoint=math.sqrt(pow(xy[point][0]-coords[0],2)+pow(xy[point][1]-coords[1],2)+pow(xy[i][2]-coords[2],2))	#distance between the event and the closest pont we have found
					print(distanceEvent," vs ",distancePoint)
					if(distancePoint>distanceEvent): 		#find the nearest
						point=i
				else:
					point=i
		playSound(point)

def create2DPlot():
	fig, ax = plt.subplots()
	### generate random points
	for i in range(0, n):
		xy.append((random.randint(0, i + 2), random.randint(0, i + 2)))
	###
	### fixed list
	# x = [1, 2, 3, 4, 5]
	# y = [1, 2, 3, 4, 5]
	# y2 = [1, 4, 9, 16, 25]
	###
	x = [i[0] for i in xy]
	y = [i[1] for i in xy]
	### place the points
	ax.scatter(x, y, c='red')
	# ax.scatter(x, y2, c = 'blue')
	###
	# bind press event with onclick function
	cid = fig.canvas.mpl_connect('button_press_event',lambda event: onclick2D(event,ax))
	# plot labelling
	plt.xlabel("X")
	plt.ylabel("Y")
	plt.legend(loc='upper left')
	plt.title("PLOT")
	plt.show()


def create3DPlot():
	fig = plt.figure()
	ax = fig.add_subplot(projection='3d')
	### generate random points
	for i in range(0, n):
		xy.append((random.randint(0, i + 2), random.randint(0, i + 2),random.randint(0, i + 2)))
	###
	### fixed list
	# x = [1, 2, 3, 4, 5]
	# y = [1, 2, 3, 4, 5]
	# y2 = [1, 4, 9, 16, 25]
	###
	x = [i[0] for i in xy]
	y = [i[1] for i in xy]
	z = [i[2] for i in xy]
	### place the points
	ax.scatter(x, y,z ,c='red')
	# ax.scatter(x, y2, c = 'blue')
	###
	# bind press event with onclick function
	cid = fig.canvas.mpl_connect('button_press_event',lambda event: onclick3D(event,ax))
	# plot labelling
	ax.set_xlabel("X")
	ax.set_ylabel("Y")
	ax.set_zlabel("Z")
	#plt.legend(loc='upper left')
	plt.title("PLOT")
	plt.show()

if __name__ == "__main__":
	if dim3D:
		create3DPlot()
	else:
		create2DPlot()






