#!/bin/bash

# Parameters

pathToExport='Out/'
pathToOrigin=''

newspk='spk2utt'
newfeat='feats'
newutt='utt2spk'

feats='featsOrigin.scp'
spk2utt='spk2uttOrigin'
utt2spk='utt2spkOrigin'

utteranceNumber=50
ct=0

trainExtension='Train'

utteranceTestNumber=$(( utteranceNumber / 5 ))
testExtension='Test'

utteranceDevNumber=$(( utteranceNumber / 10 ))
devExtension='Dev'



# Code 

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