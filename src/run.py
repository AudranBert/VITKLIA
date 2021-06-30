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


def errorExit(msg, code=-1):
    '''
    error
    :param msg:
    :param code:
    :return:
    '''
    print(msg)
    exit(code)


def autoName(plotFile, dimension, reductionMethod, intra, inter):
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


def readConf(fileName):
    '''
    read the configuration file
    :param fileName:
    :return:
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
    exportReductionFile = yaml_content.get("exportReductionFile")
    readingFile = yaml_content.get("readingFile")
    filePlotExport = yaml_content.get("plotFile")
    sounds = yaml_content.get("sounds_dir")
    resources = yaml_content.get("resources_dir")
    exportDir = yaml_content.get("export_dir")
    if not (os.path.isdir(resources + os.path.sep + exportDir)):
        os.mkdir(resources + os.path.sep + exportDir)
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
    exportReductionFile = resources + os.path.sep + exportReductionFile
    #readingFile = resources + os.path.sep + readingFile
    filePlotExport = resources + os.path.sep + filePlotExport
    f = filePlotExport.split("/")
    f.pop()
    d = ""
    for i in f:
        d += i + "/"
    if not (os.path.isdir(d)):
        os.mkdir(d)
    return yaml_content


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--conf", default="", help="name of the config file")
    parser.add_argument("--mode", default="", help="mode")
    args = parser.parse_args()
    # readConf(args.conf)
    yaml_content = readConf(args.conf)
    # for key, value in yaml_content.items():
    #     print(f"{key}: {value}")
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
        if (yaml_content.get("findProto") and not (yaml_content.get("afterReduction"))):
            if "LDA" in mode and "UMAP" in mode:
                vectors = reductionVectors.ldaMethod(utt, vectors, mode, yaml_content.get("dimension"))
                i = mode.index("LDA")
                del mode[i]
            if yaml_content.get("eachSpeaker"):
                lprototypes, lcriticisms, gridSearchIntra, gridSearchInter = prototypes.prototypesEachSpeaker(utt,
                                                                                                              vectors,
                                                                                                              yaml_content.get(
                                                                                                                  "gridSearch"),
                                                                                                              yaml_content.get(
                                                                                                                  "kernel"))
            else:
                classifiedVectors, lprototypes, lcriticisms, gridSearchIntra, gridSearchInter = prototypes.prototypes(
                    utt, vectors, yaml_content.get("nbProto"), yaml_content.get("gridSearch"),
                    yaml_content.get("kernel"))

            # if "LDA" in mode and "UMAP" not in mode:
            #     vectors = reductionVectors.ldaMethod(utt, vectors, mode, yaml_content.get("dimension"))
            #     i = mode.index("LDA")
            #     del mode[i]
        utt, vectors = reductionVectors.reduce(utt, vectors, mode, exportReductionFile,
                                               int(yaml_content.get("dimension")), yaml_content.get("n_neighbor"),
                                               yaml_content.get("min_dist"), yaml_content.get("loadUmapModel"),
                                               saveUmapModelFile, loadUmapModelFile, yaml_content.get("loadLdaModel"),
                                               saveLdaModelFile, loadLdaModelFile,
                                               yaml_content.get("variableSelectionOption"),
                                               yaml_content.get("variablesSelectionNumber"))
        utt, vectors = load(exportReductionFile)
    elif (mode == "read"):  # reading mode
        # if not os.path.isfile(readingFile):  # check if conf file exist
        #     errorExit("File : " + readingFile + " does not exist")
        # utt,vectors=load(readingFile)
        if (yaml_content.get("readingProto")):
            print("reading files...")
            utt, vectors, lprototypes, lcriticisms = fileManager.readFiles(saveUttFile, saveProtoFile, saveCritFile)
            # for i in range(len(vectors)):
            #     print(utt[i],end='')
            #     print(vectors[i])
            # for i in range(len(classifiedVectors)):
            #     print(len(classifiedVectors[i]))
            #     for j in range(len(classifiedVectors[i])):
            #         print(classifiedUtt[i][j], end='')
            #         print(classifiedVectors[i][j])
            # print(len(vectors))
        else:
            utt, vectors = fileManager.readUtt(saveUttFile)
        classifiedUtt, classifiedVectors = classify(utt, vectors)
    else:
        errorExit("Mode invalid")
    # #print(len(vectors[0]))
    # #prototypes.classify(vectors,utt)
    dimension = 2

    if len(vectors) > 0 and len(vectors[0]) == 3:
        dimension = 3
    if (yaml_content.get("findProto") and mode!="read") or (yaml_content.get("readingProto") and mode == "read"):
        if not (yaml_content.get("readingProto")) or mode != "read":
            if (yaml_content.get("afterReduction")):
                if yaml_content.get("eachSpeaker"):
                    classifiedVectors, classifiedUtt, lprototypes, lcriticisms, gridSearchIntra, gridSearchInter = prototypes.prototypesEachSpeaker(
                        utt, vectors, yaml_content.get("gridSearch"), yaml_content.get("kernel"))
                else:
                    classifiedVectors, classifiedUtt, lprototypes, lcriticisms, gridSearchIntra, gridSearchInter = prototypes.prototypes(
                        utt, vectors, yaml_content.get("nbProto"), yaml_content.get("gridSearch"),
                        yaml_content.get("kernel"))
            if (yaml_content.get("saveFiles")):
                if saveProtoFile != "" and saveCritFile != "" and saveUttFile != "":
                    fileManager.exportFiles(classifiedUtt, classifiedVectors, lprototypes, lcriticisms, saveUttFile,
                                            saveProtoFile, saveCritFile)
                else:
                    print("You want to save files but at least one is not defined")
        if (yaml_content.get("autoNamePlot")):
            filePlotExport = autoName(yaml_content.get("plotFile"), dimension, yaml_content.get("reductionMethod"),
                                      gridSearchIntra, gridSearchInter)
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
            # plotCreator.create2DPlot(vectors,utt,showPlot,filePlotExport,dotSize)
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
    # print(vectors.shape)
