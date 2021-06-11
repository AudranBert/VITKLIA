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

def getListMin(list, number,debug=False):
    lmin = []
    lpos=[]
    sumMin=0
    for i in range(0,number):
        min=0
        pos=0
        for j in range(0,len(list)):
            if min>list[j] and list[j] not in lmax:
                min=list[j]
                pos=j
        lpos.append(pos)
        lmin.append(min)
        sumMin += min
        if debug:
            print(min)
    return lmin,lpos,sumMin

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

def getInfos(extend,vectors,plot=False,debug=False):
    sumExtend=0
    for i in range(0,len(extend)):
        sumExtend+=extend[i]
    print("--------")
    print("Statistiques globales")
    print("Vecteurs du fichier:",path)
    print("nombre de vecteurs:",len(vectors))
    print("nombre de variables:",len(extend))
    print("moyenne des etendues totale:", sumExtend/len(extend))
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
    prepBarPlotLoss(extend,sumExtend,"Curve of sum extent")
    prepBarPlot(extend,"Bar plot of the extend of the variables")

def getExtent(vectors,option,qtt,debug=False):
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
    #qtt = len(extend) // 10
    if option=="best":
        lmax,lpos,sumMax=getListMax(extend,qtt)
    elif option=="worst":
        lmin, lpos, sumMin = getListMin(extend, qtt)
    if debug:
        getInfos(extend,vectors,True)
    return lpos

def prepBarPlot(list,title,total=False):
    minVal=min(list)
    maxVal=max(list)
    extendPlot=maxVal-minVal
    nbStep=10
    step=extendPlot/nbStep
    bar=[]
    value=[]
    for i in range(0,nbStep):
        bar.append(">"+str(round(i*step,1)))
        value.append(0)
    if total:
        bar.append("Total")
        value.append(0)
    for i in range(0,len(list)) :
        for t in reversed(range(0,nbStep)) :
            if (list[i]>step*t):
                value[t]+=1
                if total:
                    value[nbStep]+=1
                break

    plot(bar,value,title)

def prepBarPlotLoss(list,total,title="Plot"):
    value=[]
    value.append(total)
    list.sort(reverse=True)
    ct=1
    for i in range(0,len(list)):
        value.append(value[ct-1]-list[i])
        ct+=1

    plt.plot(value)
    plt.ylabel("sum of extent")
    plt.xlabel("number of removed variables")
    plt.title(title)
    plt.savefig("plot/"+title+".jpeg")
    print("plot saved:", "plot/" + title + ".jpeg")
    plt.show()

    #plot(bar,value,title,"sum of extents","number of variables remove")

def plot(bar,value,title="plot",ylabel="Number of variables",xlabel="Value of the extend"):
    #fig = plt.figure()
    #ax = fig.add_axes([0, 1])

    plt.bar(bar, value)
    plt.xticks( bar)
    #plt.yticks( [0,max(value)//2,max(value)] )
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.savefig("plot/"+title+".jpeg")
    print("plot saved:", "plot/"+title+".jpeg")
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
    '''
    scritp that allows to have acces to infos about variables
    '''
    if (len(sys.argv) >= 2):
        path=(sys.argv[1])
    utt,vectors=readVectors(path)
    variables=getExtent(vectors,True)
