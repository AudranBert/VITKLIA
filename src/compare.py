import math

import plotCreator
import xvectorsParser
import fileManager
import prototypes
import reductionVectors
import os
import argparse
import yaml
import run
from multiprocessing import Process

resources=""
plotFile0=""
plotFile1=""
utt1 = ""
proto1 = ""
crit1 = ""
utt2 = ""
proto2 = ""
crit2 = ""
sounds=""

def readConf(fileName):
    '''
    read the configuration file and return file names
    :param fileName:
    :return:
    '''
    global resources
    global utt1
    global proto1
    global crit1
    global utt2
    global proto2
    global crit2
    global plotFile0
    global plotFile1
    global sounds

    if not os.path.isfile(fileName):  # check if conf file exist
        run.errorExit("Conf file : " + fileName + " does not exist")
    yaml_file = open(fileName, 'r')
    yaml_content = yaml.load(yaml_file, Loader=yaml.FullLoader)

    resources=yaml_content.get("resources_dir")
    set_dir = yaml_content.get("file_dir")
    set_dir= resources+os.path.sep+set_dir+os.path.sep
    utt1=set_dir+yaml_content.get("uttFileSet0")
    proto1=set_dir+yaml_content.get("protoFileSet0")
    crit1 = set_dir + yaml_content.get("critFileSet0")
    utt2=set_dir+yaml_content.get("uttFileSet1")
    proto2=set_dir+yaml_content.get("protoFileSet1")
    crit2 = set_dir + yaml_content.get("critFileSet1")
    plotFile0=resources + os.path.sep +yaml_content.get("plotFile0")
    plotFile1=resources + os.path.sep +yaml_content.get("plotFile1")
    sounds = yaml_content.get("sounds_dir")
    return yaml_content

def compare(data1,data2,title="Titre",showPrint=False):
    sum = 0
    pos = []
    dist = []
    for i in range(len(data1)):
        posi = 0
        disti = 10000
        pi = data1[i][1:]
        for j in range(len(data2)):
            pj = data2[j][1:]
            distj = math.dist(pi, pj)
            if disti > distj:
                posi = j
                disti = distj
        pos.append(posi)
        dist.append(disti)
    if (showPrint):
        print("-----------------------------")
        print(title)
    for i in range(len(dist)):
        if (showPrint):
            print(round(dist[i], 3), " between ", data1[i][0], " and ", data2[pos[i]][0])
        sum += disti
    mean=sum / len(dist)
    if (showPrint):
        print("mean dist:", round(mean, 3))
        print("-----------------------------")
    return mean,title

def calcul(proto,crit,showPrint=False,mode=[["p-0","p-1"],["c-0","p-0"],["c-1","p-1"],["c-0","p-1"],["c-1","p-0"]],):
    title=[]
    mean=[]
    for i in mode:
        data=[]
        t = "Difference between"
        for j in range(len(i)):
            m=i[j].split("-")
            m[1]=int(m[1])
            if m[0]=="p":
                data.append(proto[m[1]])
                t+=" prototypes "+str(m[1])
            elif m[0]=="c":
                data.append(crit[m[1]])
                t+=" criticisms "+str(m[1])
            else:
                print("unknown")
        a=compare(data[0],data[1],t,showPrint)
        mean.append(a[0])
        title.append(a[1])
    for i in range(len(title)):
        print("mean of ",title[i]," is ",round(mean[i],3))

if __name__ == "__main__":
    '''
    main
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("--conf", default="", help="name of the config file")
    args = parser.parse_args()
    yaml_content = readConf(args.conf)
    if yaml_content.get("readingProto"):
        utt, vectors, lprototypes, lcriticisms = fileManager.readFiles(utt1, proto1, crit1)
        classifiedUtt, classifiedVectors = run.classify(utt, vectors)
        plotName="Plot "+yaml_content.get("protoFileSet0")
        p=plotCreator.create2DPlotPrototypes(classifiedUtt, classifiedVectors, lprototypes, lcriticisms, False, plotFile0,yaml_content.get("dotSize"),yaml_content.get("protoSize"), yaml_content.get("dotLineWidth"), yaml_content.get("protoLineWidth"), sounds,yaml_content.get("oneDotPerSpeaker"),yaml_content.get("detailSpeakerClick"),yaml_content.get("scalePrototypes"),plotName)
        utt2, vectors2, lprototypes2, lcriticisms2 = fileManager.readFiles(utt2, proto2, crit2)
        classifiedUtt2, classifiedVectors2 = run.classify(utt2, vectors2)
        plotName="Plot "+yaml_content.get("protoFileSet1")
        p2=plotCreator.create2DPlotPrototypes(classifiedUtt2, classifiedVectors2, lprototypes2, lcriticisms2, False, plotFile1,yaml_content.get("dotSize"),yaml_content.get("protoSize"), yaml_content.get("dotLineWidth"), yaml_content.get("protoLineWidth"), sounds,yaml_content.get("oneDotPerSpeaker"),yaml_content.get("detailSpeakerClick"),yaml_content.get("scalePrototypes"),plotName)

        lproto=[lprototypes,lprototypes2]
        lcrit=[lcriticisms,lcriticisms2]

        calcul(lproto,lcrit,yaml_content.get("showPrint"))

        if yaml_content.get("showPlot"):
            p.show()
        #p2.show()