import os.path
#import pyaudio
import wave
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
alreadyStarted=False
stream=None
wf=None
paudio=None

plot=None

dotSize=20
protoSize=25
dotLineWidth=1
protoLineWidth=1

xyz=[]
utt=[]
colorsOrdered=[]
xyzOrdered=[]
uttOrdered=[]
lPrototypes=None
lCriticisms=None

def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)

def pyAudioStarting(file):
	global stream
	global wf
	global paudio
	print("start")
	wf = wave.open(file, 'rb')
	paudio = pyaudio.PyAudio()
	stream = paudio.open(format=paudio.get_format_from_width(wf.getsampwidth()),
					channels=wf.getnchannels(),
					rate=wf.getframerate(),
					output=True,
					stream_callback=callback
					)
	stream.start_stream()

def setOptions(dotS=20,dotLineW=1,protoS=-1,protoLineW=-1):
	global dotSize
	global protoSize
	global dotLineWidth
	global protoLineWidth
	dotSize=dotS
	protoSize=protoS
	dotLineWidth=dotLineW
	protoLineWidth=protoLineW

def setSound(dir):
	global sounds_dir
	sounds_dir=dir


def playSound(i,xy,utt):
	global stream
	global wf
	global p
	if (i != None and i!=-1):  # if a point have been found
		print(i)
		spk=utt[i[0]][i[1]].split("-")
		print("The point is :", xy[i[0]][i[1]])
		print("The speaker is :",spk[0])
		if stream!=None:
			# stop stream
			stream.stop_stream()
			stream.close()
			wf.close()
			# close PyAudio
			paudio.terminate()
			print("stop")
		#if (i <= len(utt)):  # if a sound exist
		#	print(wavLink.getFileWithPathToData(sounds_dir,utt[i]))
			#playsound(s[i])
		#pyAudioStarting("../resources/sounds/1.wav")


def rePlot(spk):
	if plot!=None:
		fig, ax = plot.subplots()
		x=[]
		y=[]
		ct=0

		for i in range(len(uttOrdered)):
			z=uttOrdered[i][0].split("-")
			z=z[0]
			if z==spk:
				ct=i
				for j in range (len(xyzOrdered[i])):
					x.append(xyzOrdered[i][j][0])
					y.append(xyzOrdered[i][j][1])
		plt.scatter(x,y,s=dotSize,color=colorsOrdered[ct],edgecolors='black',linewidth=dotLineWidth)
		if lPrototypes!=None:
			if ct<=len(lPrototypes):
				p=lPrototypes[ct]
				p=p[1:]
				plt.scatter(p[0], p[1], color=colorsOrdered[ct],s=protoSize, marker="D",edgecolors='black',linewidth=protoLineWidth)
				c=lCriticisms[ct]
				c=c[1:]
				plt.scatter(c[0], c[1], color=colorsOrdered[ct], s=protoSize, marker="^", edgecolors='black',linewidth=protoLineWidth)
				d=math.dist(p,c)
				legend="dist with criticism:"+str(round(d,2))
				plt.plot([],[],color='white',label=legend)
				s=0
				if len(x)>0:
					for i in range(len(x)):
						s=s+math.dist(p,[x[i],y[i]])
					d=s/len(x)
					legend="mean dist:"+str(round(d,2))
					plt.plot([],[],color='white',label=legend)
				plt.legend()
		title = "Speaker :" + str(spk)
		cid = fig.canvas.mpl_connect('button_press_event', lambda event: onclick2DPlaySound(event, ax, xyz, utt))

		plt.title(title)
		plt.show()
		# on the plot
		# plot.clf()
		# fig=plot.gcf()
		# ax=fig.add_subplot()
		# ax.scatter(xy[id][0], xy[id][1])
		# title="Speaker :"+str(spk)
		# plot.title(title)
		# fig.canvas.draw_idle()
		# plot.show()

def find3DCoords(event, ax):
	pressed = ax.button_pressed
	ax.button_pressed = -1  # some value that doesn't make sense.
	coords = ax.format_coord(event.xdata, event.ydata)  # coordinates string in the form x=value, y=value, z= value
	ax.button_pressed = pressed
	temp = re.findall(r"[-+]?\d*\.\d+|\d+", coords)
	res=list(map(float,temp))
	print(res)
	return res

def onclick2DOpenNewPlot(event,ax,xy,utt):		#click on the plot
	global plot
	if event.inaxes!=None:	#inside the plot
		print("The click : ",event.xdata," ",event.ydata)
		point=-1
		for i in range (0,len(xy)):	#search the nearest point
			for j in range(len(xy[i])):
				minX=event.xdata-0.5
				maxX=event.xdata+0.5
				minY=event.ydata-0.5
				maxY=event.ydata+0.5
				if (xy[i][j][0]>=minX and xy[i][j][0]<=maxX and xy[i][j][1]>=minY and xy[i][j][1]<=maxY):	#near enough
					if(point!=-1):		#if a point have been already found
						#print(i," vs ",point)
						distanceEvent=math.sqrt(pow(xy[i][j][0]-event.xdata,2)+pow(xy[i][j][1]-event.ydata,2))	#distance between the event and the point we are looking at
						distancePoint=math.sqrt(pow(xy[point[0]][point[1]][0]-event.xdata,2)+pow(xy[point[0]][point[1]][1]-event.ydata,2))	#distance between the event and the closest pont we have found
						#print(distanceEvent," vs ",distancePoint)
						if(distancePoint>distanceEvent): 		#find the nearest
							point=[i,j]
					else:
						point=[i,j]
		spk = utt[point[0]][point[1]].split("-")
		rePlot(spk[0])

def onclick2DPlaySound(event,ax,xy,utt):		#click on the plot
	global plot
	if event.inaxes!=None:	#inside the plot
		print("The click : ",event.xdata," ",event.ydata)
		point=-1
		for i in range (0,len(xy)):	#search the nearest point
			for j in range(len(xy[i])):
				minX=event.xdata-0.5
				maxX=event.xdata+0.5
				minY=event.ydata-0.5
				maxY=event.ydata+0.5
				if (xy[i][j][0]>=minX and xy[i][j][0]<=maxX and xy[i][j][1]>=minY and xy[i][j][1]<=maxY):	#near enough
					if(point!=-1):		#if a point have been already found
						#print(i," vs ",point)
						distanceEvent=math.sqrt(pow(xy[i][j][0]-event.xdata,2)+pow(xy[i][j][1]-event.ydata,2))	#distance between the event and the point we are looking at
						distancePoint=math.sqrt(pow(xy[point[0]][point[1]][0]-event.xdata,2)+pow(xy[point[0]][point[1]][1]-event.ydata,2))	#distance between the event and the closest pont we have found
						#print(distanceEvent," vs ",distancePoint)
						if(distancePoint>distanceEvent): 		#find the nearest
							point=[i,j]
					else:
						point=[i,j]
		playSound(point,xy,utt)


	
def onclick3D(event,ax,xyz,utt):		#click on the plot
	if event.inaxes!=None:	#inside the plot
		coords=find3DCoords(event, ax)
		point=-1
		for i in range (0,len(xyz)):	#search the nearest point
			for j in range(len(xyz[i])):
				minX=coords[0]-1
				maxX=coords[0]+1
				minY=coords[1]-1
				maxY=coords[1]+1
				minZ = coords[2] - 1
				maxZ =coords[2] + 1
				if (xyz[i][j][0]>=minX and xyz[i][j][0]<=maxX and xyz[i][j][1]>=minY and xyz[i][j][1]<=maxY and xyz[i][j][2]>=minZ and xyz[i][j][2]<=maxZ):	#near enough
					if(point!=-1):		#if a point have been already found
						#print(i," vs ",point)
						distanceEvent=math.sqrt(pow(xyz[i][j][0]-coords[0],2)+pow(xyz[i][j][1]-coords[1],2)+pow(xyz[i][j][2]-coords[2],2))	#distance between the event and the point we are looking at
						distancePoint=math.sqrt(pow(xyz[point[0]][point[1]][0]-coords[0],2)+pow(xyz[point[0]][point[1]][1]-coords[1],2)+pow(xyz[point[0]][point[1]][2]-coords[2],2))	#distance between the event and the closest pont we have found
						#print(distanceEvent," vs ",distancePoint)
						if(distancePoint>distanceEvent): 		#find the nearest
							point=[i,j]
					else:
						point=[i,j]
		playSound(point,xyz,utt)


def chooseColor(xy,utt):
	colors=[]
	loc=[]
	newXY=[]
	ctutt=0
	for i in utt:
		idL=i.split("-",1)
		id=idL[0]
		ct=0
		find=False
		for j in loc:
			if j==id:
				#colors.append(colors[ct])
				newXY[ct].append(xy[ctutt])
				find=True
				break
			ct += 1
		if find==False:
			loc.append(id)
			# if (rgb+1>=255):
			# 	rgb=0
			rgb=(random.uniform(0.05,1),random.uniform(0.05,1),random.uniform(0.05,1))
			colors.append(rgb)
			newXY.append([])
			newXY[-1].append(xy[ctutt])
			#print(id, " not found :", rgb)
		#print(id)
		ctutt+=1
	#for i in newutt:
	#	print(i)
	print("Number of speakers:",len(colors))
	return colors,newXY,loc

def chooseColor2(xy,utt):
	colors=[]
	loc=[]
	newXY=[]
	ctutt=0
	for i in range(len(utt)):
		rgb = (random.uniform(0.05, 1), random.uniform(0.05, 1), random.uniform(0.05, 1))
		colors.append(rgb)

	#for i in newutt:
	#	print(i)
	print("Number of speakers:",len(colors))
	return colors,xy,utt

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

def create2DPlot(utt2D,xy,show=False,filePlotExport="plot.jpeg",dotS=20,dotLineW=1,soundsdir="",detailSpeakerClick=True):
	global plot
	global colorsOrdered
	global xyzOrdered
	global uttOrdered
	global lPrototypes
	global lCriticisms
	global xyz
	global utt
	xyz=xy
	utt=utt2D
	setSound(soundsdir)
	setOptions(dotS, dotLineW)
	plot=plt
	fig, ax = plot.subplots()
	colorsOrdered,xyzOrdered,uttOrdered=chooseColor2(xy, utt)
	x=[]
	y=[]
	for i in xyzOrdered: 	# for each speaker
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
	for i in range (0,len(xyzOrdered)):
		#print()
		#print(colors[i])
		#print(x[i])
		#print(y[i])
		#print("")
		#ax.scatter(x[i],y[i])
		ax.scatter(x[i],y[i],s=dotSize,color=colorsOrdered[i],edgecolors='black',linewidth=dotLineWidth)
	#ax.scatter(x, y,  c=colormap[colors])
	# 	###
	# bind press event with onclick function
	if detailSpeakerClick:
		cid = fig.canvas.mpl_connect('button_press_event', lambda event: onclick2DOpenNewPlot(event, ax, xy, utt))
	else:
		cid = fig.canvas.mpl_connect('button_press_event',lambda event: onclick2DPlaySound(event,ax,xy,utt))
	# plot labelling
	plot.xlabel("X")
	plot.ylabel("Y")
	plot.legend(loc='upper left')
	plot.title("PLOT")
	if checkDir(filePlotExport):
		plot.savefig(filePlotExport,dpi=1920)
		print("Plot save to", filePlotExport)
	if (show==True):
		plot.show()

def create2DPlotPrototypes(utt2D,xy,prototypes,criticisms,show=False,filePlotExport="plot.jpeg",dotS=20,protoS=25,dotLineW=1,protoLineW=1,soundsdir="",oneDotPerSpeaker=True,detailSpeakerClick=True):
	global plot
	global colorsOrdered
	global xyzOrdered
	global uttOrdered
	global lPrototypes
	global lCriticisms
	global xyz
	global utt
	xyz=xy
	utt=utt2D
	setOptions(dotS,dotLineW,protoS,protoLineW)
	setSound(soundsdir)
	plot=plt
	#plot.ion()
	fig, ax = plot.subplots()
	colorsOrdered,xyzOrdered,uttOrdered=chooseColor2(xy, utt2D)
	lPrototypes=prototypes
	lCriticisms=criticisms
	if oneDotPerSpeaker!=True:
		x=[]
		y=[]

		for i in xyzOrdered: 	# for each speaker
			#print(i)
			x.append([])
			y.append([])
			for j in i:
				x[-1].append(j[0])	# add the utt
				y[-1].append(j[1])
		for i in range (0,len(xyzOrdered)):
			ax.scatter(x[i],y[i],s=dotSize,color=colorsOrdered[i],edgecolors='black',linewidth=dotLineWidth)
	xp=[]
	yp=[]
	for i in prototypes:
		#p=xyzOrdered[i[0]][i[1]]
		xp.append(i[1])	# add the utt
		yp.append(i[2])
	xc=[]
	yc=[]
	for i in criticisms:
		#c = xyzOrdered[i[0]][i[1]]
		xc.append(i[1])  # add the utt
		yc.append(i[2])
	for i in range (len(xp)):
		ax.scatter(xp[i], yp[i], color=colorsOrdered[i],s=protoSize, marker="D",edgecolors='black',linewidth=protoLineWidth)
	for i in range (len(xc)):
		ax.scatter(xc[i], yc[i],color=colorsOrdered[i], s=protoSize, marker="^",edgecolors='black',linewidth=protoLineWidth)
		#plt.clabel(ax,colors='blue')
	if detailSpeakerClick:
		cid = fig.canvas.mpl_connect('button_press_event', lambda event: onclick2DOpenNewPlot(event, ax, xy, utt))
	else:
		cid = fig.canvas.mpl_connect('button_press_event',lambda event: onclick2DPlaySound(event,ax,xy,utt))
	plot.xlabel("X")
	plot.ylabel("Y")
	#plot.legend(loc='upper left')
	plot.title("PLOT")

	if checkDir(filePlotExport):
		plot.savefig(filePlotExport,dpi=1920)
		print("Plot save to",filePlotExport )
	#plot.ioff()
	if (show==True):
	 	plot.show()

def create3DPlotPrototypes(utt3D,xyz3D,prototypes,criticisms,show=False,filePlotExport="plot.jpeg",dotSize=20,protoSize=25,dotLineWidth=1,protoLineWidth=1,soundsdir=""):
	global plot
	global colorsOrdered
	global xyzOrdered
	global uttOrdered
	global lPrototypes
	global lCriticisms
	global xyz
	global utt
	xyz=xyz3D
	utt=utt3D
	setSound(soundsdir)
	fig = plt.figure()
	colors, xyzOrdered,uttOrdered = chooseColor2(xyz3D, utt3D)
	x = []
	y = []
	z= []
	for i in xyzOrdered:
		x.append([])
		y.append([])
		z.append([])
		for j in i:
			x[- 1].append(j[0])
			y[- 1].append(j[1])
			z[- 1].append(j[1])
	xp=[]
	yp=[]
	zp=[]
	for i in prototypes:
		#p = xyzOrdered[i[0]][i[1]]
		xp.append(i[1])	# add the utt
		yp.append(i[2])
		zp.append(i[3])
	xc=[]
	yc=[]
	zc=[]
	for i in criticisms:
		#c = xyzOrdered[i[0]][i[1]]
		xc.append(i[1])	# add the utt
		yc.append(i[2])
		zc.append(i[3])
	ax = fig.add_subplot(projection='3d')
	### place the points
	for i in range (0,len(xyzOrdered)):
		ax.scatter(x[i],y[i],z[i],s=dotSize,color=colors[i],edgecolors='black',linewidth=dotLineWidth)
	###
	for i in range (0,len(prototypes)):
		ax.scatter(xp[i], yp[i],zp[i], s=(dotSize*1.1), marker="D",edgecolors='black',linewidth=protoLineWidth)
	for i in range (0,len(criticisms)):
		ax.scatter(xc[i], yc[i],zc[i], s=(dotSize*1.1), marker="^",edgecolors='black',linewidth=protoLineWidth)
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
		print("Plot save to", filePlotExport)
	if (show==True):
		plt.show()

def create3DPlot(utt,xyz,show=False,filePlotExport="plot.jpeg",dotSize=20,soundsdir=""):
	setSound(soundsdir)
	fig = plt.figure()
	colors, newutt = chooseColor2(xyz, utt)
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
		print("Plot save to", filePlotExport)
	if (show==True):
		plt.show()

if __name__ == "__main__":
	xy=generateRandomGraphic()
	if len(xy[0])==3:
		create3DPlot(xy)
	else:
		create2DPlot(xy)






