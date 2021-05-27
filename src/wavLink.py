
import os.path

from playsound import playsound


def getFile(pathToWav,id):
    txt=id.split("-")
    path=pathToWav
    for i in range (len(txt)):
        path+=txt[i]
        if (i<len(txt)-1):
            path+=os.path.sep
        else :
            path+=".wav"
    print(path)
    if(os.path.isfile(path)):
        playsound(path)
        return path

    else:
        return None


def getFileWithPathToData(id):
    cwd = os.getcwd()
    pathToStklia="path"
    pathToData=cwd+os.path.sep+"data"+os.path.sep+"wav"+os.path.sep+"voxceleb1"+os.path.sep
    print(cwd)
    path=getFile(pathToData,id)
    print(path)

if __name__ == "__main__":
    getFileWithPathToData("id10270-5r0dWxy17C8-00001")




