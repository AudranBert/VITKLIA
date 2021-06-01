
import os.path

from playsound import playsound

voxceleb="voxceleb1"

def getFile(pathToWav,id):
    '''
    :param pathToWav:
    :param id:
    :return path if the file exist:
    '''
    txt=id.split("-")                       # split uttId on "-"
    path=pathToWav                          # path to Voxceleb folder
    locId=txt[0]                            # get the speaker id
    uttId=txt[-1]                           # get the wav number
    p="-".join(txt[1:len(txt)-1])           # get the subfolder
    # for i in range (len(txt)):
    #     path+=txt[i]
    #     if (i<len(txt)-1):
    #         path+=os.path.sep
    #     else :
    #         path+=".wav"
    path=path+locId+os.path.sep+p+os.path.sep+uttId+".wav"      # make the path
    print(path)
    if(os.path.isfile(path)):           # if the file exist
        playsound(path)
        return path

    else:
        return None     # file not found


def getFileWithPathToData(id):
    '''
    :param id:
    :return path:
    '''
    cwd = os.getcwd()       # get current path
    #pathToStklia="path"
    pathToData=cwd+os.path.sep+"data"+os.path.sep+"wav"+os.path.sep+voxceleb+os.path.sep     #path to Voxceleb1
    #print(cwd)
    path=getFile(pathToData,id)     # path of the wav
    return path

if __name__ == "__main__":
    getFileWithPathToData("id10270-5r0dWxy17C8-00001")




