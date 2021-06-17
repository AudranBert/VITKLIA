import os.path
import re
import matplotlib.pyplot as plt
from playsound import playsound
import math
import wavLink
import random

s=[]		#sound list
#s=["../ressources/1.wav","","","",""]
#for i in range (0,10):
#	s.append("../ressources/sounds/1.wav")

sounds_dir=""

def setSound(dir):
	global sounds_dir
	sounds_dir=dir


def playSound(i,xy,sounds):
	if (i >= 0):  # if a point have been found
		spk=sounds[i].split("-")
		print("The point is :", xy[i])
		print("The speaker is :",spk[0])
		if (i <= len(sounds)):  # if a sound exist
			print(wavLink.getFileWithPathToData(sounds_dir,sounds[i]))
			print("start")
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

def onclick2D(event,ax,xy,sounds):		#click on the plot
	if event.inaxes!=None:	#inside the plot
		print("The click : ",event.xdata," ",event.ydata)
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
		playSound(point,xy,sounds)

	
def onclick3D(event,ax,xyz,sounds):		#click on the plot
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
		playSound(point,xyz,sounds)

def chooseColor(xy,utt):
	colors=[]
	loc=[]
	newutt=[]
	ctutt=0
	for i in utt:
		idL=i.split("-",1)
		id=idL[0]
		ct=0
		find=False
		for j in loc:
			if j==id:
				#colors.append(colors[ct])
				newutt[ct].append(xy[ctutt])
				find=True
				break
			ct += 1
		if find==False:
			loc.append(id)
			# if (rgb+1>=255):
			# 	rgb=0
			rgb=(random.uniform(0.05,1),random.uniform(0.05,1),random.uniform(0.05,1))
			colors.append(rgb)
			newutt.append([])
			newutt[len(newutt)-1].append(xy[ctutt])
			#print(id, " not found :", rgb)
		#print(id)
		ctutt+=1
	#for i in newutt:
	#	print(i)
	print("Number of speakers:",len(colors))
	return colors,newutt

def checkDir(path):
	p=path.split("/")
	p.pop()
	np=""
	for i in p:
		np+=i+os.path.sep
	if (os.path.isdir(np)):
		return True
	else:
		print("Directory :"+np+" does not exist")
		return False

def create2DPlot(xy,utt,show=False,filePlotExport="plot.jpeg",dotSize=20,soundsdir=""):
	setSound(soundsdir)
	fig, ax = plt.subplots()
	colors,newutt=chooseColor(xy, utt)
	x=[]
	y=[]
	for i in newutt: 	# for each speaker
		x.append([])
		y.append([])
		for j in i:
			x[len(x)-1].append(j[0])	# add the utt
			y[len(y)-1].append(j[1])
	#x = [i[0] for i in newutt]
	#y = [i[1] for i in newutt]
	#colormap = np.array(['r', 'g', 'b'])
	# for i in range(0,len(colors)):
	#
	# 	### place the points
	# 	ax.scatter(x[i], y[i], c=[colors[i]])
	# 	# ax.scatter(x, y2, c = 'blue')
	for i in range (0,len(newutt)):
		#print()
		#print(colors[i])
		#print(x[i])
		#print(y[i])
		#print("")
		#ax.scatter(x[i],y[i])
		ax.scatter(x[i],y[i],s=dotSize,color=colors[i])
	#ax.scatter(x, y,  c=colormap[colors])
	# 	###
	# bind press event with onclick function
	cid = fig.canvas.mpl_connect('button_press_event',lambda event: onclick2D(event,ax,xy,utt))
	# plot labelling
	plt.xlabel("X")
	plt.ylabel("Y")
	plt.legend(loc='upper left')
	plt.title("PLOT")
	if checkDir(filePlotExport):
		plt.savefig(filePlotExport,dpi=1920)
	if (show==True):
		plt.show()

def create2DPlotPrototypes(xy,prototypes,criticisms,utt,show=False,filePlotExport="plot.jpeg",dotSize=20,soundsdir=""):
	setSound(soundsdir)
	fig, ax = plt.subplots()
	colors,newutt=chooseColor(xy, utt)
	x=[]
	y=[]
	for i in newutt: 	# for each speaker
		x.append([])
		y.append([])
		for j in i:
			x[len(x)-1].append(j[0])	# add the utt
			y[len(y)-1].append(j[1])
	xp=[]
	yp=[]
	for i in prototypes:
		p=newutt[i[0]][i[1]]
		xp.append(p[0])	# add the utt
		yp.append(p[1])
	xc=[]
	yc=[]
	for i in criticisms:
		c = newutt[i[0]][i[1]]
		xc.append(c[0])  # add the utt
		yc.append(c[1])
	for i in range (0,len(newutt)):
		ax.scatter(x[i],y[i],s=dotSize,color=colors[i])
	for i in range (0,len(prototypes)):
		ax.scatter(xp[i], yp[i], s=(dotSize*0.9), marker="D",color='black')
	for i in range (0,len(criticisms)):
		ax.scatter(xc[i], yc[i], s=(dotSize*0.9), marker="^",color='black')
		#plt.clabel(ax,colors='blue')
	cid = fig.canvas.mpl_connect('button_press_event',lambda event: onclick2D(event,ax,xy,utt))
	plt.xlabel("X")
	plt.ylabel("Y")
	plt.legend(loc='upper left')
	plt.title("PLOT")
	if checkDir(filePlotExport):
		plt.savefig(filePlotExport,dpi=1920)
		print("Plot save to",filePlotExport, )
	if (show==True):
		plt.show()

def create3DPlotPrototypes(xyz,prototypes,criticisms,utt,show=False,filePlotExport="plot.jpeg",dotSize=20,soundsdir=""):
	setSound(soundsdir)
	fig = plt.figure()
	colors, newutt = chooseColor(xyz, utt)
	x = []
	y = []
	z= []
	for i in newutt:
		x.append([])
		y.append([])
		z.append([])
		for j in i:
			x[len(x) - 1].append(j[0])
			y[len(y) - 1].append(j[1])
			z[len(z) - 1].append(j[1])
	xp=[]
	yp=[]
	zp=[]
	for i in prototypes:
		xp.append(i[0])	# add the utt
		yp.append(i[1])
		zp.append(i[2])
	xc=[]
	yc=[]
	zc=[]
	for i in criticisms:
		xc.append(i[0])	# add the utt
		yc.append(i[1])
		zc.append(i[2])
	ax = fig.add_subplot(projection='3d')
	### place the points
	for i in range (0,len(newutt)):
		ax.scatter(x[i],y[i],z[i],s=dotSize,color=colors[i])
	###
	for i in range (0,len(prototypes)):
		ax.scatter(xp[i], yp[i],zp[i], s=(dotSize*1.1), marker="D",color='black')
	for i in range (0,len(criticisms)):
		ax.scatter(xc[i], yc[i],zc[i], s=(dotSize*1.1), marker="^",color='black')
	# bind press event with onclick function
	cid = fig.canvas.mpl_connect('button_press_event',lambda event: onclick3D(event,ax,xyz,utt))
	# plot labelling
	ax.set_xlabel("X")
	ax.set_ylabel("Y")
	ax.set_zlabel("Z")
	#plt.legend(loc='upper left')
	plt.title("PLOT")
	if checkDir(filePlotExport):
		plt.savefig(filePlotExport,dpi=1920)
	if (show==True):
		plt.show()

def create3DPlot(xyz,utt,show=False,filePlotExport="plot.jpeg",dotSize=20,soundsdir=""):
	setSound(soundsdir)
	fig = plt.figure()
	colors, newutt = chooseColor(xyz, utt)
	x = []
	y = []
	z= []
	for i in newutt:
		x.append([])
		y.append([])
		z.append([])
		for j in i:
			x[len(x) - 1].append(j[0])
			y[len(y) - 1].append(j[1])
			z[len(z) - 1].append(j[1])
	ax = fig.add_subplot(projection='3d')
	# x = [i[0] for i in xyz]
	# y = [i[1] for i in xyz]
	# z = [i[2] for i in xyz]
	### place the points
	for i in range (0,len(newutt)):
		#print()
		#print(colors[i])
		#print(x[i])
		#print(y[i])
		#print("")
		#ax.scatter(x[i],y[i])
		ax.scatter(x[i],y[i],z[i],s=dotSize,color=colors[i])
	#ax.scatter(x, y,z ,c='red')
	# ax.scatter(x, y2, c = 'blue')
	###
	# bind press event with onclick function
	cid = fig.canvas.mpl_connect('button_press_event',lambda event: onclick3D(event,ax,xyz,utt))
	# plot labelling
	ax.set_xlabel("X")
	ax.set_ylabel("Y")
	ax.set_zlabel("Z")
	#plt.legend(loc='upper left')
	plt.title("PLOT")
	if checkDir(filePlotExport):
		plt.savefig(filePlotExport,dpi=1920)
	if (show==True):
		plt.show()

if __name__ == "__main__":
	xy=generateRandomGraphic()
	if len(xy[0])==3:
		create3DPlot(xy)
	else:
		create2DPlot(xy)






