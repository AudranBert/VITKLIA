# Tool to make a smaller DATASET 

The goal is to create a smaller dataset with voxeceleb's speakers.

## Two possibilities

You can use a number of speakers or a number of utterances. Each one is a different script.

## SpeakerSelector

If you want to select X speakers for your dataset use this script.

### How to use it

Simply launch :

    bash speakersSelector.sh


### Configuration

if you want to change parameters, open speakersSelector.sh.


  * You can also set the path to the origin files and the path to the exported files (default : blank, so it searchs in the current folder)
  * You can change the name of origin files and new files (there are default values for each)
  * You can change the number of speakers in the train by changing "speakerTrainNumber" (default value : 50) 
  * You can set the folder where you want your train dataset
  * You can change the number of test dataset by changing "testDatasetNumber"
  * You can change the number of speakers for test dataset by changing "speakerTestNumber"
  * You can set the folder where you want your test dataset

## UtteranceSelector

If you want to select X utterances for your dataset use this script

### How to use it

Simply launch :

    bash utterancesSelector.sh


### Configuration

if you want to change parameters, open utterancesSelector.sh.

There are the same as the speakerSelector.

## DatasetInfo

This script gives you informations about a dataset: numbers of speakers, number of utterances, number mean of utterances per speaker...

### How to use it

Launch:

    python datasetInfo.py fileName

FileName is the path of the feats.scp file of your dataset.
