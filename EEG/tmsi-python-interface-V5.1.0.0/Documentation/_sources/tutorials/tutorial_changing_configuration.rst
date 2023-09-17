Tutorial changing configuration (APEX)
==========================================

This tutorial provides a step-by-step guide on running the *example_change_channel_list.py* located inside the *examples_APEX* folder.

Using TMSi APEX amplifier it’s possible to select any (sub)set of channels to be included in the signal's acquisition reference calculation. The TMSi Python interface can be used to change this parameter as well as the channel names.

Adding the correct directory of files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To recognize the TMSi Python interface folder, which is necessary for running the examples, your Python interpreter needs to know the corresponding path. 
Therefore, the first lines of code add this information. If you wish to store the recordings in a different folder than the default one, you can change the directory given 
in line 39.

.. literalinclude:: ..\..\..\examples_APEX\example_change_channel_list.py
    :language: python
    :lines: 35-40
    :linenos:
    :lineno-start: 35
    :emphasize-lines: 5

Importing the required classes and functions from TMSi SDK
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These are the libraries which are implemented by TMSi and are required for the example script to work. They are used for purposes such as 
handling errors, writing recording files on PC, and plotting incoming data.

.. literalinclude:: ..\..\..\examples_APEX\example_change_channel_list.py
    :language: python
    :lines: 43-47
    :linenos:
    :lineno-start: 43

Finding connected devices
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
It’s possible to have more than one device connected. The Python interface can be used to discover each device. Therefore, it’s necessary to specify the type of 
connected device as well as the interface via which the device is connected to PC (line 51). For APEX it can be either *usb* or *bluetooth*. 
Next, a list of connected devices (device type has already been specified) can be stored inside variable *discoveryList*. The next line of code (line 54)
is a check to ensure that at least one device has been discovered. When one or multiple devices are found, the first device is opened.
The handle to this discovered device is stored in the variable *dev*. The *dev.open()* command opens a connection to APEX.

.. literalinclude:: ..\..\..\examples_APEX\example_change_channel_list.py
    :language: python
    :lines: 50-59
    :linenos:
    :lineno-start: 50

Configuring reference channels 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Once a connection to the device is opened, it is possible to configure the reference channels. This can be done by calling the *set_device_references* method from *dev* class.
There are two arguments for this method:

* *‘list_references’*, which is a binary list containing value 1 for each channel that should be included in reference calculation and value 0 for each of other channels (line 62).
* *‘list_indices’*, which is a list containing channel indices that correspond to each value given in *‘list_references’* (line 63).

.. literalinclude:: ..\..\..\examples_APEX\example_change_channel_list.py
    :language: python
    :lines: 61-63
    :linenos:
    :lineno-start: 61


Changing channels names
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Using the method *‘set_device_channel_names’* from class *‘dev’*, custom channel names can be set on the provided indices. Channels with indices 1 and 7
will get new names *‘Fpz’* and *‘F8’* respectively. In a similar way, more/less channels could be renamed to custom names.  

.. literalinclude:: ..\..\..\examples_APEX\example_change_channel_list.py
    :language: python
    :lines: 65-66
    :lineno-start: 65

Plotting the signals
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The plotter helper defines which plotter we use to view the signals. In this case, raw signals without any 
processing are desired. Therefore, the SignalPlotterHelper is initialized. This Helper needs a handle to the device, which is why the device is passed  
as variable. The GUI opens the defined plotter and shows the signals. For more infomration on plotters, please review :ref:`Tutorial Plotters <TMSi Plotter tutorial>`

.. literalinclude:: ..\..\..\examples_APEX\example_change_channel_list.py
    :language: python
    :lines: 68-79
    :linenos:
    :lineno-start: 68

Closing the connection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Once the GUI is closed by the user, the event loop is stopped. Next, the connection to the device can be closed properly. APEX is now ready to be used again.

.. literalinclude:: ..\..\..\examples_APEX\example_change_channel_list.py
    :language: python
    :lines: 81-82
    :linenos:
    :lineno-start: 81


