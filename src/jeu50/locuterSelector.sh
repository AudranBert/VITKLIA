#!/bin/bash
newspk='spk2utt'
newfeat='feats.scp'
newutt='utt2spk'
feats='featsOrigin.scp'
spk2utt='spk2uttOrigin'
utt2spk='utt2spkOrigin'
speakerNumber=50
ct=0

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
python3 featSelector.py $newspk $newfeat $newutt $feats $utt2spk $ct