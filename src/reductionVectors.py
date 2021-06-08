
import os.path
#filePath="/stklia/cfg/example_exp_speaker/xvectors/train_data/xvectors.txt"
import sys
import prototypes
#filePath="\\xvectors.txt"
import xvectorsParser
import umap
import plotCreator
import fileReader
import main





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

def reduce(filePath,fileToExport,dimension):
    '''
    transform vectors into 2D or 3D vectors
    :param filePath:
    :param fileToExport:
    :return utt:
    :return embedding:
    '''
    utt,vectors=xvectorsParser.readVectors(filePath)        # read xvectors
    #lpos = xvectorsParser.getExtent(vectors)
    #vectors=xvectorsParser.removeVariables(vectors,lpos)
    #printAll(utt,vectors)
    #reducer=umap.UMAP()
    #scaled_vectors = umap.StandardScaler().fit_transform(vectors)
    #embedding = reducer.fit_transform(scaled_vectors)
    print(fileToExport)
    if (dimension=="2"):
        embedding=umap.UMAP().fit_transform(vectors)            # transform into 2D
        #printAll(utt,embedding)
        fileReader.exportData(utt, embedding, fileToExport)      # save 2D vectors
        return utt,embedding
    elif(dimension=="3"):
        fit = umap.UMAP(
            n_components=3,
        )
        embedding=fit.fit_transform(vectors)            # transform into 2D
        #printAll(utt,embedding)
        fileReader.exportData(utt, embedding, fileToExport)      # save 2D vectors
        return utt,embedding
    else:
        main.errorExit("mode must be read or reduction")











