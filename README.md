# pySpecV

This is a Sunday, fun project turned into a radar spectra visualizer for pamtra

The visualizer works best on Linux platforms. It has been tested on Windows 10 under Anaconda and works with some visualization problems regarding size and position of frames and labels

DEPENDENCIES:
  - numpy
  - scipy
  - matplolib
  - tkinter
  - netCDF4

To test the software, clone the repository and download a sample data file (7 GB !!!) from the following link https://uni-koeln.sciebo.de/s/X9kjogWlwvGo4Sg 

Simply run 
python3 pySpectraVisualizer.py

It is not recommended to use IDE integrated run consoles. The project is based on tkinter and your IDE tkinter might interfere

The usage of the software is very easy for people familiar with pamtra and radar spectra analysis. For people who do not:
1) Open the sample file with the Open button (bottom left corner)
2) Select a frequency and a variable to be displayed from the relative option menu. Click the "Draw" button
3) A Time-Height plot should appear in the top left panel. You can adjust height, time and value limits using the relative input windows. For time you should use a valid format string according to CF standards like 2015-11-24 06:00
4) Click on the Time-Height plot to activate the other panels, you will see (in counterclock wise order):
  - A time series of the selected variable at the clicked height
  - A vertical profile of the selected variable at the clicked time
  - The Doppler spectrum at the clicked time and height
  - A spectrogram (height distribution of Doppler spectra) for the clicked time
  
This project has been coded in one afternoon, sorry for the lack of code documentation
