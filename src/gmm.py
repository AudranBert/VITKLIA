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
import random

from matplotlib import pyplot as plt
from sklearn.mixture import GaussianMixture


cp=[0.05,0.1,0.15,0.2,0.25,0.3,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1]
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
    n_clusters=20
    gm = GaussianMixture(n_components=n_clusters, random_state=0).fit(vectors)
    l=gm.predict(vectors)
    lmean=[]
    for i in range(n_clusters):
        ct=0
        lmean.append(["0",0,0,0])
        for j in range(len(l)):
            if l[j]==i:
                ct+=1
                lmean[i][1]+=vectors[j][0]
                lmean[i][2] += vectors[j][1]
        if ct>0:
            lmean[i][1] = lmean[i][1]/ct
            lmean[i][2] = lmean[i][2]/ct
            lmean[i][3] = ct
            p=findClose(vectors,lmean[i][1:3])
            lmean[i][0]=utt[vectors.index(p)]
        else:
            lmean.remove()
    # for i in range(len(lmean)):
    #     print(i," : ",lmean[i])
    return l,lmean

if __name__ == "__main__":
    '''
    main
    '''
    utt,vectors=fileManager.readUtt("../resources/files/utt.txt")
    v2=vectors[:]
    #utt,vectors=run.classify(utt, vectors)
    classifiedUtt, classifiedVectors = run.classify(utt, v2)
    lgmm=[]
    lgmmnb=[]
    lutt=[]
    for i in range(len(classifiedVectors)):
        l,lmean=gmm(classifiedUtt[i],classifiedVectors[i])
        lgmm.append([])
        lutt.append([])
        lgmmnb.append([])
        for j in lmean:
            lgmm[i].append(j[1:3])
            lutt[i].append(j[0])
            lgmmnb[i].append(j[3])
    # for i in range(len(lgmm)):
    #     print("speaker:",classifiedUtt[i][0])
    #     print(lgmm[i][0])
    # for i in range(len(utt)):
    #     print(utt[i]," :",l[i] ," : ",vectors[i])
    lprototypes, lcriticisms, gridSearchIntra, gridSearchInter = prototypes.grouped(lutt, lgmm, 1,False, "euclidienne",20,lgmmnb)
    lp, lc, gridSearchIntra, gridSearchInter = prototypes.grouped(classifiedUtt, classifiedVectors, 1, False, "euclidienne",20)
    fig, ax = plt.subplots()
    x = []
    y = []
    colors=[]
    for i in range(len(lprototypes)):
        colors.append((random.choice(cp),random.choice(cp),random.choice(cp)))
    for i in range(len(lprototypes)):
        # x.append(i[1])
        # y.append(i[2])
        ax.scatter(lprototypes[i][1], lprototypes[i][2],color=colors[i],marker="D",edgecolors='black')
    x = []
    y = []
    for i in range(len(lp)):
        # x.append(i[1])
        # y.append(i[2])
        ax.scatter(lp[i][1], lp[i][2],color=colors[i],marker="^",edgecolors='black')
    plt.show()
    #plotCreator.create2DPlotPrototypes(classifiedUtt, classifiedVectors,lprototypes,lcriticisms,True)