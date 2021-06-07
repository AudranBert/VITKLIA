#!/bin/bash

# Parameters

pathToExport='Out/'
pathToOrigin=''

newspk='spk2utt'
newfeat='feats.scp'
newutt='utt2spk'

feats='featsOrigin.scp'
spk2utt='spk2uttOrigin'
utt2spk='utt2spkOrigin'

speakerNumber=50
ct=0

createATestDataSet=True
speakerTestNumber=$((speakerNumber/10))
testExtension='Test'



# Code 

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