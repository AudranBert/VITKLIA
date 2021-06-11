
import plotCreator
import xvectorsParser
import fileReader
import prototypes
import reductionVectors
import sys
import os
import argparse
import yaml

# global variables
resources=""
sounds=""
mode="read"
# reduction
xvectorsFile=""
#dimension= "2"
exportReductionFile=""
#reading
readingFile=""
# plot
#showPlot = True
filePlotExport = "plot.jpeg"
#dotSize = 20
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
    global resources
    global sounds
    global mode
    global dimension
    global xvectorsFile
    global exportReductionFile
    global readingFile
    global filePlotExport
    global showPlot
    global dotSize
    if not os.path.isfile(fileName):        # check if conf file exist
        errorExit("Conf file : "+fileName+" does not exist")
    yaml_file = open(fileName, 'r')
    yaml_content = yaml.load(yaml_file, Loader=yaml.FullLoader)
    if args.mode!="":
        mode=args.mode
    elif yaml_content.get("mode")!="" and yaml_content.get("mode")!=None:
        mode=yaml_content.get("mode")
    else:
        print("no mode defined")
    xvectorsFile=yaml_content.get("xvectorsFile")
    exportReductionFile=yaml_content.get("exportReductionFile")
    readingFile=yaml_content.get("readingFile")
    filePlotExport=yaml_content.get("plotFile")
    sounds=yaml_content.get("sounds_dir")
    resources=yaml_content.get("resources_dir")
    xvectorsFile=resources+os.path.sep+xvectorsFile
    exportReductionFile=resources+os.path.sep+exportReductionFile
    readingFile=resources+os.path.sep+readingFile
    filePlotExport=resources+os.path.sep+filePlotExport
    return yaml_content


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--conf",default="",help="name of the config file")
    parser.add_argument("--mode", default="", help="mode")
    args=parser.parse_args()
    #readConf(args.conf)
    yaml_content=readConf(args.conf)
    # for key, value in yaml_content.items():
    #     print(f"{key}: {value}")
    mode=mode.strip("\n")
    mode=mode.strip()
    if (mode=="reduction"):   # mode  reduction
        if not os.path.isfile(xvectorsFile):  # check if conf file exist
            errorExit("File : " + xvectorsFile + " does not exist")
        utt,vectors=reductionVectors.reduce(xvectorsFile,exportReductionFile,int(yaml_content.get("dimension")),yaml_content.get("n_neighbor"),yaml_content.get("min_dist"),yaml_content.get("variableSelectionOption"),yaml_content.get("variablesSelectionNumber"))
        utt,vectors=load(exportReductionFile)
    elif (mode=="read"):      # reading mode
        if not os.path.isfile(readingFile):  # check if conf file exist
            errorExit("File : " + readingFile + " does not exist")
        utt,vectors=load(readingFile)
    else:
        errorExit("Mode invalid")
    # #print(len(vectors[0]))
    # #prototypes.classify(vectors,utt)
    if yaml_content.get("findProto"):
        lprototypes,lcriticisms=prototypes.prototypesEachSpeaker(vectors,utt,yaml_content.get("gridSearch"))
        if (len(vectors[0])==3):    # if 3D vectors
            plotCreator.create3DPlotPrototypes(vectors,lprototypes,lcriticisms,utt,yaml_content.get("showPlot"),filePlotExport,yaml_content.get("dotSize"))
        else:       # 2D vectors
            plotCreator.create2DPlotPrototypes(vectors,lprototypes,lcriticisms, utt, yaml_content.get("showPlot"), filePlotExport, yaml_content.get("dotSize"),sounds)
            #plotCreator.create2DPlot(vectors,utt,showPlot,filePlotExport,dotSize)
    else:
        if (len(vectors[0])==3):    # if 3D vectors
            plotCreator.create3DPlot(vectors,utt,yaml_content.get("showPlot"),filePlotExport,yaml_content.get("dotSize"))
        else:       # 2D vectors
            plotCreator.create2DPlot(vectors, utt, yaml_content.get("showPlot"), filePlotExport, yaml_content.get("dotSize"),sounds)
    #print(vectors.shape)



