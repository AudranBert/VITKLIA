#!/bin/bash

# Parameters

# path where the dataset is
pathToOrigin='../../resources/dataset/'

# name of the feats file where we take utterances
feats='featsOrigin.scp'
# name of the spk2utt file where we take speakers
spk2utt='spk2uttOrigin'
# name of the utt2spk file
utt2spk='utt2spkOrigin'

# Export

# path where the new dataset will be
pathToExport='../../resources/dataset/Out/'

# name of the new spk2utt file
newspk='spk2utt'
# name of the new feats.scp file
newfeat='feats.scp'
# name of the new utt2spk file
newutt='utt2spk'

# number of utterances in the train dataset
utteranceTrainNumber=5000
# folder for the new train dataset (no "/" at the end)
trainExtension='Train'

# number of test dataset
testDatasetNumber=5
# number of utterances in the test
utteranceTestNumber=5000
# folder for the new test dataset (no "/" at the end)
testExtension='Test'


# End parameters

# Code 
ct=0
newfeatTrain="${pathToExport}${trainExtension}/${newfeat}"
newspkTrain="${pathToExport}${trainExtension}/${newspk}"
newuttTrain="${pathToExport}${trainExtension}/${newutt}"

feats=$pathToOrigin$feats
spk2utt=$pathToOrigin$spk2utt
utt2spk=$pathToOrigin$utt2spk

if [ ! -d $pathToExport ] 
then
	mkdir $pathToExport
fi

if [ -f "$newfeat" ];
then
	ct=1
	while [ -f "$newfeat$ct" ] ; do
		ct=$(($ct+1))
	done
fi

echo "File names:"
echo $feats
echo $spk2utt
echo $utt2spk
echo "Utterances selection..."

if [ $ct -ne 0 ];
then
newfeat=$newfeat$ct
fi

if [ ! -d $pathToExport$trainExtension ] 
then
	mkdir $pathToExport$trainExtension
fi

utteranceNumber=$(((utteranceTestNumber*testDatasetNumber)+(utteranceTrainNumber)))
cat $feats | shuf | head -n $utteranceNumber > tmpFeat

cat tmpFeat | head -n $utteranceTrainNumber > $newfeatTrain
tail -n +$((utteranceTrainNumber+1)) tmpFeat > tmp
cp -f tmp tmpFeat
python3 uttSelector.py $newspkTrain $newuttTrain $newfeatTrain


i=1
testExtension="${pathToExport}${testExtension}"
while [ $i -le $testDatasetNumber ]
do
        testFeat="${testExtension}${i}/${newfeat}"
        testSpk="${testExtension}${i}/${newspk}"
        testUtt="${testExtension}${i}/${newutt}"
        if [ ! -d ${testExtension}${i} ] 
	then
		mkdir ${testExtension}${i}
	fi
        i=$((i+1))
	cat tmpFeat | head -n $utteranceTestNumber > $testFeat
	tail -n +$((utteranceTestNumber+1)) tmpFeat > tmp
	cp -f tmp tmpFeat
	echo "Get Test utterances :"
	python3 uttSelector.py $testSpk $testUtt $testFeat
done

rm tmp
rm tmpFeat





