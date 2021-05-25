
import plotCreator
import fileReader


if __name__ == "__main__":
	data=fileReader.reading("../ressources/randomData2D.txt")
	print(data)
	if len(data[0]) == 3:
		plotCreator.create3DPlot(data)
	else:
		plotCreator.create2DPlot(data)






