# README

## How to use it

You can use the tool simply by launching:

    python reductionVectors configFile [mode]

For example this line:
    
    python reductionVectors config.txt reduction
will launch with the mode reduction and the configuration file : config.txt.

## Configuration
 
An example is provided : config.txt.
Here are the list of parameters that can be found on the configuration file.
You can make empty lines or make comment lines with # at the beginning of the line.

  * mode can be "reduction" or "read". Reduction will read xvectors in the given file. Read will read reducted vectors in the given file.
  * xvectorsFile is the name of the file that contains xvectors
  * dimension is the number of dimension after reduction, it can be 2 or 3.
  * exportReductionFile is the file where the result will be store
  * readingFile is the file where we read the reducted vectors
  * plotFile is the name of the file where the plot will be exported
  * showPlot defines if the plot is shown or not
  * dotSize defines the size of the dot in the plot.