CETRPlotter
===========
## Intro

This repo contains a short Python program that draws charts from the output of a CETR UMT tribometer. 

The CETR is an obscure friction testing instrument, used at Sentient Science, Columbia University, and probably some other places.

## Notes on filetypes

The CETR's output is a proprietary ```.tst``` binary file, which must be converted to a ```.csv``` via the CETR's proprietary "Textify TST" utility. This program will not work on ```.tst``` files; instead, you must textify those ```.tst``` files into ```.csv```'s. 

## Inputs and outputs

This program accepts as input the path to a directory, which ought to contain zero or more ```.csv``` files that are formatted in the standard CETR format. The ```.csv``` files can be nested arbitrarily deep in directories, and this program will happily find and plot them. The charts will be saved in the same folder that the ```.csv``` file is in, and the chart's title+filename will be the same as the name of the ```.csv``` file. 

## How to run
On Unix, run this code as follows:
```
$ python cetr_plotter.py 
```
You need some dependencies, including numpy, matplotlib, and some sort of graphical windowing setup such as Tkinter. This is because the program has a GUI for selecting directories that contain the ```.csv``` files you are interested in plotting. 

On Windows, you can probably run this from your IDE or via the Windows command line or Powershell.