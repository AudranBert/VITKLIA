# Configs


Each parameter is explained by comments. 

## Compare.yaml

Allow to compare two reducted dataset. Here are the list of most important parameters that can be found on the configuration file:

* protoFileSet0, critFileSet0, uttFileSet0 for setting files for the first set.

* protoFileSet1, critFileSet1, uttFileSet1 for the second set. 

## Config.yaml

Config.yaml is a configuration file for the python script "run.py". So it contains configuration for the calculation of prototypes, the reduction, the plotting.

Here are the list of most important parameters that can be found on the configuration file:

* ressources_dir is the path to all the files of the tool.
* export_dir is the directory where files will be saved (except for the plot).
* mode can be "reduction" or "read". Reduction will read xvectors in the given file. Read will read reducted vectors in the given file.
* xvectorsFile is the name of the file that contains vectors.
* uttFile is the file where the reducted vectors will be store.
* protoFile is the file where the prototypes will be store.
* critFile is the file where the criticisms will be store.
* dimension is the number of dimension after reduction, it can be 2 or 3.
* findProto if false just plot embeddings and if true find prototypes and criticisms and plot it.
* plotFile is the name of the file where the plot will be exported
* oneDotPerSpeaker allows to plot only the prototypes
* detailSpeakerClick allow when you click on an utterance to make a new plot with only the speaker of the clicked utterance
