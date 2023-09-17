Examples reading and analyzing data 
========================================
Aside from the examples that show how to specifically operate your SAGA or APEX device, there are also some generic examples that show how to load or 
process acquired data. The examples can be found in the “examples_reading_data” folder. This folder contains the examples below.



.. list-table:: 
    :widths: 30 70
    :header-rows: 0
    :stub-columns: 1

    * - Example file reader 
      - This example loads files and shows how to retrieve the data from .Poly5, .XDF or .EDF-file formats. The type of variables that are retrieved are the sampling frequency, samples, number of channels and channel names.
    * - Example file viewer
      - This example shows how to read data from an .Poly5, .XDF or EDF-file, convert it in a data object that can be used in MNE-Python and plot the data for viewing purposes using MNE’s interactive plotter. Reordering of data measured with HD-EMG grids is automatically applied when HD-EMG channel names are used.
    * - Example ICA 
      - This example shows how to post-process Poly5 data with MNE ICA to remove EOG artefacts.
    * - Example poly5 to edf
      - This example shows the offline conversion of .Poly5 files to .EDF files. Please note that EDF is a 16-bit file format, which requires pre-processing to remove the offset. The data can be either high-pass or bandpass filtered, in order to retain as much relevant information as possible in the conversion from the 32-bit to the 16-bit file format. Also note that the conversion requires the entire data file to be loaded in memory. The available RAM can be a limiting factor in the conversion of large data files. 
    * - Example poly5 to edf batch conversion
      - This example shows the offline conversion of .Poly5 files to .EDF files in batch, by converting all files in a selected folder (and its subfolders).
    * - Example reading live impedances
      - This example shows how to retrieve the saved live impedance values (recorded with APEX) from a stored .Poly5 or .XDF data file. Data is plotted for some channels.
    * - Example synchronise xdf
      - This function shows how to synchronize two data streams in an .xdf file, that have been collected with the LSL-based LabRecorder application.
    




