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

# number of speakers in the train dataset
speakerTrainNumber=50
# folder for the new train dataset (no "/" at the end)
trainExtension='Train'

# number of test dataset
testDatasetNumber=5
# number of speakers in the test
speakerTestNumber=50
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


if [ -f "$newspk" ];
then
	ct=1
	while [ -f "$newspk$ct" ] ; do
		ct=$(($ct+1))
	done
fi

echo "File names:"
echo $feats
echo $spk2utt
echo $utt2spk
echo "Speaker selection..."

if [ $ct -ne 0 ];
then
newspk=$newspk$ct
fi

if [ ! -d $pathToExport$trainExtension ] 
then
	mkdir $pathToExport$trainExtension
fi

speakerNumber=$(((speakerTestNumber*testDatasetNumber)+(speakerTrainNumber)))
cat $spk2utt | shuf | head -n $speakerNumber > tmpSpk


echo "Get utterances :"
cat tmpSpk | head -n $speakerTrainNumber > $newspkTrain
tail -n +$((speakerTrainNumber+1)) tmpSpk > tmp
cp -f tmp tmpSpk
python3 speakersSelector.py False $newspkTrain $newfeatTrain $newuttTrain $feats $utt2spk $ct



i=1
testExtension="${pathToExport}${testExtension}"
while [ $i -le $testDatasetNumber ]
do
        testspk="${testExtension}${i}/${newspk}"
        if [ ! -d ${testExtension}${i} ] 
	then
		mkdir ${testExtension}${i}
	fi
	ext="${testExtension}${i}/"
        i=$((i+1))
	cat tmpSpk | head -n $speakerTestNumber > $testspk
	tail -n +$((speakerTestNumber+1)) tmpSpk > tmp
	cp -f tmp tmpSpk
	echo "Get Test utterances :"
	
	python3 speakersSelector.py True $testspk $newfeat $newutt $feats $utt2spk $ct $ext
done

rm tmp
rm tmpSpk




