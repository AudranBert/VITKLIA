import re
import matplotlib.pyplot as plt
import numpy as np
from playsound import playsound
import math

s=[]		#sound list
#s=["../ressources/1.wav","","","",""]
for i in range (0,10):
	s.append("../ressources/sounds/1.wav")


def playSound(i,xy):
	if (i >= 0):  # if a point have been found
		print("The point is :", xy[i])
		if (i <= len(s)):  # if a sound exist
			print("play")
			#playsound(s[i])

def find3DCoords(event, ax):
	pressed = ax.button_pressed
	ax.button_pressed = -1  # some value that doesn't make sense.
	coords = ax.format_coord(event.xdata, event.ydata)  # coordinates string in the form x=value, y=value, z= value
	ax.button_pressed = pressed
	temp = re.findall(r"[-+]?\d*\.\d+|\d+", coords)
	res=list(map(float,temp))
	print(res)
	return res

def onclick2D(event,ax,xy):		#click on the plot
	if event.inaxes!=None:	#inside the plot
		print(event.xdata," ",event.ydata)
		point=-1
		for i in range (0,len(xy)):	#search the nearest point
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
		playSound(point,xy)

	
def onclick3D(event,ax,xyz):		#click on the plot
	if event.inaxes!=None:	#inside the plot
		coords=find3DCoords(event, ax)
		point=-1
		for i in range (0,len(xyz)):	#search the nearest point
			minX=coords[0]-1
			maxX=coords[0]+1
			minY=coords[1]-1
			maxY=coords[1]+1
			minZ = coords[2] - 1
			maxZ =coords[2] + 1
			if (xyz[i][0]>=minX and xyz[i][0]<=maxX and xyz[i][1]>=minY and xyz[i][1]<=maxY and xyz[i][2]>=minZ and xyz[i][2]<=maxZ):	#near enough
				if(point!=-1):		#if a point have been already found
					#print(i," vs ",point)
					distanceEvent=math.sqrt(pow(xyz[i][0]-coords[0],2)+pow(xyz[i][1]-coords[1],2)+pow(xyz[i][2]-coords[2],2))	#distance between the event and the point we are looking at
					distancePoint=math.sqrt(pow(xyz[point][0]-coords[0],2)+pow(xyz[point][1]-coords[1],2)+pow(xyz[i][2]-coords[2],2))	#distance between the event and the closest pont we have found
					print(distanceEvent," vs ",distancePoint)
					if(distancePoint>distanceEvent): 		#find the nearest
						point=i
				else:
					point=i
		playSound(point,xyz)

def create2DPlot(xy):
	fig, ax = plt.subplots()

	x = [i[0] for i in xy]
	y = [i[1] for i in xy]
	### place the points
	ax.scatter(x, y, c='red')
	# ax.scatter(x, y2, c = 'blue')
	###
	# bind press event with onclick function
	cid = fig.canvas.mpl_connect('button_press_event',lambda event: onclick2D(event,ax,xy))
	# plot labelling
	plt.xlabel("X")
	plt.ylabel("Y")
	plt.legend(loc='upper left')
	plt.title("PLOT")
	plt.show()


def create3DPlot(xyz):
	fig = plt.figure()
	ax = fig.add_subplot(projection='3d')
	x = [i[0] for i in xyz]
	y = [i[1] for i in xyz]
	z = [i[2] for i in xyz]
	### place the points
	ax.scatter(x, y,z ,c='red')
	# ax.scatter(x, y2, c = 'blue')
	###
	# bind press event with onclick function
	cid = fig.canvas.mpl_connect('button_press_event',lambda event: onclick3D(event,ax,xyz))
	# plot labelling
	ax.set_xlabel("X")
	ax.set_ylabel("Y")
	ax.set_zlabel("Z")
	#plt.legend(loc='upper left')
	plt.title("PLOT")
	plt.show()



if __name__ == "__main__":
	xy=generateRandomGraphic()
	if len(xy[0])==3:
		create3DPlot(xy)
	else:
		create2DPlot(xy)






