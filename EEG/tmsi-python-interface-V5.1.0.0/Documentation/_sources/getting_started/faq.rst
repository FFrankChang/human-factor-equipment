FAQ
===========
In this FAQ, a small overview of questions that are frequently asked is given. More device-related questions are answered on our `Knowledge Base <https://knowledge.tmsi.com/>`_


**An unexpected error occurred. Is there anything I should do before I can start a new measurement?**

A: When the script stops running, this does not necessarily mean that the device 
has stopped sampling. Please reset the device (removing the USB cable or 
performing a hardware reset in the case of Bluetooth), after which you can reopen 
the connection to the device in a new Python kernel. 


**What parameters/(meta)data can I access when loading a .Poly5 file?**

A: The following parameters can be retrieved when a Poly5Reader object is created: 
samples (containing the acquired data), channels (list containing all information 
from the Channel class), sample_rate, num_samples, num_channels, ch_names 
(containing all channel names) and ch_unit_names (containing all unit names of 
the used channels).

**What do I need to do if I get " response time-out" after an error?**

A: First thing to do is to repower the device and try again. If this does not work, 
restart the Python Console, otherwise restart the computer. Also make sure you 
have followed the steps mentioned in the User Manual of your device for correct 
installation.

**I want to control configurations that are not shown in the examples. How do I know how to control them?**

A: Not all functionality of the interface is shown in the examples. More information 
can be found in the inline documentation of the interface. More information about 
general control of the device can be found in the :ref:`Device API <API Reference>`.

**Why do I have to set a divider for a different sample rate for SAGA?**

A: The sample rate of SAGA device can only be set by the base sample rate divided 
by a power of 2. For example, with a base sample rate of 4000 Hz, the possible 
sample rates are 4000, 2000, 1000 or 500 Hz. To get these you will have to set the 
channel divider to respectively 1, 2, 4 or 8. See the code snippet below (from example_changing_sample_rate.py).

.. literalinclude:: ..\..\..\examples_SAGA\example_changing_sample_rate.py
    :language: python
    :lines: 101-103

**What do I need to do if I get "Docking Station response time-out" after an error?**

A: First thing to do is to repower both Docking Station and Data Recorder and try 
again. If this does not work, restart the Python Console, otherwise restart the
computer. Also make sure you have followed the steps mentioned in the User 
Manual of your device for correct installation.


