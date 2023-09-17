Plugins
================

In the TMSiPlugins/ folder, code to combine the TMSi Python Interface with other 
libraries or external devices is provided. Every plugin has a separate folder, which is
explained below.

External devices
--------------------------------
This folder contains example code to use external devices that are supported by 
TMSi to use with SAGA. 

.. list-table:: 
    :widths: 30 70
    :header-rows: 0
    :stub-columns: 1

    * - usb ttl device 
      - This file contains the class to write triggers to SAGA or APEX via the USB-TTL module, using the device-specific trigger cable sold by TMSi. With this class, it is possible to initialize and find the USB-TTL module and write triggers to the SAGA/APEX TRIGGER interface. Please note that the USB-TTL module is specified per TMSi device.
    


PsychoPy
--------------------------
This folder contains example code to show how to combine sending triggers to SAGA or APEX
while running a pre-coded PsychoPy experiment (only possible with Python version 3.8). TMSi has not tested other examples with Python version 3.8.

**Using TMSiPlugins/PsychoPy**

To use the PsychoPy plugins that are provided in TMSiPlugins, a few preparatory steps are required. First, Python version 3.8 needs to be installed, as PyschoPy currently relies on this version of Python. Secondly, a new virtual environment can be created (in Python 3.8), where the libraries listed in requirements39_Windows.txt can be installed using pip. After installing these libraries, PsychoPy needs to be installed with pip (version 2022.2.5). This sequence of steps is required as PsychoPy may need some alternative library versions, which should be considered more important.   

To use the example code, additional steps need to be taken, as the correct graphics backend needs to be configured. First, open ‘Control Panel - Edit System Environment Variables - Environment Variables’. Next, below User variables, click ‘New…’. In the ‘Variable name:’ field, you should add *PYQTGRAPH_QT_LIB* and in the ‘Variable value:’ field, you should add *PySide2*. After completing the steps above, the example can be used with the virtual environment that has just been created.  

.. list-table:: 
    :widths: 30 70
    :header-rows: 0
    :stub-columns: 1

    * - Experiment PsychoPy
      - This class demonstrates how to create an auditory oddball experiment with the PsychoPy Python Library. It also shows how to simultaneously provide stimuli to the subject and send triggers to SAGA’s or APEX' TRIGGER port with the USB-TTL module.
    * - Example PsychoPy ERP experiment SAGA 
      - This example shows how to simultaneously run an auditory oddball PsychoPy experiment and view and save the signals during the experiment with SAGA.
    * - Example PsychoPy ERP experiment APEX 
      - This example shows how to simultaneously run an auditory oddball PsychoPy experiment and view and save the signals during the experiment with APEX.
