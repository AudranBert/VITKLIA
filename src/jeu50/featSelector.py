import os
import os.path
import re
import sys

if __name__ == "__main__":
    #args
    newspk= "out.txt"
    newFeat="newFeats.scp"
    newutt="utt"


    feat="feats.scp"
    utt2spk="utt2spk"
    ct=0
    numerotaion=True

    ## args
    if (len(sys.argv)>=2):
        newspk=sys.argv[1]
    if (len(sys.argv)>=3):
        newFeat=sys.argv[2]
    if (len(sys.argv)>=4):
        newutt=sys.argv[3]
    if (len(sys.argv)>=5):
        feat=sys.argv[4]
    if (len(sys.argv)>=6):
        utt2spk=sys.argv[5]
    if (len(sys.argv) >= 7):
        ct = int(sys.argv[6])
    #if (len(sys.argv) >= 8):
    #    numerotaion = sys.argv[7]
    ## numerotation
    # if (numerotaion):
    #     ct=1
    #     n=newFeat.split(".")
    #     if(os.path.isfile(newFeat)):
    #         while(os.path.isfile(n[0]+str(ct)+"."+n[1])):
    #             ct+=1
    #         newFeat=n[0]+str(ct)+"."+n[1]

    if (ct!=0):
        n = newFeat.split(".")
        if len(n)==2:
            newFeat = n[0] + str(ct) +"."+ n[1]
        else:
            newFeat = n[0] + str(ct)
        n = newutt.split(".")
        if len(n)==2:
            newutt = n[0] + str(ct)+"." + n[1]
        else:
            newutt = n[0] + str(ct)

    print(newspk)
    print(newFeat)
    print(newutt)
    ## main code
    if(os.path.isfile(newspk) and os.path.isfile(feat)):
        print("FILES FOUND")
        out = open(newspk, "r")

        lines = out.readlines()
        idSpeaker = []
        for i in lines:
            s = i.strip("\n")
            s = s.split()
            #print(s[0])
            idSpeaker.append(s[0])
        out.close()
        feats = open(feat, "r")
        result = open(newFeat, "w")
        newspkFile=open(newutt,"w")
        ct=0
        for line in feats:
            s = line.strip("\n")
            s = s.split()
            for i in idSpeaker:
                r=re.match(i+"-", s[0])
                if(r):
                    #print(s[0])
                    result.write(s[0]+" "+s[1]+"\n")
                    newspkFile.write(s[0]+" "+i+"\n")
            ct+=1
            if (ct%10000==0):
                print("Lines ",ct," verified...")
        #for i in idSpeaker:
        #    result.write(i+"\n")
        feats.close()
        result.close()
        newspkFile.close()
        print("Finished :",newFeat)
    else:
        print("NO FILE")






