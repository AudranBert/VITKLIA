import os
import os.path
import re
import sys

testExtension = ""
oldfeat = ""
oldutt = ""
oldspk = ""


def testDataset(newspk, newFeat, newutt, feat, spk):
    if (os.path.isfile(newspk) and os.path.isfile(feat)):  # check if files exist
        print(feat)
        print(newFeat)
        print(newutt)
        print("FILES FOUND")
        print(newspk)
        rm = open(spk, "r")
        rmFromSpk = []
        for i in rm:
            s = i.strip("\n")
            s = s.split()
            ct = 0
            rmFromSpk.append(s[0])
        rm.close()
        out = open(newspk, "r")

        lines = out.readlines()
        idSpeaker = []
        linesSpk = []
        for i in lines:  # for each speaker
            s = i.strip("\n")
            s = s.split()
            # print(s[0])
            if s[0] not in rmFromSpk:
                idSpeaker.append(s[0])
                linesSpk.append(i)
        out.close()
        spk = open(newspk, "w")
        for i in linesSpk:  # for each speaker
            spk.write(i)
        spk.close()
        feats = open(newFeat, "r")
        # result = open(newFeat, "w")
        data = []

        ct = 0
        for line in feats:  # for each lines of feats
            s = line.strip("\n")
            s = s.split()
            found = False
            for i in idSpeaker:
                r = re.match(i + "-", s[0])
                if (r):  # speaker found
                    data.append([s[0], s[1], i])
                    print(s[0])
                # result.write(s[0] + " " + s[1] + "\n")
                # newspkFile.write(s[0] + " " + i + "\n")
            ct += 1
            if (ct % 10000 == 0):
                print("Lines ", ct, " verified...")
        # for i in idSpeaker:
        #    result.write(i+"\n")
        feats.close
        result = open(newFeat, "w")
        newspkFile = open(newutt, "w")
        for i in data:
            result.write(i[0] + " " + i[1] + "\n")
            newspkFile.write(i[0] + " " + i[2] + "\n")
        feats.close()
        result.close()
        newspkFile.close()
    else:
        print("NO FILE")


def trainDataset(newspk, newFeat, newutt, feat, test="False"):
    if (os.path.isfile(newspk) and os.path.isfile(feat)):  # check if files exist
        print("FILES FOUND")
        out = open(newspk, "r")

        lines = out.readlines()
        idSpeaker = []
        for i in lines:  # for each speaker
            s = i.strip("\n")
            s = s.split()
            # print(s[0])
            idSpeaker.append(s[0])
        out.close()
        feats = open(feat, "r")
        result = open(newFeat, "w")
        newspkFile = open(newutt, "w")
        ct = 0
        for line in feats:  # for each lines of feats
            s = line.strip("\n")
            s = s.split()
            for i in idSpeaker:
                r = re.match(i + "-", s[0])
                if (r):  # speaker found
                    # print(s[0])
                    result.write(s[0] + " " + s[1] + "\n")
                    newspkFile.write(s[0] + " " + i + "\n")
                    # break
            ct += 1
            if (ct % 10000 == 0):
                print("Lines ", ct, " verified...")
        # for i in idSpeaker:
        #    result.write(i+"\n")
        feats.close()
        result.close()
        newspkFile.close()
        if test == "True":
            testDataset(oldspk, oldfeat, oldutt, newFeat, newspk)
        print("Finished :", newFeat)
    else:
        print("NO FILE")


if __name__ == "__main__":
    # args
    newspk = "out.txt"
    newFeat = "newFeats.scp"
    newutt = "utt"

    # global testExtension
    # global oldspk
    # global oldutt
    # global oldfeat
    feat = "feats.scp"
    utt2spk = "utt2spk"
    ct = 0
    numerotaion = True

    test = False

    ## args
    # do not give a same file name twice
    if (len(sys.argv) >= 2):
        test = sys.argv[1]
        if test == "True":
            if (len(sys.argv) >= 3):
                newspk = sys.argv[2]  # new spk2utt file

            if (len(sys.argv) >= 4):
                newFeat = sys.argv[3]  # new feats.scp file
            if (len(sys.argv) >= 5):
                newutt = sys.argv[4]  # new utt2spk file
                oldutt = newutt
            if (len(sys.argv) >= 6):
                feat = sys.argv[5]  # feat file
                oldfeat = feat
            if (len(sys.argv) >= 7):
                utt2spk = sys.argv[6]  # utt2spk

            if (len(sys.argv) >= 8):
                ct = int(sys.argv[7])  # file numbering
            if (len(sys.argv) >= 9):
                testExtension = (sys.argv[8])
                t = newspk.split(testExtension)
                oldspk = t[0]

        else:
            if (len(sys.argv) >= 3):
                newspk = sys.argv[2]  # new spk2utt file
            if (len(sys.argv) >= 4):
                newFeat = sys.argv[3]  # new feats.scp file
            if (len(sys.argv) >= 5):
                newutt = sys.argv[4]  # new utt2spk file
            if (len(sys.argv) >= 6):
                feat = sys.argv[5]  # feat file
            if (len(sys.argv) >= 7):
                utt2spk = sys.argv[6]  # utt2spk
            if (len(sys.argv) >= 8):
                ct = int(sys.argv[7])  # file numbering
    # if (len(sys.argv) >= 8):
    #    numerotaion = sys.argv[7]
    ## numerotation
    # if (numerotaion):
    #     ct=1
    #     n=newFeat.split(".")
    #     if(os.path.isfile(newFeat)):
    #         while(os.path.isfile(n[0]+str(ct)+"."+n[1])):
    #             ct+=1
    #         newFeat=n[0]+str(ct)+"."+n[1]

    if (ct != 0):  # file numbering
        if test == "True":
            n = newFeat.split(".")
            if len(n) == 2:
                newFeat = n[0] + testExtension + str(ct) + "." + n[1]
            else:
                newFeat = n[0] + testExtension + str(ct)
            n = newutt.split(".")
            if len(n) == 2:
                newutt = n[0] + testExtension + str(ct) + "." + n[1]
            else:
                newutt = n[0] + testExtension + str(ct)
        else:
            n = newFeat.split(".")
            if len(n) == 2:
                newFeat = n[0] + str(ct) + "." + n[1]
            else:
                newFeat = n[0] + str(ct)
            n = newutt.split(".")
            if len(n) == 2:
                newutt = n[0] + str(ct) + "." + n[1]
            else:
                newutt = n[0] + str(ct)
    else:
        if test == "True":
            n = newFeat.split(".")
            if len(n) == 2:
                newFeat = n[0] + testExtension + "." + n[1]
            else:
                newFeat = n[0] + testExtension
            n = newutt.split(".")
            if len(n) == 2:
                newutt = n[0] + testExtension + "." + n[1]
            else:
                newutt = n[0] + testExtension
    print("feat: ", feat)
    print(newspk)
    print(newFeat)
    print(newutt)
    print("---")
    print(oldfeat)
    print(oldspk)
    print(oldutt)
    print("---")
    ## main code
    trainDataset(newspk, newFeat, newutt, feat, test)
