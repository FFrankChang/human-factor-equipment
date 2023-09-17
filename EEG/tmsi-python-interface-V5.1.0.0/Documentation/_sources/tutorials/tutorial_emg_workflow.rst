.. _tutorial-emg-page-label:

Tutorial HD-EMG Workflow
==========================

This tutorial provides a step-by-step guide on running the *example_EMG_workflow.py* located inside the *examples_SAGA* folder.

Adding the correct directory of files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To recognize the TMSi Python Interface folder, which is necessary for running the examples, your Python interpreter needs to know the corresponding path. 
Therefore, the first lines of code add this information. If you wish to store the recordings in a different folder than the default one, you can change the directory given 
in line 40.

.. literalinclude:: ..\..\..\examples_SAGA\example_EMG_workflow.py
    :language: python
    :lines: 36-43
    :linenos:
    :emphasize-lines: 5
    :lineno-start: 36

Importing the required classes and functions from TMSi SDK
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These are the libraries which are implemented by TMSi and are required for the example script to work. They are used for purposes such as 
handling errors, writing recording files on PC, and plotting incoming data.

.. literalinclude:: ..\..\..\examples_SAGA\example_EMG_workflow.py
    :language: python
    :lines: 45-54
    :lineno-start: 45
    :linenos:

Finding connected devices
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It’s possible to have more than one device connected. The Python Interface can be used to discover each device. Therefore, it’s necessary to specify the type of 
connected device as well as the interface via which the device is connected to PC (line 58).
For SAGA amplifiers, the Docking Station (DS) is always connected via USB. The connection of the Data Recorder (DR) with the DS can be either docked, optical or wifi.
In this case, the example uses a docked SAGA. 

Next, a list of connected devices (device type has already been specified) can be stored inside variable *discoveryList*.
The next line of code (line 61) is a check to ensure that at least one device has been discovered. When one or multiple devices are found, the first device is opened.
The handle to this discovered device is stored in the variable *dev*. The *dev.open()* command opens a connection to SAGA.

.. literalinclude:: ..\..\..\examples_SAGA\example_EMG_workflow.py
    :language: python
    :lines: 57-66
    :linenos:
    :lineno-start: 57
    :emphasize-lines: 2,5

Configuring the device
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After opening the connection to the device, the correct measurement configuration needs to loaded. The configuration defines which channels are enabled, the used channel names and
whether common reference or average reference mode is used. In this example, the grid type that is used is set first. There are multiple options for 
the type of grid, that are listed below the variable. The TMSi Python Interface comes with standard configurations, which are loaded in this example by lines 
74 or 76 (depending on the SAGA version). The configuration is different for a 32-channel or a 64-channel SAGA. The configuration .xml files sets average referencing, the correct channel names
and that all non-UNI channels are disabled. The default sampling rate for HD-EMG is set to 2000 Hz.

.. literalinclude:: ..\..\..\examples_SAGA\example_EMG_workflow.py
    :language: python
    :lines: 68-76
    :linenos:
    :lineno-start: 68

The plotter: check impedances
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before starting the measurement, it is important to check the impedances. The impedances are an indicator for signal quality. In general, the lower the impedance,
the better the signal quality. Please note that with HD-EMG grids, if they are not prepared properly, cross-bridges may occur. Ihe following code snippet 
the impedances are checked by visually inspecting the impedances per electrode. The required graphical user interface (GUI) and plotter were initially 
imported from *TMSiGui* and *TMSiPlotterHelpers*. (for more information about the plotters, please read the 
:ref:`Plotters Tutorial <TMSi Plotter tutorial>`). In this case, the ImpedancePlotterHelper is initialized in lines 86 to 88. Three parameters can be specified for the impedance plotter. The 
first parameter is the device that is passed to the Helper. The second variable, the layout variable, defines if the electrode impedances should
be visualized as a head (for EEG) or in a Grid form (for HD-EMG). Finally, the impedances can be stored in a file: the third parameter defines the 
location and name of the file.

.. literalinclude:: ..\..\..\examples_SAGA\example_EMG_workflow.py
    :language: python
    :lines: 78-92
    :linenos:
    :lineno-start: 78

Writing measurement to file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The TMSi Python interface allows to record data in either .poly5 or .xdf format. Therefore, the user is asked to provide a desired file format 
(line 99). Lines 102 to 108 ensure that the specified file format is initialized. Here, it is also possible to specify the 
directory in which the recordings are stored. The default is set to the *measurement_dir* (defined earlier) located inside the TMSi Python interface folder.
Please note, if neither .poly5 nor .xdf is given as input, the data will be saved as .poly5 (lines 106 to 108).
Moreover, it is required for the *file_writer* to get a handle to the device specified in the *discoveryList*, which is done in line 111.
The default file name is *example_EMG_workflow*. If the user wishes to change the file name, lines 102-108 can be edited. 


.. literalinclude:: ..\..\..\examples_SAGA\example_EMG_workflow.py
    :language: python
    :lines: 98-111
    :linenos:
    :lineno-start: 98

The plotter: heatmap plotter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once that the file format is chosen, a new plotter is initialized in line 116. In this case, a heatmap is created from the raw data. Therefore, the 
HeatmapPlotterHelper is initialized. Four parameters can be given to this Helper: the device should be passed, the layout of the grid that was specified
in the beginning of the file is needed and the filter variables (order and cut-off frequency). In this case, a first-order high-pass filter with a cut-off frequency of 5 Hz is applied to the data. 
The plotter is opened when the GUI is initialized and the event loop has been started, which is done in line 120.

.. literalinclude:: ..\..\..\examples_SAGA\example_EMG_workflow.py
    :language: python
    :lines: 113-120
    :linenos:
    :lineno-start: 113

Closing the application
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After the measurement is performed and the plotter window is closed, the *file_writer* is stopped and the connection to the device is closed.

.. literalinclude:: ..\..\..\examples_SAGA\example_EMG_workflow.py
    :language: python
    :lines: 122-126
    :linenos:
    :lineno-start: 122

In case of any error, the *Finally* statement in line 132 properly closes the connection to the device if this has not been done before. Afterwards, it is 
possible to use SAGA again for a different application or a new measurement.

.. literalinclude:: ..\..\..\examples_SAGA\example_EMG_workflow.py
    :language: python
    :lines: 132-136
    :linenos:
    :lineno-start: 132

Summary
^^^^^^^^^^^^^^^^^^
To wrap it up, assuming that the device driver is installed, recording data in Python using a TMSi amplifier is done by following the steps below. 
You can use the same flow to write your own script.

.. figure:: summary_eeg_emg_tutorials.png

    Figure 1: Overview of the general worflow to record data with a TMSi amplifier in Python