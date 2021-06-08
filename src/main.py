
import plotCreator
import xvectorsParser
import fileReader
import prototypes
import reductionVectors
import sys
import os

# global variables
mode="read"
# reduction
xvectorsFile=""
dimension= "2"
exportReductionFile=""
#reading
readingFile=""
# plot
showPlot = True
filePlotExport = "plot.jpeg"
dotSize = 20
# others
utt = []
vectors = []

def load(file):
    '''
    read vectors
    :param file:
    :return utt:
    :return vectors:
    '''
    utt,vectors=fileReader.readAFile(file)  # read vectors


    return utt,vectors

def errorExit(msg,code=-1):
    '''
    error
    :param msg:
    :param code:
    :return:
    '''
    print(msg)
    exit(code)

def readConf(fileName):
    '''
    read the configuration file
    :param fileName:
    :return:
    '''
    global mode
    global dimension
    global xvectorsFile
    global exportReductionFile
    global readingFile
    global filePlotExport
    global showPlot
    global dotSize
    if not os.path.isfile(fileName):        # check if conf file exist
        errorExit("Conf file :", fileName," does not exist")
    else:
        with open( fileName) as file:
            for line in file:       # read all lines
                l=line.split("=")
                l[0]=l[0].strip()
                #if (l[0].startswith("#")):
                    #print("start # : ",l[0])
                #elif ( l[0]==""):
                    #print("empty line")
                if(not(l[0].startswith("#")) and not(l[0]=="")):
                    l[1] = l[1].strip()
                    l[1] = l[1].strip("\n")
                    #print(l)
                    if (l[0]=="mode"):
                        mode=l[1]
                    elif (l[0]=="dimension"):
                        dimension=l[1]
                    elif (l[0]=="xvectorsFile"):
                        xvectorsFile=l[1]
                    elif (l[0]=="exportReductionFile"):
                        exportReductionFile=l[1]
                    elif (l[0]=="readingFile"):
                        readingFile=l[1]
                    elif (l[0]=="plotFile"):
                        filePlotExport=l[1]
                    elif (l[0]=="showPlot"):
                        showPlot=bool(l[1])
                    elif (l[0]=="dotSize"):
                        dotSize=int(l[1])
    #print("SETTINGS :")
    #print(mode)
    #print(dimension)


if __name__ == "__main__":

    if (len(sys.argv) >= 2):    # if conf file is given
        readConf(sys.argv[1])
        if (len(sys.argv) >= 3):    # if mode is given
            mode=sys.argv[2]
    else:
        errorExit("Missing conf file")
    if mode=="reduction":   # mode  reduction
        utt,vectors=reductionVectors.reduce(xvectorsFile,exportReductionFile,dimension)
        utt,vectors=load(exportReductionFile)
    elif mode=="read":      # reading mode
        utt,vectors=load(readingFile)
    else:
        errorExit("Mode invalid")
    #print(len(vectors[0]))
    #prototypes.classify(vectors,utt)
    lprototypes,lcriticisms=prototypes.prototypesEachSpeaker(vectors,utt)
    #
    #
    if (len(vectors[0])==3):    # if 3D vectors
        plotCreator.create3DPlot(vectors,utt,showPlot,filePlotExport,dotSize)
    else:       # 2D vectors
        plotCreator.create2DPlotPrototypes(vectors,lprototypes,lcriticisms, utt, showPlot, filePlotExport, dotSize)
        #plotCreator.create2DPlot(vectors,utt,showPlot,filePlotExport,dotSize)
    #print(vectors.shape)




