import os
import os.path
import re
import sys



if __name__ == "__main__":
    '''
    main
    create a utt2spk and spk2utt depending of a feats.scp file
    '''

    # args
    newspkfile = "out.txt"
    newuttfile = "utt"

    # global testExtension
    # global oldspk
    # global oldutt
    # global oldfeat
    featfile = "feats.scp"

    ## args
    # do not give a same file name twice
    if (len(sys.argv) >= 2):
        newspkfile=sys.argv[1]
    if (len(sys.argv) >= 3):
        newuttfile = sys.argv[2]  # new spk2utt file
    if (len(sys.argv) >= 4):
        featfile = sys.argv[3]  # new feats.scp file


    print("feat: ", featfile)
    print(newspkfile)
    print(newuttfile)
    listSpeaker=[]
    listUtt=[]

    if os.path.isfile(featfile):  # check if files exist
        feat = open(featfile, "r")
        newutt=open(newuttfile, "w")
        for lines in feat:
            s=lines.strip("\n")
            s=s.split(" ")
            spk=s[0].split("-")
            newutt.write(s[0]+" "+spk[0]+"\n")
            if spk not in listSpeaker:
                listSpeaker.append(spk[0])
                listUtt.append([])
                listUtt[len(listUtt)-1].append(s[0])
            else:
                listUtt[listSpeaker.index(spk)].append(s[0])
        newutt.close()
        feat.close()
        newspk=open(newspkfile,"w")
        for i in range(0,len(listSpeaker)):
            s=listSpeaker[i]+" "
            for j in range(0,len(listUtt[i])):
                s+=listUtt[i][j]+" "
            s+="\n"
            newspk.write(s)
        newspk.close()
    ## main code
