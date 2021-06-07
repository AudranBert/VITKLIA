# Tool to make a smaller DATASET 

The goal is to create a smaller dataset with voxeceleb's speakers.

## Two possibilities

You can use a number of speaker or a number of utterance. Each one is a different script.

## SpeakerSelector

If you want to select X speakers for your dataset use this script.

### How to use it

Simply launch :

    bash speakersSelector.sh


### Configuration

if you want to change parameters, open speakersSelector.sh.

  * You can change the number of speakers by changing "speakerNumber" (default value : 50) 
  * You can change the name of origin files and new files (there are default values for each)
  * You can also set the path to the orgin files and the path to the exported files (default : blank, so it searchs in the current folder)
  * You can ask for the creation of a test dataset by changing createATestDataSet to True
  * If the previus conf is at True you can select the number of speakers for the test dataset
  * You can also select the extension of the files

## UtteranceSelector

If you want to select X utterances for your dataset use this script

### How to use it

Simply launch :

    bash utterancesSelector.sh


It will create feat file for dev train and test.
Same for the spk2utt file and the utt2spk file.
Si it will create 9 files.

### Configuration

if you want to change parameters, open utterancesSelector.sh.

  * You can change the number of speakers by changing "utteranceNumber" (default value : 50) 
  * You can change the name of origin files and new files (there are default values for each)
  * You can also set the path to the orgin files and the path to the exported files (default : blank, so it searchs in the current folder)
  * You can change the number of utterances for dev or test
  * You can change the extension for each subdataset (for train, test and test dataset)