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

from matplotlib import pyplot as plt
from sklearn.mixture import GaussianMixture

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

def findClose(list,point):
    if len(list)>0:
        pt=list[0]
        for i in range(len(list)):
            if math.dist(list[i],point)<math.dist(pt,point):
                pt=list[i]
        return pt
    return None

def gmmSpk(list):
    list=list[:]
    gm = GaussianMixture(n_components=50, random_state=0).fit(list)
    l=gm.predict(list)
    print(l[:])
    return l

def gmm(utt,vectors):
    gm = GaussianMixture(n_components=50, random_state=0).fit(vectors)
    l=gm.predict(vectors)
    lmean=[]
    for i in range(50):
        ct=0
        lmean.append(["0",0,0,0])
        for j in range(len(l)):
            if l[j]==i:
                ct+=1
                lmean[i][1]+=vectors[j][0]
                lmean[i][2] += vectors[j][1]
        lmean[i][1] = lmean[i][1]/ct
        lmean[i][2] = lmean[i][2]/ct
        lmean[i][3] = ct
        p=findClose(vectors,lmean[i][1:3])
        lmean[i][0]=utt[vectors.index(p)]
    for i in range(len(lmean)):
        print(i," : ",lmean[i])
    return l,lmean

if __name__ == "__main__":
    '''
    main
    '''
    utt,vectors=fileManager.readUtt("../resources/files/utt.txt")
    v2=vectors[:]
    #utt,vectors=run.classify(utt, vectors)
    l,lmean=gmm(utt,vectors)
    utt,vectors=run.classify(utt,v2)
    #for i in range(len(utt)):
     #   print(utt[i]," :",l[i] ," : ",vectors[i])

    # fig, ax = plt.subplots()
    # x = []
    # y = []
    # for i in lmean:
    #     x.append(i[0])
    #     y.append(i[1])
    # ax.scatter(x, y)
    # plt.show()
    plotCreator.create2DPlotPrototypes(utt, vectors,lmean,[],True)