import re

import plotCreator
import xvectorsParser
import fileManager
import prototypes
import reductionVectors
import sys
import os
import argparse
import yaml

# global variables
resources = ""
sounds = ""
mode = "read"
# reduction
xvectorsFile = ""
# dimension= "2"
saveUmapModelFile = ""
loadUmapModelFile = ""
saveLdaModelFile = ""
loadLdaModelFile = ""
exportReductionFile = ""

saveProtoFile = ""
saveCritFile = ""
saveUttFile = ""

# reading
readingFile = ""
# plot
# showPlot = True
filePlotExport = "plot.jpeg"
# dotSize = 20
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
    utt, vectors = fileManager.readAFile(file)  # read vectors

    return utt, vectors

def checkPath(path,make=False):
    '''
    check if a path exist and if make=True create it
    :param path:
    :param make:
    :return:
    '''
    if not(os.path.exists(path)):
        return True
    else:
        if make:
            os.makedirs(path)
            return True
        else:
            print("Path :" + path + " does not exist")
            return False

def errorExit(msg, code=-1):
    '''
    error
    :param msg:
    :param code:
    :return:
    '''
    print(msg)
    exit(code)

def convertProto(utt,vec,l):
    '''
    find the item in l in utt to update the vectors in l
    usefull when the number of dimension of vec has changed
    :param utt:
    :param vec:
    :param l:
    :return:
    '''
    newL=[]
    for i in l:
        for j in range(len(utt)):
            if i[0] in utt[j]:
                a = utt[j].index(i[0])
                #print(vec[j][a])
                newL.append([])
                newL[-1].append(i[0])
                for z in vec[j][a]:
                    newL[-1].append(z)
                break
    return newL


def autoName(plotFile, dimension, reductionMethod, intra, inter):
    '''
    create a name for the plot depending of parameters
    :param plotFile:
    :param dimension:
    :param reductionMethod:
    :param intra:
    :param inter:
    :return: the name of the plot
    '''
    f = plotFile.split("/")
    f.pop()
    path = ""
    for i in f:
        path += i + os.path.sep
    mode = reductionMethod.split(",")
    s = ""
    if "LDA" in mode and "UMAP" not in mode and yaml_content.get("afterReduction"):
        s = "afterLDA"
    elif "LDA" in mode and "UMAP" not in mode and not (yaml_content.get("afterReduction")):
        s = "beforeLDA"
    elif "LDA" not in mode and "UMAP" in mode and not (yaml_content.get("afterReduction")):
        s = "beforeUMAP"
    elif "LDA" not in mode and "UMAP" in mode and (yaml_content.get("afterReduction")):
        s = "afterUMAP"
    elif "LDA" in mode and "UMAP" in mode and not (yaml_content.get("afterReduction")):
        s = "afterLDAbeforeUMAP"
    elif "LDA" in mode and "UMAP" in mode and (yaml_content.get("afterReduction")):
        s = "afterLDAafterUMAP"
    gridSearch = round(intra, 2)
    g2 = round(inter, 2)
    if intra == -1:
        file = resources + os.path.sep + path + str(dimension) + "D" + "_" + yaml_content.get(
            "kernel") + "_" + s + ".jpg"
    else:
        file = resources + os.path.sep + path + str(dimension) + "D" + "_" + yaml_content.get(
            "kernel") + "_" + s + "_" + str(gridSearch) + "_" + str(g2) + ".jpg"
    return file


def classify(utt, vectors):
    '''
    :param utt: list of utterance id
    :param vectors: list of utterance
    :return: list of list, each list is one speaker
    '''
    loc = []
    nutt = []
    newutt = []
    ctutt = 0
    for i in utt:
        idL = i.split("-", 1)
        id = idL[0]
        ct = 0
        find = False
        for j in loc:
            if j == id:
                nutt[ct].append(i)
                newutt[ct].append(vectors[ctutt])
                find = True
                break
            ct += 1
        if find == False:
            loc.append(id)
            newutt.append([])
            nutt.append([])
            nutt[-1].append(i)
            newutt[len(newutt) - 1].append(vectors[ctutt])
        ctutt += 1
    return nutt,newutt

def uttToSpk(id):
    '''
    :param id: an utterance id
    :return: return the id speaker
    '''
    spk=id.split("-")
    return spk[0]


def readConf(fileName):
    '''
    read the configuration file and return the conf object
    construct paths of files
    :param fileName: config file path
    :return: yaml object
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
    global saveUmapModelFile
    global loadUmapModelFile
    global saveLdaModelFile
    global loadLdaModelFile
    global saveProtoFile
    global saveCritFile
    global saveUttFile

    if not os.path.isfile(fileName):  # check if conf file exist
        errorExit("Conf file : " + fileName + " does not exist")
    yaml_file = open(fileName, 'r')
    yaml_content = yaml.load(yaml_file, Loader=yaml.FullLoader)
    if args.mode != "":
        mode = args.mode
    elif yaml_content.get("mode") != "" and yaml_content.get("mode") != None:
        mode = yaml_content.get("mode")
    else:
        print("no mode defined")
    xvectorsFile = yaml_content.get("xvectorsFile")
    #exportReductionFile = yaml_content.get("exportReductionFile")
    readingFile = yaml_content.get("readingFile")
    filePlotExport = yaml_content.get("plotFile")
    sounds = yaml_content.get("sounds_dir")
    resources = yaml_content.get("resources_dir")
    exportDir = yaml_content.get("export_dir")
    if not (os.path.isdir(resources + os.path.sep + exportDir)):
        os.makedirs(resources + os.path.sep + exportDir)
    if yaml_content.get("autoName"):
        n=xvectorsFile.split(".")
        if len(n)>1:
            n.pop()
        n=n[-1].split("/")
        n=n[-1]
        saveUmapModelFile = resources + os.path.sep + exportDir + os.path.sep + n + "UMAP"
        loadUmapModelFile = resources + os.path.sep + exportDir + os.path.sep + n + "UMAP"
        saveLdaModelFile = resources + os.path.sep + exportDir + os.path.sep + n + "LDA"
        loadLdaModelFile = resources + os.path.sep + exportDir + os.path.sep + n + "LDA"
        saveProtoFile = resources + os.path.sep + exportDir + os.path.sep + n + "proto.txt"
        saveCritFile = resources + os.path.sep + exportDir + os.path.sep + n + "crit.txt"
        saveUttFile = resources + os.path.sep + exportDir + "/" + n + "utt.txt"
    else:
        saveUmapModelFile = yaml_content.get("saveUmapModelFile")
        if saveUmapModelFile != "":
            saveUmapModelFile = resources + os.path.sep + exportDir + os.path.sep + yaml_content.get("saveUmapModelFile")
        loadUmapModelFile = yaml_content.get("loadUmapModelFile")
        if loadUmapModelFile != "":
            loadUmapModelFile = resources + os.path.sep + exportDir + os.path.sep + yaml_content.get("loadUmapModelFile")
        saveLdaModelFile = yaml_content.get("saveLdaModelFile")
        if saveLdaModelFile != "":
            saveLdaModelFile = resources + os.path.sep + exportDir + os.path.sep + yaml_content.get("saveLdaModelFile")
        loadLdaModelFile = yaml_content.get("loadLdaModelFile")
        if loadLdaModelFile != "":
            loadLdaModelFile = resources + os.path.sep + exportDir + os.path.sep + yaml_content.get("loadLdaModelFile")
        saveProtoFile = yaml_content.get("protoFile")
        if saveProtoFile != "":
            saveProtoFile = resources + os.path.sep + exportDir + os.path.sep + yaml_content.get("protoFile")
        saveCritFile = yaml_content.get("critFile")
        if saveCritFile != "":
            saveCritFile = resources + os.path.sep + exportDir + os.path.sep + yaml_content.get("critFile")
        saveUttFile = yaml_content.get("uttFile")
        if saveUttFile != "":
            saveUttFile = resources + os.path.sep + exportDir + os.path.sep + yaml_content.get("uttFile")
    xvectorsFile = resources + os.path.sep + xvectorsFile
    #exportReductionFile = resources + os.path.sep + exportReductionFile
    #readingFile = resources + os.path.sep + readingFile
    filePlotExport = resources + os.path.sep + filePlotExport
    f = filePlotExport.split("/")
    f.pop()
    d = ""
    for i in f:
        d += i + "/"
    if not (os.path.isdir(d)):
        os.makedirs(d)
    f=saveUttFile.split("/")
    f.pop()
    d= ""
    for i in f:
        d+= i + "/"
    if not (os.path.isdir(d)):
        os.makedirs(d)
    return yaml_content


if __name__ == "__main__":
    '''
    main
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("--conf", default="", help="name of the config file")
    parser.add_argument("--mode", default="", help="mode")
    args = parser.parse_args()

    yaml_content = readConf(args.conf)

    mode = mode.strip("\n")
    mode = mode.strip()
    lprototypes = []
    lcriticisms = []
    classifiedVectors = None
    classifiedUtt = None
    gridSearchIntra = 0
    gridSearchInter = 0
    if (mode == "reduction"):  # mode  reduction
        if not os.path.isfile(xvectorsFile):  # check if conf file exist
            errorExit("File : " + xvectorsFile + " does not exist")
        utt, vectors = xvectorsParser.readVectors(xvectorsFile)  # read xvectors
        mode = yaml_content.get("reductionMethod").split(",")
        classifiedUtt, classifiedVectors = classify(utt, vectors)
        if (yaml_content.get("findProto") and not (yaml_content.get("afterReduction"))):
            if "LDA" in mode and "UMAP" in mode:
                vectors = reductionVectors.ldaMethod(utt, vectors, mode, yaml_content.get("dimension"))
                i = mode.index("LDA")
                del mode[i]

            if yaml_content.get("eachSpeaker"):
                if yaml_content.get("reducedUtterances"):
                    lprototypes, lcriticisms, gridSearchIntra, gridSearchInter = prototypes.grouped(
                        classifiedUtt, classifiedVectors, yaml_content.get("nbProto"), yaml_content.get("gridSearch"),
                        yaml_content.get("kernel"), yaml_content.get("groupSize"))
                else:
                    lprototypes, lcriticisms, gridSearchIntra, gridSearchInter = prototypes.prototypesEachSpeaker(
                        classifiedUtt, classifiedVectors, yaml_content.get("nbProto"),
                        yaml_content.get("gridSearch"), yaml_content.get("kernel"))
            else:
                lprototypes, lcriticisms, gridSearchIntra, gridSearchInter = prototypes.prototypes(
                    classifiedUtt, classifiedVectors, yaml_content.get("nbProto"), yaml_content.get("gridSearch"),
                    yaml_content.get("kernel"))
        utt, vectors = reductionVectors.reduce(utt, vectors, mode, saveUttFile,
                                               int(yaml_content.get("dimension")), yaml_content.get("n_neighbor"),
                                               yaml_content.get("min_dist"), yaml_content.get("loadUmapModel"),
                                               saveUmapModelFile, loadUmapModelFile, yaml_content.get("loadLdaModel"),
                                               saveLdaModelFile, loadLdaModelFile,
                                               yaml_content.get("variableSelectionOption"),
                                               yaml_content.get("variablesSelectionNumber"))
        utt, vectors = fileManager.readUtt(saveUttFile)
    elif (mode == "read"):  # reading mode
        if (yaml_content.get("readingProto")):
            print("reading files...")
            utt, vectors, lprototypes, lcriticisms = fileManager.readFiles(saveUttFile, saveProtoFile, saveCritFile)
        else:
            utt, vectors = fileManager.readUtt(saveUttFile)
        classifiedUtt, classifiedVectors = classify(utt, vectors)
    else:
        errorExit("Mode invalid")
    dimension = 2

    if len(vectors) > 0 and len(vectors[0]) == 3:
        dimension = 3
    if (yaml_content.get("findProto") and mode!="read") or (yaml_content.get("readingProto") and mode == "read"):
        if not (yaml_content.get("readingProto")) or mode != "read":
            classifiedUtt, classifiedVectors = classify(utt, vectors)
            if (yaml_content.get("afterReduction")):

                if yaml_content.get("eachSpeaker"):
                    if yaml_content.get("groupCalculation"):
                        lprototypes, lcriticisms, gridSearchIntra, gridSearchInter = prototypes.grouped(
                        classifiedUtt, classifiedVectors,yaml_content.get("nbProto"), yaml_content.get("gridSearch"), yaml_content.get("kernel"),yaml_content.get("groupSize"))
                    else:
                        lprototypes, lcriticisms, gridSearchIntra, gridSearchInter = prototypes.prototypesEachSpeaker(
                            classifiedUtt, classifiedVectors, yaml_content.get("nbProto"),
                            yaml_content.get("gridSearch"), yaml_content.get("kernel"))
                else:
                    lprototypes, lcriticisms, gridSearchIntra, gridSearchInter = prototypes.prototypes(
                        classifiedUtt, classifiedVectors, yaml_content.get("nbProto"), yaml_content.get("gridSearch"),
                        yaml_content.get("kernel"))
            else:
                lprototypes=convertProto(classifiedUtt,classifiedVectors,lprototypes)
                lcriticisms=convertProto(classifiedUtt,classifiedVectors,lcriticisms)
            if (yaml_content.get("saveFiles")):
                if saveProtoFile != "" and saveCritFile != "" and saveUttFile != "":
                    fileManager.exportFiles(classifiedUtt, classifiedVectors, lprototypes, lcriticisms, saveUttFile,
                                            saveProtoFile, saveCritFile)
                else:
                    print("You want to save files but at least one is not defined")

        if (yaml_content.get("autoNamePlot")):
            filePlotExport = autoName(yaml_content.get("plotFile"), dimension, yaml_content.get("reductionMethod"),
                                      gridSearchIntra, gridSearchInter)
        prototypes.changePrototypesFormat(lprototypes)
        if (len(vectors) > 0 and dimension == 3):  # if 3D vectors
            plotCreator.create3DPlotPrototypes(classifiedUtt,classifiedVectors, lprototypes, lcriticisms, yaml_content.get("showPlot"),
                                               filePlotExport, yaml_content.get("dotSize"))
        else:  # 2D vectors
            plotCreator.create2DPlotPrototypes(classifiedUtt,classifiedVectors, lprototypes, lcriticisms, yaml_content.get("showPlot"),
                                               filePlotExport, yaml_content.get("dotSize"),
                                               yaml_content.get("protoSize"), yaml_content.get("dotLineWidth"),
                                               yaml_content.get("protoLineWidth"), sounds,
                                               yaml_content.get("oneDotPerSpeaker"),
                                               yaml_content.get("detailSpeakerClick"))
    else:
        classifiedUtt,classifiedVectors = classify(utt, vectors)
        if (yaml_content.get("autoNamePlot")):
            filePlotExport = autoName(yaml_content.get("plotFile"), dimension, yaml_content.get("reductionMethod"), -1,
                                      -1)
        if (len(vectors) > 0 and dimension == 3):  # if 3D vectors
            plotCreator.create3DPlot(classifiedUtt,classifiedVectors, yaml_content.get("showPlot"), filePlotExport,
                                     yaml_content.get("dotSize"))
        else:  # 2D vectors
            plotCreator.create2DPlot(classifiedUtt,classifiedVectors, yaml_content.get("showPlot"), filePlotExport,
                                     yaml_content.get("dotSize"), yaml_content.get("dotLineWidth"), sounds,
                                     yaml_content.get("detailSpeakerClick"))
