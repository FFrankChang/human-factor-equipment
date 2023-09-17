.. _tutorial-eeg-page-label:

Tutorial EEG Workflow (APEX)
===============================

This tutorial provides a step-by-step guide on running the *example_EEG_workflow.py* located inside the *examples_APEX* folder.

Adding the correct directory of files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To recognize the TMSi Python interface folder, which is necessary for running the examples, your Python interpreter needs to know the corresponding path. 
Therefore, the first lines of code add this information. If you wish to store the recordings in a different folder than the default one, you can change the directory given 
in line 42.

.. literalinclude:: ..\..\..\examples_APEX\example_EEG_workflow.py
    :language: python
    :lines: 38-45
    :linenos:
    :lineno-start: 38
    :emphasize-lines: 5

Importing the required classes and functions from TMSi SDK
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These are the libraries which are implemented by TMSi and are required for the example script to work. They are used for purposes such as 
handling errors, writing recording files on PC, and plotting incoming data.

.. literalinclude:: ..\..\..\examples_APEX\example_EEG_workflow.py
    :language: python
    :lines: 47-53
    :linenos:
    :lineno-start: 47

Finding connected devices
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It’s possible to have more than one device connected. The Python interface can be used to discover each device. Therefore, it’s necessary to specify the type of 
connected device as well as the interface via which the device is connected to PC (line 58). For APEX it can be either *usb* or *bluetooth*. 
Next, a list of connected devices (device type has already been specified) can be stored inside variable *discoveryList*. The next line of code (line 61)
is a check to ensure that at least one device has been discovered. When one or multiple devices are found, the first device is opened.
The handle to this discovered device is stored in the variable *dev*. The *dev.open()* command opens a connection to APEX.

.. literalinclude:: ..\..\..\examples_APEX\example_EEG_workflow.py
    :language: python
    :lines: 57-66
    :linenos:
    :lineno-start: 57

Loading desired device configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As shown in the beginning, the pre-defined configuration files are located inside the configs folder of the TMSi Python interface (*TMSiSDK\tmsi_resources*). It is also 
possible to create custom configurations and save these as .xml files. In this example, a 32-channel configuration with EEG 
labeling is loaded to the device (line 75). Please make sure to load the device configuration after opening a connection to the device.

.. literalinclude:: ..\..\..\examples_APEX\example_EEG_workflow.py
    :language: python
    :lines: 68-75
    :linenos:
    :lineno-start: 68

Initializing impedance plotter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In most EEG measurements, it is common to monitor impedances prior to signal acquisition. Therefore, once the device configuration 
is set, a real-time plotter is initialized. As shown, the required graphical user interface (GUI) and plotter helper were initially imported from *TMSiGui* 
and *TMSiPlotterHelpers*. The plotter helper defines which plotter is shown by the GUI (for more information about the plotters, please read the 
:ref:`Plotters Tutorial <TMSi Plotter tutorial>`). In this case, the ImpedancePlotterHelper is initialized in line 85. Three parameters can be specified for the impedance plotter. The 
first parameter is the device that is passed to the Helper. The second variable, the layout variable, defines if the electrode impedances should
be visualized as a head (for EEG) or in a Grid form (for HD-EMG). Finally, the impedances can be stored in a file: the third parameter defines the 
location and name of the file.

.. literalinclude:: ..\..\..\examples_APEX\example_EEG_workflow.py
    :language: python
    :lines: 77-91
    :linenos:
    :lineno-start: 77

Initializing file writer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The TMSi Python interface allows to record data in either .poly5 or .xdf format. Therefore, the user is asked to provide a desired file format 
(line 98). Line 101 - 107 ensures that the specified file format is initialized. Here, it is also possible to specify the 
directory in which the recordings are stored. The default is set to the *measurement_dir* (defined earlier) located inside the TMSi Python interface folder.
Please note, if neither .poly5 nor .xdf is given as input, the data will be saved as .poly5 (lines 105 - 107).
Moreover, it is required for the *file_writer* to get a handle to the device specified in the *discoveryList*, which is done in line 110.
The default file name is *example_EEG_workflow*. If the user wishes to change the file name, lines 101-107 can be edited. 


.. literalinclude:: ..\..\..\examples_APEX\example_EEG_workflow.py
    :language: python
    :lines: 97-110
    :linenos:
    :lineno-start: 97

Initializing signal plotter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This step is very similar to initializing the impedance plotter. As plotting the real-time signal (instead of impedances) 
is desired, the SignalPlotterHelper is needed. The SignalPlotterHelper only needs the device as input parameter. The
GUI is initialized based on the correct Helper and the GUI's event loop is started by line 117.

As soon as the GUI is closed by the user, it is crucial to stop the *file_writer* and then close the connection to the device. 

For simplicity, the explanation of try…except statement was skipped in this tutorial.

.. literalinclude:: ..\..\..\examples_APEX\example_EEG_workflow.py
    :language: python
    :lines: 112-123
    :linenos:
    :lineno-start: 112

Summary
^^^^^^^^^^^^

To wrap it up, assuming that the device driver is installed, recording data in Python using a TMSi amplifier is done by following the steps below. 
You can use the same flow to write your own script.

.. figure:: summary_eeg_emg_tutorials.png

    Figure 1: Overview of the general worflow to record data with a TMSi amplifier in Python






