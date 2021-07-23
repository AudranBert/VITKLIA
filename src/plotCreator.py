import os.path
import pyaudio
import wave
import run
import re
import matplotlib.pyplot as plt
from playsound import playsound
import math
import wavLink
import random

s = []  # sound list
# s=["../ressources/1.wav","","","",""]
# for i in range (0,10):
#	s.append("../ressources/sounds/1.wav")

sounds_dir = ""
alreadyStarted = False
stream = None
wf = None
paudio = None

plot = None

dotSize = 20
protoSize = 25
dotLineWidth = 1
protoLineWidth = 1

xyz = []
utt = []
colorsOrdered = []
xyzOrdered = []
uttOrdered = []
lPrototypes = None
lCriticisms = None

cp = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]


def callback(in_data, frame_count, time_info, status):
	'''
	callback for the audio
	:param in_data:
	:param frame_count:
	:param time_info:
	:param status:
	:return:
	'''
	data = wf.readframes(frame_count)
	return (data, pyaudio.paContinue)


def pyAudioStarting(file):
	'''
	start a sound if it exists
	:param file:
	:return:
	'''
	global stream
	global wf
	global paudio
	print("start ", file)
	if os.path.isfile(file):
		wf = wave.open(file, 'rb')
		paudio = pyaudio.PyAudio()
		stream = paudio.open(format=paudio.get_format_from_width(wf.getsampwidth()),
							 channels=wf.getnchannels(),
							 rate=wf.getframerate(),
							 output=True,
							 stream_callback=callback
							 )
		stream.start_stream()


def setOptions(dotS=20, dotLineW=1, protoS=-1, protoLineW=-1):
	'''
	set global params for plots
	:param dotS:
	:param dotLineW:
	:param protoS:
	:param protoLineW:
	:return:
	'''
	global dotSize
	global protoSize
	global dotLineWidth
	global protoLineWidth
	dotSize = dotS
	protoSize = protoS
	dotLineWidth = dotLineW
	protoLineWidth = protoLineW


def setSound(dir):
	'''
	set sound path
	:param dir:
	:return:
	'''
	global sounds_dir
	sounds_dir = dir


def playSound(i, xy, utt):
	'''
	play a sound depending of the utt id
	:param i:
	:param xy:
	:param utt:
	:return:
	'''
	global stream
	global wf
	if (i is not None and i != -1):  # if a point have been found
		# print(i)
		#spk = utt[i[0]][i[1]].split("-")

		if stream is not None:
			# stop stream
			stream.stop_stream()
			stream.close()
			wf.close()
			# close PyAudio
			paudio.terminate()
			print("stop")
		# if (i <= len(utt)):  # if a sound exist

		# print(wavLink.getFileWithPathToData(sounds_dir,utt[i]))
		# playsound(s[i])
		thesound = wavLink.getFileWithPathToData(sounds_dir, utt[i[0]][i[1]])
		if thesound is not None:
			pyAudioStarting(thesound)
		# pyAudioStarting("../resources/sounds/1.wav")


def rePlot(spk):
	'''
	plot only one speaker when clicking on a point
	:param spk:
	:return:
	'''
	if plot is not None:
		fig, ax = plot.subplots()
		x = []
		y = []
		ct = 0

		for i in range(len(uttOrdered)):
			z = uttOrdered[i][0].split("-")
			z = z[0]
			if z == spk:
				ct = i
				for j in range(len(xyzOrdered[i])):
					x.append(xyzOrdered[i][j][0])
					y.append(xyzOrdered[i][j][1])
		plt.scatter(x, y, s=dotSize, color=colorsOrdered[ct], edgecolors='black', linewidth=dotLineWidth)
		if lPrototypes is not None:
			xp = []
			yp = []
			p = []
			for i in lPrototypes:
				spkP = run.uttToSpk(i[0])
				if spkP == spk:
					xp.append(i[1])
					yp.append(i[2])
					p.append(i[1:])

			xc = []
			yc = []
			c = []
			for i in lCriticisms:
				spkC = run.uttToSpk(i[0])
				if spkC == spk:
					xc.append(i[1])
					yc.append(i[2])
					c.append(i[1:])
			plt.scatter(xp, yp, color=colorsOrdered[ct], s=protoSize, marker="D", edgecolors='black',
						linewidth=protoLineWidth)
			plt.scatter(xc, yc, color=colorsOrdered[ct], s=protoSize, marker="^", edgecolors='black',
						linewidth=protoLineWidth)
			if len(p) > 0:
				if len(c) > 0:
					d = math.dist(p[0], c[0])
					legend = "dist with criticism:" + str(round(d, 2))
					plt.plot([], [], color='white', label=legend)
				s = 0
				if len(x) > 0 and len(p[0]) <= 2:
					for i in range(len(x)):
						s = s + math.dist(p[0], [x[i], y[i]])
					d = s / len(x)
					legend = "mean dist:" + str(round(d, 2))
					plt.plot([], [], color='white', label=legend)
				plt.legend()
		title = "Speaker :" + str(spk)
		cid = fig.canvas.mpl_connect('button_press_event', lambda event: onclick2D(event, ax, xyz, utt))
		plt.title(title)
		plt.show()


def find3DCoords(event, ax):
	'''
	find where the mouse is in 3D
	:param event:
	:param ax:
	:return:
	'''
	pressed = ax.button_pressed
	ax.button_pressed = -1  # some value that doesn't make sense.
	coords = ax.format_coord(event.xdata, event.ydata)  # coordinates string in the form x=value, y=value, z= value
	ax.button_pressed = pressed
	temp = re.findall(r"[-+]?\d*\.\d+|\d+", coords)
	res = list(map(float, temp))
	print("X=",res[0]," Y=",res[1]," Z=",res[2])
	return res



def onclick2D(event, ax, xy, utt, oneDotPerSpeaker=False,newPlot=False):  # click on the plot
	'''
	when click on a dot play the corresponding sound or make a new plot
	:param event:
	:param ax:
	:param xy:
	:param utt:
	:return:
	'''
	global plot
	if event.inaxes != None:  # inside the plot
		print("")
		print("The click : X=", event.xdata, " Y=", event.ydata)
		point = -1
		minX = event.xdata - 0.5
		maxX = event.xdata + 0.5
		minY = event.ydata - 0.5
		maxY = event.ydata + 0.5
		for i in range(0, len(xy)):  # search the nearest point
			for j in range(len(xy[i])):
				p = [utt[i][j], xy[i][j][0], xy[i][j][1]]
				if not oneDotPerSpeaker or p in lPrototypes or p in lCriticisms:
					if (xy[i][j][0] >= minX and xy[i][j][0] <= maxX and xy[i][j][1] >= minY and xy[i][j][1] <= maxY):  # near enough
						if (point != -1):  # if a point have been already found
							# print(i," vs ",point)
							distanceEvent = math.sqrt(pow(xy[i][j][0] - event.xdata, 2) + pow(xy[i][j][1] - event.ydata,2))  # distance between the event and the point we are looking at
							distancePoint = math.sqrt(pow(xy[point[0]][point[1]][0] - event.xdata, 2) + pow(xy[point[0]][point[1]][1] - event.ydata,2))  # distance between the event and the closest pont we have found
							# print(distanceEvent," vs ",distancePoint)
							if (distancePoint > distanceEvent):  # find the nearest
								point = [i, j]
						else:
							point = [i, j]
		if point != -1:
			spk = utt[point[0]][point[1]].split("-")
			print("The point is :",utt[point[0]][point[1]],":", xy[point[0]][point[1]])
			print("The speaker is :", spk[0])
			if newPlot:
				rePlot(spk[0])
			else:
				playSound(point, xyz, utt)


def onclick3D(event, ax, xyz, utt, oneDotPerSpeaker=False,newPlot=False):  # click on the plot
	'''
	when click on 3D plot play the corresponding sound or make a new plot
	:param event:
	:param ax:
	:param xyz:
	:param utt:
	:return:
	'''
	if event.inaxes != None:  # inside the plot
		coords = find3DCoords(event, ax)
		point = -1
		minX = coords[0] - 1
		maxX = coords[0] + 1
		minY = coords[1] - 1
		maxY = coords[1] + 1
		minZ = coords[2] - 1
		maxZ = coords[2] + 1
		for i in range(0, len(xyz)):  # search the nearest point
			for j in range(len(xyz[i])):
				p = [utt[i][j], xyz[i][j][0], xyz[i][j][1],xyz[i][j][2]]
				if not oneDotPerSpeaker or p in lPrototypes or p in lCriticisms:
					if (xyz[i][j][0] >= minX and xyz[i][j][0] <= maxX and xyz[i][j][1] >= minY and xyz[i][j][1] <= maxY and xyz[i][j][2] >= minZ and xyz[i][j][2] <= maxZ):  # near enough
						if (point != -1):  # if a point have been already found
							# print(i," vs ",point)
							distanceEvent = math.sqrt(
								pow(xyz[i][j][0] - coords[0], 2) + pow(xyz[i][j][1] - coords[1], 2) + pow(
									xyz[i][j][2] - coords[2],
									2))  # distance between the event and the point we are looking at
							distancePoint = math.sqrt(
								pow(xyz[point[0]][point[1]][0] - coords[0], 2) + pow(xyz[point[0]][point[1]][1] - coords[1],2) + pow(xyz[point[0]][point[1]][2] - coords[2],2))  # distance between the event and the closest pont we have found
							# print(distanceEvent," vs ",distancePoint)
							if (distancePoint > distanceEvent):  # find the nearest
								point = [i, j]
						else:
							point = [i, j]
		if point != -1:
			if newPlot:
				spk = utt[point[0]][point[1]].split("-")
				rePlot(spk[0])
			else:
				playSound(point, xyz, utt)


def chooseColor(xy, utt):
	'''
	choose a color for each speaker
	:param xy:
	:param utt:
	:return:
	'''
	colors = []
	for i in range(len(utt)):
		rgb = (random.uniform(0.05, 1), random.uniform(0.05, 1), random.uniform(0.05, 1))
		colors.append(rgb)
	print("Number of speakers:", len(colors))
	return colors, xy, utt


def chooseColorProto(utt, xy, colors, proto, crit):
	'''
	found the corresponding colors for prototypes and criticisms
	:param utt:
	:param xy:
	:param colors:
	:param proto:
	:param crit:
	:return:
	'''
	colorsProto = []
	colorsCrit = []
	for i in proto:
		for j in range(len(utt)):
			spkJ = run.uttToSpk(utt[j][0])
			spkI = run.uttToSpk(i[0])
			if spkJ == spkI:
				colorsProto.append(colors[j])
				break
	for i in crit:
		for j in range(len(utt)):
			spkJ = run.uttToSpk(utt[j][0])
			spkI = run.uttToSpk(i[0])
			if spkJ == spkI:
				colorsCrit.append(colors[j])
				break
	return colorsProto, colorsCrit


def findSpkInUtt(spk):
	'''
	find a given speaker in the uttOrdered list
	:param spk:
	:return:
	'''
	for i in range(len(uttOrdered)):
		if run.uttToSpk(uttOrdered[i][0]) == spk:
			return i


def autoScaleFunction(proto, crit, size):
	'''
	scale the size of prototypes depending of the mean dist between the prototypes and the others points of the speaker
	:param proto:
	:param crit:
	:param size:
	:return:
	'''
	autoScale = []
	min = size * 0.75
	maxSize = size * 3
	maxDist = 0
	for i in range(len(proto)):
		spkP = run.uttToSpk(proto[i][0])
		z = findSpkInUtt(spkP)
		d = 0
		for j in range(len(xyzOrdered[z])):
			d = d + math.dist(proto[i][1:], xyzOrdered[z][j])
		d = d / len(xyzOrdered[z])
		if d > maxDist:
			maxDist = d
	for i in range(len(proto)):
		spkP = run.uttToSpk(proto[i][0])
		z = findSpkInUtt(spkP)
		d = 0
		for j in range(len(xyzOrdered[z])):
			d = d + math.dist(proto[i][1:], xyzOrdered[z][j])
		d = d / len(xyzOrdered[z])
		d2 = (d * maxSize) / maxDist
		# print(d,"  ",d2)
		autoScale.append(d2)
	return autoScale


def create2DPlot(utt2D, xy, show=False, filePlotExport="plot.jpeg", dotS=20, dotLineW=1, soundsdir="",
				 detailSpeakerClick=True, title="Plot"):
	'''
	create a 2D plot
	:param utt2D:
	:param xy:
	:param show:
	:param filePlotExport:
	:param dotS:
	:param dotLineW:
	:param soundsdir:
	:param detailSpeakerClick:
	:return:
	'''
	global plot
	global colorsOrdered
	global xyzOrdered
	global uttOrdered
	global lPrototypes
	global lCriticisms
	global xyz
	global utt
	xyz = xy
	utt = utt2D
	setSound(soundsdir)
	setOptions(dotS, dotLineW)
	plot = plt
	fig, ax = plot.subplots()
	colorsOrdered, xyzOrdered, uttOrdered = chooseColor(xy, utt)
	x = []
	y = []
	for i in xyzOrdered:  # for each speaker
		x.append([])
		y.append([])
		for j in i:
			x[len(x) - 1].append(j[0])  # add the utt
			y[len(y) - 1].append(j[1])
	for i in range(0, len(xyzOrdered)):
		# ax.scatter(x[i],y[i])
		ax.scatter(x[i], y[i], s=dotSize, color=colorsOrdered[i], edgecolors='black', linewidth=dotLineWidth)
	# bind press event with onclick function
	cid = fig.canvas.mpl_connect('button_press_event', lambda event: onclick2D(event, ax, xy, utt,False,detailSpeakerClick))
	# plot labelling
	plot.xlabel("X")
	plot.ylabel("Y")
	plot.legend(loc='upper left')
	plot.title(title)
	f=filePlotExport.split("/")
	if len(f)>1:
		f.pop()
	f="".join(f)
	if run.checkPath(f):
		plot.savefig(filePlotExport, dpi=1920)
		print("Plot save to", filePlotExport)
	if (show == True):
		plot.show()


def create2DPlotPrototypes(utt2D, xy, prototypes, criticisms, show=False, filePlotExport="plot.jpeg", dotS=20,
						   protoS=25, dotLineW=1, protoLineW=1, soundsdir="", oneDotPerSpeaker=False,
						   detailSpeakerClick=True, autoScaleDot=False, title="Plot"):
	'''
	create a 2D plot with prototypes and criticisms
	:param utt2D:
	:param xy:
	:param prototypes:
	:param criticisms:
	:param show:
	:param filePlotExport:
	:param dotS:
	:param protoS:
	:param dotLineW:
	:param protoLineW:
	:param soundsdir:
	:param oneDotPerSpeaker:
	:param detailSpeakerClick:
	:param autoScaleDot:
	:return:
	'''
	global plot
	global colorsOrdered
	global xyzOrdered
	global uttOrdered
	global lPrototypes
	global lCriticisms
	global xyz
	global utt
	xyz = xy
	utt = utt2D
	setOptions(dotS, dotLineW, protoS, protoLineW)
	setSound(soundsdir)
	plot = plt
	# plot.ion()
	fig, ax = plot.subplots()
	colorsOrdered, xyzOrdered, uttOrdered = chooseColor(xy, utt2D)
	colorsProto, colorsCrit = chooseColorProto(uttOrdered, xyzOrdered, colorsOrdered, prototypes, criticisms)
	lPrototypes = prototypes
	lCriticisms = criticisms
	if oneDotPerSpeaker != True:
		x = []
		y = []

		for i in xyzOrdered:  # for each speaker
			# print(i)
			x.append([])
			y.append([])
			for j in i:
				x[-1].append(j[0])  # add the utt
				y[-1].append(j[1])
		for i in range(0, len(xyzOrdered)):
			ax.scatter(x[i], y[i], s=dotSize, color=colorsOrdered[i], edgecolors='black', linewidth=dotLineWidth)
	xp = []
	yp = []
	# print(len(lPrototypes))
	for i in lPrototypes:
		# p=xyzOrdered[i[0]][i[1]]
		xp.append(i[1])  # add the utt
		yp.append(i[2])
	xc = []
	yc = []
	# print(len(colorsProto))
	for i in lCriticisms:
		# c = xyzOrdered[i[0]][i[1]]
		xc.append(i[1])  # add the utt
		yc.append(i[2])
	autoScale = []
	if autoScaleDot:
		autoScale = autoScaleFunction(lPrototypes, lCriticisms, protoSize)
	for i in range(len(xc)):
		ax.scatter(xc[i], yc[i], color=colorsCrit[i], s=protoSize, marker="^", edgecolors='black',
				   linewidth=protoLineWidth)
	for i in range(len(xp)):
		# print(xp[i],"  ",xc[i])
		# print(i)
		if autoScaleDot:
			ax.scatter(xp[i], yp[i], color=colorsProto[i], s=autoScale[i], marker="D", edgecolors='black',
					   linewidth=protoLineWidth)
		else:
			ax.scatter(xp[i], yp[i], color=colorsProto[i], s=protoSize, marker="D", edgecolors='black',
					   linewidth=protoLineWidth)

		# plt.clabel(ax,colors='blue')
	cid = fig.canvas.mpl_connect('button_press_event', lambda event: onclick2D(event, ax, xy, utt,oneDotPerSpeaker, detailSpeakerClick))
	plot.xlabel("X")
	plot.ylabel("Y")
	# plot.legend(loc='upper left')
	plot.title(title)
	f=filePlotExport.split("/")
	if len(f)>1:
		f.pop()
	f="".join(f)
	if run.checkPath(f):
		plot.savefig(filePlotExport, dpi=1920)
		print("Plot save to", filePlotExport)
	# plot.ioff()
	if (show == True):
		plot.show()
	return plot


def create3DPlotPrototypes(utt3D, xyz3D, prototypes, criticisms, show=False, filePlotExport="plot.jpeg", dotS=20,protoS=25, dotLineW=1, protoLineW=1, soundsdir="", oneDotPerSpeaker=True,detailSpeakerClick=True, autoScaleDot=False):
	'''
	create a 3D plot with prototypes and criticisms
	:param utt3D:
	:param xyz3D:
	:param prototypes:
	:param criticisms:
	:param show:
	:param filePlotExport:
	:param dotSize:
	:param protoSize:
	:param dotLineWidth:
	:param protoLineWidth:
	:param soundsdir:
	:param oneDotPerSpeaker:
	:param detailSpeakerClick:
	:param autoScaleDot:
	:return:
	'''
	global plot
	global colorsOrdered
	global xyzOrdered
	global uttOrdered
	global lPrototypes
	global lCriticisms
	global xyz
	global utt
	xyz = xyz3D
	utt = utt3D
	setSound(soundsdir)
	setOptions(dotS, dotLineW, protoS, protoLineW)
	fig = plt.figure()
	colorsOrdered, xyzOrdered, uttOrdered = chooseColor(xyz3D, utt3D)
	colorsProto, colorsCrit = chooseColorProto(uttOrdered, xyzOrdered, colorsOrdered, prototypes, criticisms)
	lPrototypes = prototypes
	lCriticisms = criticisms
	x = []
	y = []
	z = []
	for i in xyzOrdered:
		x.append([])
		y.append([])
		z.append([])
		for j in i:
			x[- 1].append(j[0])
			y[- 1].append(j[1])
			z[- 1].append(j[1])

	xc = []
	yc = []
	zc = []
	xp = []
	yp = []
	zp = []
	np= []
	# for i in range(len(uttOrdered)):
	# 	for j in range(len(prototypes)):
	# 		if prototypes[j][0] in uttOrdered[i]:
	# 			a=uttOrdered[i].index(prototypes[j][0])
	# 			xp.append(xyzOrdered[i][a][0])  # add the utt
	# 			yp.append(xyzOrdered[i][a][1])
	# 			zp.append(xyzOrdered[i][a][2])
	# 			np.append([prototypes[j][0],xp[-1],yp[-1],zp[-1]])
	for i in criticisms:
		# c = xyzOrdered[i[0]][i[1]]
		xc.append(i[1])  # add the utt
		yc.append(i[2])
		zc.append(i[3])
	autoScale = []
	if autoScaleDot:
		autoScale = autoScaleFunction(np, lCriticisms, protoSize)

	for i in prototypes:
		# p = xyzOrdered[i[0]][i[1]]
		xp.append(i[1])  # add the utt
		yp.append(i[2])
		zp.append(i[3])
	ax = fig.add_subplot(projection='3d')
	### place the points
	for i in range(0, len(xyzOrdered)):
		ax.scatter(x[i], y[i], z[i], s=dotSize, color=colorsOrdered[i], edgecolors='black', linewidth=dotLineWidth)
	###
	for i in range(0, len(criticisms)):
		ax.scatter(xc[i], yc[i], zc[i], s=protoSize, color=colorsCrit[i], marker="^", edgecolors='black',
				   linewidth=protoLineWidth)
	for i in range(len(xp)):
		# print(xp[i],"  ",xc[i])
		# print(i)
		if autoScaleDot:
			ax.scatter(xp[i], yp[i],zp[i], color=colorsProto[i], s=autoScale[i], marker="D", edgecolors='black',
					   linewidth=protoLineWidth)
		else:
			ax.scatter(xp[i], yp[i],zp[i], color=colorsProto[i], s=protoSize, marker="D", edgecolors='black',
					   linewidth=protoLineWidth)
	# bind press event with onclick function
	cid = fig.canvas.mpl_connect('button_press_event', lambda event: onclick3D(event, ax, xyz, utt,oneDotPerSpeaker,detailSpeakerClick))
	# plot labelling
	ax.set_xlabel("X")
	ax.set_ylabel("Y")
	ax.set_zlabel("Z")
	# plt.legend(loc='upper left')
	plt.title("PLOT")
	f=filePlotExport.split("/")
	if len(f)>1:
		f.pop()
	f="".join(f)
	if run.checkPath(f):
		plt.savefig(filePlotExport, dpi=1920)
		print("Plot save to", filePlotExport)
	if (show == True):
		plt.show()


def create3DPlot(utt3D, xyz3D, show=False, filePlotExport="plot.jpeg", dotS=20, dotLineW=1, soundsdir="",
				 detailSpeakerClick=True, title="Plot"):
	'''
	create a 3D plot
	:param utt:
	:param xyz:
	:param show:
	:param filePlotExport:
	:param dotSize:
	:param soundsdir:
	:param detailSpeakerClick:
	:return:
	'''
	setSound(soundsdir)
	setOptions(dotS, dotLineW)
	fig = plt.figure()
	colorsOrdered, xyzOrdered, uttOrdered = chooseColor(xyz3D, utt3D)
	x = []
	y = []
	z = []
	for i in xyzOrdered:
		x.append([])
		y.append([])
		z.append([])
		for j in i:
			x[len(x) - 1].append(j[0])
			y[len(y) - 1].append(j[1])
			z[len(z) - 1].append(j[1])
	ax = fig.add_subplot(projection='3d')
	### place the points
	for i in range(0, len(xyzOrdered)):
		ax.scatter(x[i], y[i], z[i],s=dotSize, color=colorsOrdered[i], edgecolors='black', linewidth=dotLineWidth)
	# bind press event with onclick function
	cid = fig.canvas.mpl_connect('button_press_event', lambda event: onclick3D(event, ax, xyz, utt,detailSpeakerClick))
	# plot labelling
	ax.set_xlabel("X")
	ax.set_ylabel("Y")
	ax.set_zlabel("Z")
	# plt.legend(loc='upper left')
	plt.title("PLOT")
	f=filePlotExport.split("/")
	if len(f)>1:
		f.pop()
	f="".join(f)
	if run.checkPath(f):
		plt.savefig(filePlotExport, dpi=1920)
		print("Plot save to", filePlotExport)
	if (show == True):
		plt.show()







