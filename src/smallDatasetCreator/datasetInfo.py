import os
import os.path
import re
import sys



def getInfos(fileName):
    '''
    give infos about a dataset
    :param fileName: the path of the feats.scp file
    :return:
    '''
    nbSpeaker=0
    nbUtt=0
    nbUttMinPerSpeaker=-1
    nbUttMaxPerSpeaker= -1
    nbUttMeanPerSpeaker=0
    min=-1
    max=-1
    speakerList=[]
    speakerUttNb=[]

    with open(fileName) as file:  # Use file to refer to the file object
        for line in file:
            line.strip("\n")
            line = line.split()
            idS=line[0].split("-")
            nbUtt+=1
            if idS[0] not in speakerList:
                speakerList.append(idS[0])
                speakerUttNb.append(1)
                nbSpeaker+=1
            else:
                pos=speakerList.index(idS[0])
                speakerUttNb[pos]+=1

    for i in range(0,len(speakerUttNb)):
        if min==-1 or speakerUttNb[min]>speakerUttNb[i]:
            min=i
        if max==-1 or speakerUttNb[max]<speakerUttNb[i]:
            max=i
    nbUttMeanPerSpeaker=nbUtt/nbSpeaker
    nbUttMinPerSpeaker=speakerUttNb[min]
    nbUttMaxPerSpeaker=speakerUttNb[max]
    print("DATASET Infos : ",fileName )
    print(nbSpeaker)
    print(nbUtt)
    print(nbUttMinPerSpeaker)
    print(nbUttMaxPerSpeaker)
    print(nbUttMeanPerSpeaker)
    return nbSpeaker,nbUtt,nbUttMinPerSpeaker,nbUttMaxPerSpeaker,nbUttMeanPerSpeaker

if __name__ == "__main__":
    '''
    main
    '''
    feat="feats.scp"
    ## args
    # do not give a same file name twice
    if (len(sys.argv)>=2):
        feat=sys.argv[1]      # new spk2utt file

    ## main code
    if(os.path.isfile(feat)):    # check if files exist
        getInfos(feat)
    else:
        print("NO FILE")






