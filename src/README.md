# README

## How to use it

You can use the tool simply by launching:

    python run.py --conf configFile [--mode mode]

For example this line:
    
    python run.py --conf ../resources/config.txt --mode reduction
will launch with the mode reduction and the configuration file : config.txt.

## Configuration
 
An example is provided : config.txt.
Config file is in YAML.
Here are the list of parameters that can be found on the configuration file.
You can make empty lines or make comment lines with # at the beginning of the line.

  * ressources_dir is the path all the files in the config file.
  * mode can be "reduction" or "read". Reduction will read xvectors in the given file. Read will read reducted vectors in the given file.
  * xvectorsFile is the name of the file that contains xvectors
  * variableSelectionOption (default="") is the mode of selecting variables "" means all varaibles, best means variables with the biggest extent, worst means variables with the lowest extent
  * exportReductionFile is the file where the result will be store
  * dimension is the number of dimension after reduction, it can be 2 or 3.
  * n_neighbor (default=15) is a parameter for UMAP, define the number of neighbor taken for reduction.
  * min_dist (default=0.1) is a parameter for UMAP, the min dist to take the neighbor
  * readingFile is the file where we read the reducted vectors
  * plotFile is the name of the file where the plot will be exported
  * showPlot defines if the plot is shown or not
  * dotSize defines the size of the dot in the plot.
  * findProto if false just plot embeddings and if true finc prototypes and criticisms and plot it.
  * grdiSearch if true calculate the grid search between prototypes and criticisms