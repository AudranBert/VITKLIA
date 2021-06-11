#!/bin/bash

# Parameters

# path where the new dataset will be
pathToExport='Out/'

# path where the dataset is
pathToOrigin=''

# name of the new spk2utt file
newspk='spk2utt'
# name of the new feats.scp file
newfeat='feats'
# name of the new utt2spk file
newutt='utt2spk'

# name of the feats file where we take utterances
feats='featsOrigin.scp'
# name of the spk2utt file where we take speakers
spk2utt='spk2uttOrigin'
# name of the utt2spk file
utt2spk='utt2spkOrigin'

# numer of total utterances 
utteranceNumber=50

# train files will have "newspk+trainExtension" for example
trainExtension='Train'

# number of utterances in the test
utteranceTestNumber=$(( utteranceNumber / 5 ))
# test files will have "newspk+testExtension" for example
testExtension='Test'

# number of utterances in the dev
utteranceDevNumber=$(( utteranceNumber / 10 ))
# dev files will have "newspk+devExtension" for example
devExtension='Dev'

# the train has utteraneNumber-Test-Dev utterances

# Code 
ct=0
newfeat=$pathToExport$newfeat
newspk=$pathToExport$newspk
newutt=$pathToExport$newutt

feats=$pathToOrigin$feats
spk2utt=$pathToOrigin$spk2utt
utt2spk=$pathToOrigin$utt2spk

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



cat $feats | shuf | head -n $utteranceNumber > $newfeat$trainExtension

cat $newfeat$trainExtension | head -n $utteranceDevNumber > $newfeat$devExtension
tail -n +$((utteranceDevNumber+1)) $newfeat$trainExtension > tmp
cat tmp | head -n $utteranceTestNumber > $newfeat$testExtension
tail -n +$((utteranceTestNumber+1)) tmp > $newfeat$trainExtension
rm tmp

python3 uttSelector.py $newspk$trainExtension $newutt$trainExtension $newfeat$trainExtension
python3 uttSelector.py $newspk$testExtension $newutt$testExtension $newfeat$testExtension
python3 uttSelector.py $newspk$devExtension $newutt$devExtension $newfeat$devExtension