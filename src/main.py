import matplotlib.pyplot as plt
import numpy as np
from playsound import playsound
import math
import random

n=10		#number of point

s=[]		#sound list
#s=["../ressources/1.wav","","","",""]
for i in range (0,n):
	s.append("../ressources/1.wav")


def onclick(event):		#click on the plot
	if event.inaxes!=None:	#inside the plot
		print(event.xdata," ",event.ydata)
		point=-1
		for i in range (0,n):	#search the nearest point
			minX=event.xdata-0.5
			maxX=event.xdata+0.5
			minY=event.ydata-0.5
			maxY=event.ydata+0.5
			if (x[i]>=minX and x[i]<=maxX and y[i]>=minY and y[i]<=maxY):	#near enough
				if(point!=-1):		#if a point have been already found
					#print(i," vs ",point)
					distanceEvent=math.sqrt(pow(x[i]-event.xdata,2)*pow(y[i]-event.ydata,2))	#distance between the event and the point we are looking at
					distancePoint=math.sqrt(x[point]-pow(event.xdata,2)*pow(y[point]-event.ydata,2))	#distance between the event and the closest pont we have found
					#print(distanceEvent," vs ",distancePoint)
					if(distancePoint>distanceEvent): 		#find the nearest
						point=i
				else:
					point=i
		if (point>=0):	#if a point have been found
			print("The point is :",x[point]," ",y[point])
			if(point<=len(s)):	#if a sound exist
				print("play")
				playsound(s[point])
	


fig,ax=plt.subplots()

### generate random points
x=[]
y=[]
for i in range (0,n):
	x.append(random.randint(0, i+2))
	y.append(random.randint(0, i+4))
###

### fixed list
#x = [1, 2, 3, 4, 5]
#y = [1, 2, 3, 4, 5]
#y2 = [1, 4, 9, 16, 25]
###

### place the points
ax.scatter(x, y, c = 'red')
#ax.scatter(x, y2, c = 'blue')
###

#bind press event with onclick function
cid = fig.canvas.mpl_connect('button_press_event', onclick)

# plot labelling
plt.xlabel("X")
plt.ylabel("Y")
plt.legend(loc='upper left')
plt.title("PLOT")
plt.show()



