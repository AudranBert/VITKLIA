
import os.path
import sys
import prototypes
import xvectorsParser
import umap
import plotCreator
import fileReader
import run
import pickle
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

def ldaMethod(utt,vectors,mode,dimension,load=False,saveModel="",loadModel=""):
    embedding=[]
    if "UMAP" not in mode:
        print("LDA with reduction")
        y = []
        newutt = prototypes.classify(utt, vectors)
        for i in range(len(vectors)):
            index = -1
            for j in range(len(newutt)):
                if vectors[i] in newutt[j]:
                    index = j
                    break
            y.append(index)
        if load and loadModel!="":
            loaded_model = pickle.load((open(loadModel, 'rb')))
            print("LDA model:",loadModel, "has been loaded")
            embedding = loaded_model.fit_transform(vectors,y)
        else:
            lda=LinearDiscriminantAnalysis(
                n_components=dimension
            )
            embedding=lda.fit_transform(vectors,y)
            if saveModel != "":
                pickle.dump(lda, open(saveModel, 'wb'))
                print("LDA model:", saveModel, " has been saved")
    else:
        print("LDA without reduction")
        y = []
        newutt = prototypes.classify(utt, vectors)
        for i in range(len(vectors)):
            index = -1
            for j in range(len(newutt)):
                if vectors[i] in newutt[j]:
                    index = j
                    break
            y.append(index)
        if load and loadModel!="":
            loaded_model = pickle.load((open(loadModel, 'rb')))
            print("LDA model:",loadModel, "has been loaded")
            embedding = loaded_model.fit_transform(vectors,y)
        else:
            lda=LinearDiscriminantAnalysis(
            )
            embedding = lda.fit_transform(vectors, y)
            if saveModel != "":
                pickle.dump(lda, open(saveModel, 'wb'))
                print("LDA model:", saveModel, " has been saved")
    return embedding

def umapMethod(vectors,dimension,n_neighbor,min_dist,load,saveModel,loadModel):
    embedding=[]
    print("UMAP reduction")
    if load and loadModel!="":
        loaded_model = pickle.load((open(loadModel, 'rb')))
        print("UMAP model:",loadModel, "has been loaded")
        embedding=loaded_model.fit_transform(vectors)
    else:
        reducer = umap.UMAP(
            n_components=dimension,
            n_neighbors=n_neighbor,
            min_dist=min_dist,
        )
        embedding = reducer.fit_transform(vectors)  # transform into 2D
        if saveModel!="":
            pickle.dump(reducer, open(saveModel, 'wb'))
            print("UMAP model:",saveModel," has been saved")
    return embedding


def printAll(utt,vectors):
    '''
    print all vectors of a list
    :param utt:
    :param vectors:
    :return:
    '''
    for i in range(0,len(utt)):
        print()
        print(utt[i]+" : ",end="")
        print(vectors[i])
        print()

def reduce(utt,vectors,reductionMethod,fileToExport,dimension,n_neighbor=15,min_dist=0.1,loadUmap=False,saveUmapModel="",loadUmapModel="",loadLda=False,saveLdaModel="",loadLdaModel="",option="",number=0):
    '''
    transform vectors into 2D or 3D vectors
    :param filePath:
    :param fileToExport:
    :return utt:
    :return embedding:
    '''
    print("Reduction of embeddings...")


    if option!="":
        lpos = xvectorsParser.getExtent(vectors,option,number)
        vectors=xvectorsParser.removeVariables(vectors,lpos)
    else:
        print("no option")
    #printAll(utt,vectors)
    #reducer=umap.UMAP()
    #scaled_vectors = umap.StandardScaler().fit_transform(vectors)
    #embedding = reducer.fit_transform(scaled_vectors)
    print(fileToExport)
    if dimension==2 or dimension==3:
        embedding = []
        method = reductionMethod
        if "LDA" in method:
            embedding=ldaMethod(utt,vectors,reductionMethod,dimension,loadLda,saveLdaModel,loadLdaModel)
            vectors=embedding
        if "UMAP" in method:
            embedding=umapMethod(vectors,dimension,n_neighbor,min_dist,loadUmap,saveUmapModel,loadUmapModel)
        #printAll(utt,embedding)
        fileReader.exportData(utt, embedding, fileToExport)      # save 2D vectors
        return utt,embedding
    else:
        run.errorExit("dimension must be 2 or 3")











