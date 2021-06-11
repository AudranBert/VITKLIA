#!/bin/bash

# Parameters

# path where the new dataset will be
pathToExport='Out/'

# path where the dataset is
pathToOrigin=''

# name of the new spk2utt file
newspk='spk2utt'
# name of the new feats.scp file
newfeat='feats.scp'
# name of the new utt2spk file
newutt='utt2spk'

# name of the feats file where we take utterances
feats='featsOrigin.scp'
# name of the spk2utt file where we take speakers
spk2utt='spk2uttOrigin'
# name of the utt2spk file
utt2spk='utt2spkOrigin'

# number of speakers in the new dataset
speakerNumber=50

# create a test dataset
createATestDataSet=True
# if true how many speakers
speakerTestNumber=$((speakerNumber/10))
# test files will have "newspk+testExtension" for example
testExtension='Test'



# Code 
ct=0

newfeat=$pathToExport$newfeat
newspk=$pathToExport$newspk
newutt=$pathToExport$newutt

feats=$pathToOrigin$feats
spk2utt=$pathToOrigin$spk2utt
utt2spk=$pathToOrigin$utt2spk


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



cat $spk2utt | shuf | head -n $speakerNumber > $newspk


echo "Get utterances :"
python3 featSelector.py False $newspk $newfeat $newutt $feats $utt2spk $ct

if [ "$createATestDataSet" ];
then
	testspk=${newspk}${testExtension}
	cat $newspk | shuf | head -n $speakerTestNumber > $testspk
	echo "Get Test utterances :"
	python3 speakersSelector.py True $testspk $newfeat $newutt $newfeat $utt2spk $ct $testExtension
fi	