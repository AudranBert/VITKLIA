import os.path
import sys
import matplotlib.pyplot as plt

path = "xvectors.txt"


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
                    l.append(float(i))     # get and create the vector
                if (i == "[" or i == "]"  ):
                    invect=True
            vectors.append(l)       # append the vector
            ct+=1
    return utt,vectors


def getListMax(list, number,debug=False):
    lmax = []
    lpos=[]
    sumMax=0
    for i in range(0,number):
        max=0
        pos=0
        for j in range(0,len(list)):
            if max<list[j] and list[j] not in lmax:
                max=list[j]
                pos=j
        lpos.append(pos)
        lmax.append(max)
        sumMax += max
        if debug:
            print(max)
    return lmax,lpos,sumMax

def getSup(list,value,debug=False):
    meansup1=0
    m=0
    ctInf=0
    for i in list:
        if i>value:
            if debug:
                print(i)
            meansup1+=i
            m+=1
        if i<value:
            ctInf+=1
    meansup1=meansup1/m

    print("nombre de variables dont etendue inf a ",value, ": " ,ctInf)
    ctSup=len(list)-ctInf
    print("nombre de variables dont etendue sup a ", value, ": ", ctSup)
    print("moyenne des variables avec etendue sup a ",value,": ",meansup1)

def getInfos(extend):
    sumExtend=0
    for i in range(0,len(extend)):
        sumExtend+=extend[i]
    print("--------")
    print("Statistiques globales")
    print("Vecteurs du fichier:",path)
    print("nombre de variables:",len(extend))
    print("moyenne totale:", sumExtend/len(extend))
    print("somme des etendues",sumExtend)
    print("--------")
    print("Statistiques des plus grandes etendues")
    qtt=len(extend)//10
    print("les",qtt,"plus grandes etendues:")
    lmax,lpos,sumMax=getListMax(extend,qtt)
    print(lmax)
    print("les positions:")
    print(lpos)
    print("% de l'etendue total conservée :",(sumMax/sumExtend)*100)
    print("qtt de variable et somme etendue:",len(lmax),";",sumMax,"vs total :",len(extend),";",sumExtend)
    print("moyenne:",sumMax/len(lmax))
    print("--------")
    print("Statistiques Ciblées")
    getSup(extend,8)
    print("--------")
    #prepBarPlot(extend,"Extend")

def getExtent(vectors):
    min=[]
    max=[]
    for i in range(0,len(vectors)):
        for j in range(0,len(vectors[i])):
            if j >= len(min):
                min.append(vectors[i][j])
                max.append(vectors[i][j])
            else:
                if min[j]>vectors[i][j]:
                    min[j]=vectors[i][j]
                elif max[j]<vectors[i][j]:
                    max[j]=vectors[i][j]
    extend=[]
    for i in range(0,len(min)):
        extend.append(max[i]-min[i])
    qtt = len(extend) // 10
    lmax,lpos,sumMax=getListMax(extend,qtt)
    getInfos(extend)
    return lpos

def prepBarPlot(list,title):
    min=min(list)
    max=max(list)
    extendPlot=max-min
    nbStep=10
    step=extendPlot//nbStep
    bar=[]
    value=[]
    for i in range(0,nbStep):
        bar.append(i*step)
        value.append(0)
    for i in range(0,len(list)) :
        print("blop")
    plot(bar,value,title)

def plot(bar,value,title="plot"):
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    langs = ['C', 'C++', 'Java', 'Python', 'PHP']
    ax.bar(bar, value)
    plt.title(title)
    plt.show()

def removeVariables(vectors,lpos):
    newVectors=[]
    for i in range(0,len(vectors)):
        newVectors.append([])
        for j in range(0,len(vectors[i])):
            if j in lpos:
                newVectors[i].append(vectors[i][j])
    #print(newVectors)
    #getExtent(newVectors)
    return newVectors

if __name__ == "__main__":
    if (len(sys.argv) >= 2):
        path=(sys.argv[1])
    utt,vectors=readVectors(path)
    variables=getExtent(vectors)
