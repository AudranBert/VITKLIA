# Configs

## Compare.yaml

1speaker.txt : file with reducted vectors in 2 dimensions of 1 speaker
2speaker.txt : file with reducted vectors in 2 dimensions of 2 speakers
emb2D.txt : file with reducted vectors in 2 dimensions of 50 speakers
emb2DTEST.txt : file with reducted vectors in 2 dimensions of 50 speakers with the 20 variables with the biggest extend
emb3D.txt : file with reducted vectors in 3 dimensions of 50 speakers
xvectors.txt : file with embeddings inside

## Config.yaml

plot/ : default folder for saving plots
dataset/ : folder with original feats.scp, spk2utt and utt2spk

Config.yaml is a configuration file for the python script "run.py". So it contains configuration for the calculation of prototypes, the reduction, the plotting.

Each parameter is explained by comments. 