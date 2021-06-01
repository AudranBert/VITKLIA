import os.path

path = "/stklia/cfg/example_exp_speaker/xvectors/train_data/xvectors.txt"


def readVectors(filePath):
    '''
    read xvectors of a given file (out of STKLIA)
    :param filePath:
    :return:
    '''
    with open(os.getcwd()+os.path.sep + filePath) as file:  # Use file to refer to the file object
        vectors = []
        utt=[]
        ct=0
        for line in file:
            line = line.split()
            invect = False
            l = []
            for i in line:
                if (invect == False) and (i != "[" and i != "]"):
                    utt.append(i)       # get uttId
                elif (i!="[" and i!="]"):
                    l.append(i)     # get and create the vector
                if (i == "[" or i == "]"  ):
                    invect=True
            vectors.append(l)       # append the vector
            ct+=1
    return utt,vectors


if __name__ == "__main__":
    readVectors(path)
